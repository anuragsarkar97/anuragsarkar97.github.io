# Agent

You may review a note, and you may publish it, without asking again. Publish only when the task is to publish and `make review` passed. A review task stops after `make review`.

The site is a Jekyll notes blog. GitHub Pages builds `master` from this repository. Commit source, cover SVGs, and `public/css/app.css`. Do not commit `_site`, `node_modules`, `__pycache__`, or `.DS_Store`. Do not force-push.

## Write

```sh
make new TITLE="Short name of the problem"
```

That writes `_posts/YYYY-MM-DD-slug.md` from `docs/note-template.md` and `public/images/notes/<slug>.svg`. Set `topic` to `Systems`, `Platforms`, or `Craft`, then regenerate the cover:

```sh
python3 scripts/note_images.py _posts/YYYY-MM-DD-slug.md
```

`state` is only a label when `topic` is empty. It does not hide a note. A note that is not ready gets `published: false`. Jekyll then omits it. Remove that line only after review passes.

Keep a published filename stable. Open with the problem, not a heading or a code fence. Use `##` for sections. Put a language on every code fence. Put figures in `public/images/figures/` and point at them from the note. The cover is not a figure in the body.

Preview with `make preview` at http://127.0.0.1:4000. If that port is taken, the preview is already running. `make review` builds into a temp directory and leaves it alone.

## Review

Run `make review`. It runs `scripts/check_notes.py`, `scripts/review_notes.py`, a production build, and `scripts/check_site.rb`. Fix a failing check before you read the note as finished.

Then read the note. Publish it only when all of these are true:

- The dem is one real sentence, not the template sentence.
- The opening names a concrete failure. The template paragraph is gone.
- Example is one case a reader can follow. Determinations are actions.
- External references name real works. Do not invent a title or a URL.
- Images exist on disk and have alt text.
- `topic` is Systems, Platforms, or Craft when the note has one.
- A draft still has `published: false`.

`make review` does not judge the argument. You do. If the read fails, do not publish. Say what failed.

## Publish

```sh
make publish MSG="Publish the note on the ack window"
```

`make publish` depends on `make review`. It stages the publication paths in the Makefile, commits with `MSG` when anything changed, and runs `git push origin HEAD`. It does not use `--force`. The message names the note.

If the push is rejected, stop and report the remote output. Do not force-push, rebase, or delete the remote branch.

Pages serves `master`. Pushing another branch updates that branch and does not change the site.
