#!/usr/bin/env python3
"""Check that every note follows docs/note-template.md. Uses the Python standard library only."""

import pathlib
import sys

root = pathlib.Path(__file__).resolve().parents[1]
errors = []
posts = sorted((root / "_posts").glob("*.md"))

for path in posts:
    text = path.read_text()
    name = path.name
    if not text.startswith("---\n") or "\nstyle: rfd\n" not in text.split("\n---\n", 1)[0] + "\n":
        errors.append(f"{name}: set style: rfd")
        continue
    front, _, body = text.partition("\n---\n")
    if not body.strip():
        errors.append(f"{name}: missing body")
        continue
    if not any(line.startswith("title:") and line.strip() != "title:" for line in front.splitlines()):
        errors.append(f"{name}: needs a title")
    if not any(line.startswith(("dem:", "description:")) and len(line.split(":", 1)[1].strip()) for line in front.splitlines()):
        errors.append(f"{name}: needs dem (the one-line summary)")
    start = body.lstrip()
    if start.startswith("#") or start.startswith("```"):
        errors.append(f"{name}: open with the problem, not a heading or code fence")
    for heading, label in (
        ("## Determinations", "a Determinations section"),
        ("## External references", "an External references section"),
    ):
        if heading not in body:
            errors.append(f"{name}: missing {label}")

if errors:
    sys.exit("\n".join(errors))

print(f"PASS: {len(posts)} note(s) match the template.")
