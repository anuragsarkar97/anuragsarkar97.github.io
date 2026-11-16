#!/usr/bin/env python3
"""Create a note from docs/note-template.md."""

import datetime
import pathlib
import re
import sys

import note_images

root = pathlib.Path(__file__).resolve().parents[1]
template = (root / "docs" / "note-template.md").read_text()


def slug(title):
    text = title.lower()
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:80] or "note"


def main():
    if len(sys.argv) > 2:
        sys.exit("usage: python3 scripts/new_note.py \"Title\"")
    title = sys.argv[1].strip() if len(sys.argv) == 2 else input("Title: ").strip()
    if not title:
        sys.exit("a title is required")
    day = datetime.date.today().isoformat()
    path = root / "_posts" / f"{day}-{slug(title)}.md"
    if path.exists():
        sys.exit(f"already exists: {path.relative_to(root)}")
    body = template.replace('title: "Short name of the problem"', f'title: {title!r}', 1)
    path.write_text(body)
    note_images.write_note(path)
    print(path.relative_to(root))


if __name__ == "__main__":
    main()
