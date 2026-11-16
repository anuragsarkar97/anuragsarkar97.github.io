---
layout: post
title: "When the ack arrives after the caller leaves"
dem: "A broker can tell the caller the write succeeded while the disk is still deciding, and the retry then writes the same key twice."
state: published
style: rfd
topic: Systems
---

A publish call can return success and still lose the record. The broker appends the record to a memory log, acknowledges the caller, and only then asks the disk to make the write durable. If the caller gives up during that gap, it retries. The first write may land after the second one, or it may not land at all. The caller has already been told that both attempts worked.

This is not a crash in the mutex, and it is not a network partition you can draw as two islands. It is three clocks that the API treats as one. The caller’s timeout, the broker’s acknowledgement, and the disk’s `fsync` each finish on their own schedule. The bug appears when the first of those clocks is allowed to speak for the other two.

The note walks one key, `invoice-1847`, through that gap. The numbers are from a single broker process with one volume. A replicated log changes the width of the window. It does not close it, unless the acknowledgement waits for the durability rule the caller was promised.

## Example

The caller is a web handler with a 200 ms budget. The broker is in the same building. The disk is a single volume that sometimes returns `ENOSPC` after it has already accepted the write into its own cache.

1. `web-6` sends the record and starts a 200 ms timer.
2. The broker appends the record at offset `90211` and returns an ack from memory.
3. `web-6` receives the ack, writes its own success log, and closes the connection.
4. The volume returns `ENOSPC` for offset `90211`. Nobody is listening.
5. A later retry from the same user sends the key again. The broker appends it at offset `90240` and acks that one too.

<figure>
  <img src="{{ '/public/images/figures/ack-window.svg' | relative_url }}" alt="Timeline of the caller, the broker, and the disk. The caller leaves after the memory ack and before the disk write fails." width="1200" height="640" loading="lazy" decoding="async">
  <figcaption>The dashed line is the moment the caller leaves. The disk error lands to the right of it.</figcaption>
</figure>

The producer treats the ack as the end of the call. The comment in `Publish` is the whole defect. The function tells the truth about the memory log and then does the slow work after the caller has been released.

```go
func (b *Broker) Publish(ctx context.Context, rec Record) error {
    b.mu.Lock()
    defer b.mu.Unlock()

    offset := b.log.Append(rec)
    // The caller is released here. The disk write has not started.
    if err := b.ack(rec.Caller, offset); err != nil {
        return err
    }
    if err := b.disk.Write(ctx, offset, rec); err != nil {
        b.log.MarkLost(offset)
        return fmt.Errorf("publish %s at offset %d: disk write failed after the caller was acknowledged: %w", rec.Key, offset, err)
    }
    return nil
}
```

> **Note**
>
> `MarkLost` updates the broker’s own log. It does not reach the caller that already closed the socket. A lost offset is not a failed request unless someone is still waiting for the request.

The caller’s retry uses the same context it just gave up on. The second `Publish` is born cancelled, or it is given a fresh timeout that overlaps the first disk write. Either way the key now has two live attempts.

```go
func (c *Client) Put(ctx context.Context, key string, value []byte) error {
    ctx, cancel := context.WithTimeout(ctx, 200*time.Millisecond)
    defer cancel()

    rec := Record{Key: key, Value: value, Caller: c.id}
    err := c.broker.Publish(ctx, rec)
    if errors.Is(err, context.DeadlineExceeded) {
        // The first write may still be on its way to the volume.
        return c.broker.Publish(context.WithoutCancel(ctx), rec)
    }
    return err
}
```

A single key is enough to see the overlap. The shaded span in the next figure is the interval during which both attempts believe they own `invoice-1847`.

<figure>
  <img src="{{ '/public/images/figures/retry-overlap.svg' | relative_url }}" alt="Two bars for the same key. Attempt 2 starts before attempt 1 has finished writing." width="1200" height="520" loading="lazy" decoding="async">
  <figcaption>Attempt 2 starts a new timeout. Attempt 1 has not finished with the disk.</figcaption>
</figure>

The broker’s log, trimmed to the lines that matter, reads:

```text
14:02:11.018 ack    key=invoice-1847 offset=90211 caller=web-6
14:02:11.019 closed caller=web-6
14:02:11.440 disk   offset=90211 error=ENOSPC
14:02:11.441 retry  key=invoice-1847 caller=web-6
14:02:11.455 ack    key=invoice-1847 offset=90240 caller=web-6
14:02:12.102 disk   offset=90240 ok
14:02:12.880 disk   offset=90211 ok    replayed by the volume
```

Line six and line seven are the damage. The volume eventually stored both copies. The second ack is the one the user interface kept. A reader that tails the log from the end returns the later record. A reader that scans from an older snapshot can still return the first. For an invoice, those two records were not equal. The retry had already added a tax line.

## What the caller believes

The handler has one return value. The system underneath it has three clocks, and the handler can see only the first.

| Clock | What it actually measures | What the caller treats it as |
| --- | --- | --- |
| Ack | The record is in the broker’s memory log | The record is durable and will not be written again |
| Disk | The volume has the bytes, or it has refused them | Invisible, once the ack has been sent |
| Timeout | The caller stopped waiting | A reason to send the same key again |

Read down the middle column and the right column is the bug. Nothing in the table is a slow computer. Each clock is doing the job it was built for. The API’s mistake is the sentence “the call returned, so the write is finished.”

The caller also keeps a local story about the key:

- Before the ack, the key is in flight and must not be shown to the user as saved.
- After the ack, the key is saved, and the handler may release the request.
- After a timeout, the key is *not* saved, so the handler may send it again.

The third bullet is the one that fails. A timeout means the handler stopped waiting. It does not mean the broker stopped writing. The two facts get joined because the client code has nowhere else to put a half-finished call.

Two details decide whether the retry is safe:

- The broker can reject a second append of a key that still has an attempt in `MarkLost` or in flight.
- The caller can attach the attempt id it already used, and the broker can treat a repeat of that id as the same write.

Neither detail exists on this path. The record carries a caller name and a key. It does not carry an attempt id. The broker’s deduplication, such as it is, looks at the key only after both writes have been acknowledged.

## What causes it

Three conditions have to be true together. Any one of them, alone, is a normal publish.

### The ack leaves before the disk

`b.ack` runs before `b.disk.Write`. The lock is held across both, so the broker’s own process is consistent: a reader on this process will not observe the offset until the append has happened. The caller is not a reader on this process. The caller is a socket. The socket gets the ack while the lock is still held and the disk call has not begun.

Holding the lock longer does not repair that. It only makes the next publisher wait behind a write the first caller has already stopped waiting for.

### The timeout is allowed to mean “send it again”

A 200 ms budget is a product decision. The page should not spin. The defect is the `if` that turns `context.DeadlineExceeded` into a second `Publish` of the same key. The retry is unconditional. It does not ask the broker whether offset `90211` is still open, lost, or durable.

The fresh context from `context.WithoutCancel` is the right way to keep the process alive for a cleanup. It is the wrong way to start a second write. The first write is still the owner of the key until the broker says otherwise.

### The volume may complete a write the broker has marked lost

`ENOSPC` arrived once. The volume later replayed the same offset and stored it. `MarkLost` had already told the broker’s log to forget the record. The disk did not forget. A lost offset and a stored offset are both in the system, and they disagree.

> The ack is not a lie about the present. It is a promise the process may not live long enough to keep.

That promise is what the user interface rendered. The invoice page said the draft was saved. The draft on disk, when the replay landed, was the draft from before the tax line.

## Determinations

- Acknowledge a record only after the durability rule you documented has been met. For this broker, that rule is `fsync` on the volume, not the append to the memory log.
- Give every attempt an id. A retry sends the same id. The broker returns the original offset and does not append a second record.
- Treat a caller timeout as “stop showing a spinner.” Do not treat it as “the write did not happen.”
- When the disk reports a failure, keep the offset visible as lost until a later read proves the volume does not have it. Do not let a replay become a second success.

### Dropping the timeout does not help

The tempting fix is to wait. Remove the 200 ms budget, hold the handler open, and let `Publish` return only after `disk.Write`. The page stops lying. It also stops answering. A volume that stalls for seconds pins a web worker for seconds, and the user refreshes, which is another retry with a new attempt.

```go
func (b *Broker) Publish(ctx context.Context, rec Record) error {
    offset := b.log.Append(rec)
    if err := b.disk.Write(ctx, offset, rec); err != nil {
        b.log.MarkLost(offset)
        return err
    }
    return b.ack(rec.Caller, offset)
}
```

This version has the ack on the correct side of the disk write. It is still incomplete. `MarkLost` races the volume’s replay, and a browser refresh still sends the key again unless the attempt id is stable across that refresh. Moving the ack is necessary. It is not the whole fix.

#### What the handler should do instead

Show the draft as *in flight* until the broker returns the offset for that attempt id. If the handler is still waiting when the page’s budget runs out, keep the attempt id in the session and ask for that offset on the next load. Do not mint a new id because a timer fired.

## Open questions

The volume replayed a write the broker had marked lost. It is not settled whether the broker should read the offset back after `ENOSPC`, or whether the volume’s contract already forbids a later success. The log from 16 November shows one replay. That is enough to stop trusting `MarkLost` by itself. It is not enough to write the volume’s rule into this note.

A replicated broker, with the ack waiting for a quorum, shrinks the window to the time between the quorum and the caller’s timeout. It does not answer what a minority replica should do with a write the quorum never saw. That case belongs in a separate note once this path refuses a second attempt id.

## External references

- Go. [context](https://pkg.go.dev/context). 2026.
- Linux. [fsync](https://man7.org/linux/man-pages/man2/fsync.2.html). 2024.
- Martin Kleppmann. [Please stop calling databases CP or AP](https://martin.kleppmann.com/2015/05/11/please-stop-calling-databases-cp-or-ap.html). 2015. A single label was doing the work of several guarantees.
- Pat Helland. [Life beyond distributed transactions](https://queue.acm.org/detail.cfm?id=3025012). 2016.
