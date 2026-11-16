#!/usr/bin/env python3
"""Mechanical review of notes before publish.

Editorial judgment is not this script. AGENT.md is. Exit 1 when a note is
unsafe to publish. Warnings do not fail the run.
"""

import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parents[1]
posts = sorted((root / "_posts").glob("*.md"))
errors = []
warnings = []
drafts = []

placeholder_dem = "One sentence a reader can use to decide whether to open the note."
placeholder_open = "State the problem in one or two paragraphs."
placeholder_title = "Short name of the problem"
topics = {"Systems", "Platforms", "Craft"}
date_prefix = re.compile(r"^(\d{4}-\d{2}-\d{2})-(.+)$")
image_ref = re.compile(r"/public/images/[A-Za-z0-9_./-]+\.(?:svg|png|jpe?g|webp|gif)")


def split_front(text):
    if not text.startswith("---\n"):
        return "", text
    front, sep, body = text.partition("\n---\n")
    if not sep:
        return "", text
    return front, body


def field(front, key):
    for line in front.splitlines():
        if line.startswith(key + ":"):
            value = line.split(":", 1)[1].strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
                value = value[1:-1]
            return value
    return None


def bare_fences(body):
    found = []
    open_fence = False
    for number, line in enumerate(body.splitlines(), 1):
        if not line.startswith("```"):
            continue
        if open_fence:
            open_fence = False
            continue
        open_fence = True
        if line.strip() == "```":
            found.append(number)
    return found


for path in posts:
    name = path.name
    match = date_prefix.match(path.stem)
    if not match:
        errors.append(f"{name}: filename must start with YYYY-MM-DD-")
        continue
    slug = match.group(2)
    text = path.read_text()
    front, body = split_front(text)
    title = field(front, "title")
    dem = field(front, "dem") or field(front, "description")
    topic = field(front, "topic")
    published = (field(front, "published") or "").lower()

    if published == "false":
        drafts.append(name)

    cover = root / "public" / "images" / "notes" / f"{slug}.svg"
    if not cover.is_file():
        errors.append(f"{name}: missing cover public/images/notes/{slug}.svg")

    if title == placeholder_title:
        errors.append(f"{name}: title is still the template")
    if dem == placeholder_dem:
        errors.append(f"{name}: dem is still the template sentence")
    if placeholder_open in body:
        errors.append(f"{name}: opening is still the template paragraph")

    if topic and topic not in topics:
        errors.append(f"{name}: topic must be Systems, Platforms, or Craft")
    elif not topic:
        warnings.append(f"{name}: no topic, so the cover stays plain")

    for line in bare_fences(body):
        errors.append(f"{name}:{line}: code fence needs a language")

    for ref in sorted(set(image_ref.findall(text))):
        target = root / ref.lstrip("/")
        if not target.is_file():
            errors.append(f"{name}: missing image {ref}")

if errors:
    sys.exit("\n".join(errors))

for note in drafts:
    print(f"draft: {note} (published: false, omitted from the site)")
for note in warnings:
    print(f"warn: {note}")
if not posts:
    print("warn: no notes in _posts/")
print(f"PASS: {len(posts)} note(s) reviewed, {len(drafts)} draft(s).")
