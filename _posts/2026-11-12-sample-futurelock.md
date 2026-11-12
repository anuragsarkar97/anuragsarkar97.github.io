---
layout: post
title: "A lock held across two waits"
dem: "A task that waits on one future while holding a lock the other future needs will stall both."
emoji: lock
state: discussion
style: rfd
---

A task owns a lock, starts a wait, and the work that would release the lock is scheduled on that same task. Nothing is looping. Both sides are simply waiting for each other, and the process looks idle.

This shows up in async runtimes where one task polls many futures. The lock is not the bug by itself. The bug is holding it across a point where the runtime must poll something else to make progress.

## Example

1. Task A locks a mutex and starts a request.
2. The request's completion is a future that Task A is also responsible for polling.
3. Task A is blocked inside the lock, so it never polls that future.
4. The future never completes, so the lock is never released.

> **Note**
>
> The mutex is not deadlocked with a second mutex. It is deadlocked with the scheduler. Looking only for lock-order cycles will miss it.

```rust
// Task A holds `guard` and then waits.
let guard = mutex.lock().await;
join(request, other_work).await;
drop(guard);
```

## What causes it

Three conditions have to be true together. The task holds a resource. The next step needs that same task to run. The wait does not release the resource. Remove any one of them and the stall goes away.

## Determinations

Do not hold a lock across a wait unless the completion path is running on some other task. If the same task must both wait and make progress, drop the lock first.

A timeout on the wait hides the stall. It does not remove the cycle. Use it only as a way to surface the bug, then fix the hold.

## Open questions

How often this shows up outside async Rust, in thread pools that run the completion callback on the blocked worker, is still open.

## External references

- Oxide Computer Company. [RFD 609 Futurelock](https://rfd.shared.oxide.computer/rfd/0609). 2026.
