#!/usr/bin/env python3
"""Write a deterministic cover SVG for every note.

Each cover pairs one quiet ground with one figure. Both are chosen from
the title and topic, so running this again does not change a note that
has not changed. GitHub Pages does not run this script; commit the files
under public/images/notes/.
"""

import hashlib
import math
import pathlib
import re
import sys

root = pathlib.Path(__file__).resolve().parents[1]
out_dir = root / "public" / "images" / "notes"
date_prefix = re.compile(r"^\d{4}-\d{2}-\d{2}-(.+)$")

# One paper and one accent per topic, so a three-column grid stays in families.
families = {
    "Systems": ("#d9e2ea", "#17202a", "#163e66"),
    "Platforms": ("#f0e4d6", "#2a211b", "#8a3e24"),
    "Craft": ("#e3eee4", "#1a261c", "#1d5a36"),
}
plain = ("#eceae4", "#171717", "#171717")


class Rng:
    def __init__(self, key):
        self._seed = hashlib.sha256(key.encode()).digest()
        self._bytes = b""

    def _byte(self):
        if not self._bytes:
            self._seed = hashlib.sha256(self._seed).digest()
            self._bytes = self._seed
        value, self._bytes = self._bytes[0], self._bytes[1:]
        return value

    def pick(self, span):
        if span <= 1:
            return 0
        space, draw = 1, 0
        while space < span:
            space *= 256
            draw += 1
        limit = space - (space % span)
        while True:
            value = 0
            for _ in range(draw):
                value = value * 256 + self._byte()
            if value < limit:
                return value % span

    def between(self, low, high):
        return low + self.pick(high - low + 1)


def read_front(text):
    if not text.startswith("---\n"):
        return {}
    front = text.split("\n---\n", 1)[0]
    values = {}
    for line in front.splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        value = raw.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        values[key.strip()] = value
    return values


def ground_clear(rng, ink, accent, paper):
    return []


def ground_vsplit(rng, ink, accent, paper):
    x = rng.between(280, 920)
    if rng.pick(2):
        return [f'<rect width="{x}" height="800" fill="{accent}" opacity=".14"/>']
    return [f'<rect x="{x}" width="{1200 - x}" height="800" fill="{accent}" opacity=".14"/>']


def ground_band(rng, ink, accent, paper):
    y = rng.between(80, 540)
    height = rng.between(72, 190)
    return [f'<rect y="{y}" width="1200" height="{height}" fill="{ink}" opacity=".07"/>']


def ground_corner(rng, ink, accent, paper):
    cx, cy = ((0, 0), (1200, 0), (0, 800), (1200, 800))[rng.pick(4)]
    radius = rng.between(280, 520)
    return [
        '<g clip-path="url(#plate)">',
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{accent}" opacity=".16"/>',
        "</g>",
    ]


def ground_diagonal(rng, ink, accent, paper):
    triangles = (
        "0,0 1200,0 0,800",
        "1200,0 1200,800 0,800",
        "0,0 1200,0 1200,800",
        "0,0 1200,800 0,800",
    )
    return [f'<polygon points="{triangles[rng.pick(4)]}" fill="{accent}" opacity=".12"/>']


def ground_dots(rng, ink, accent, paper):
    step = rng.between(72, 108)
    parts = []
    y = 70
    while y < 750:
        x = 70
        while x < 1160:
            parts.append(f'<circle cx="{x}" cy="{y}" r="3.5" fill="{ink}" opacity=".28"/>')
            x += step
        y += step
    return parts


def ground_frame(rng, ink, accent, paper):
    inset = rng.between(46, 88)
    return [
        f'<rect x="{inset}" y="{inset}" width="{1200 - 2 * inset}" height="{800 - 2 * inset}" rx="32" stroke="{ink}" stroke-width="3" opacity=".4"/>'
    ]


def ground_rules(rng, ink, accent, paper):
    top = rng.between(110, 200)
    bottom = rng.between(590, 700)
    return [
        f'<path d="M120 {top} H1080" stroke="{ink}" stroke-width="3" opacity=".4"/>',
        f'<path d="M120 {bottom} H1080" stroke="{ink}" stroke-width="3" opacity=".4"/>',
    ]


def disc(rng, ink, accent, paper):
    cx, cy = rng.between(460, 740), rng.between(300, 500)
    return [
        f'<circle cx="{cx}" cy="{cy}" r="{rng.between(140, 210)}" fill="{accent}"/>',
        f'<circle cx="{cx + rng.between(-120, 120)}" cy="{cy + rng.between(-70, 70)}" r="{rng.between(80, 140)}" stroke="{ink}" stroke-width="4"/>',
        f'<path d="M180 {cy} H1020" stroke="{ink}" stroke-width="3" opacity=".35"/>',
    ]


def queue(rng, ink, accent, paper):
    count = rng.between(4, 6)
    marked = rng.pick(count)
    parts = []
    y = rng.between(160, 220)
    for index in range(count):
        color = accent if index == marked else ink
        parts.append(
            f'<rect x="200" y="{y}" width="{rng.between(340, 760)}" height="40" rx="20" fill="{color}"/>'
        )
        y += rng.between(64, 82)
    return parts


def columns(rng, ink, accent, paper):
    count = rng.between(5, 8)
    marked = rng.pick(count)
    width, gap = 58, 24
    left = (1200 - (count * width + (count - 1) * gap)) // 2
    parts = []
    for index in range(count):
        height = rng.between(140, 440)
        color = accent if index == marked else ink
        x = left + index * (width + gap)
        parts.append(f'<rect x="{x}" y="{690 - height}" width="{width}" height="{height}" rx="8" fill="{color}"/>')
    return parts


def graph(rng, ink, accent, paper):
    count = rng.between(5, 7)
    points = [(rng.between(260, 940), rng.between(180, 620)) for _ in range(count)]
    order = sorted(range(count), key=lambda index: points[index][0])
    parts = []
    for left, right in zip(order, order[1:]):
        x1, y1 = points[left]
        x2, y2 = points[right]
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ink}" stroke-width="4"/>')
    extra = rng.pick(count)
    x1, y1 = points[order[0]]
    x2, y2 = points[extra]
    parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{ink}" stroke-width="4" opacity=".4"/>')
    marked = rng.pick(count)
    for index, (x, y) in enumerate(points):
        if index == marked:
            parts.append(f'<circle cx="{x}" cy="{y}" r="18" fill="{accent}"/>')
        else:
            parts.append(f'<circle cx="{x}" cy="{y}" r="10" fill="{ink}"/>')
    return parts


def arcs(rng, ink, accent, paper):
    cx, cy = ((-40, 840), (1240, 840), (-40, -40), (1240, -40))[rng.pick(4)]
    marked = rng.pick(4)
    parts = ['<g clip-path="url(#plate)">']
    for index in range(4):
        color = accent if index == marked else ink
        width = 32 if index == marked else 4
        parts.append(
            f'<circle cx="{cx}" cy="{cy}" r="{190 + index * 145}" stroke="{color}" stroke-width="{width}"/>'
        )
    parts.append("</g>")
    return parts


def split(rng, ink, accent, paper):
    x = rng.between(480, 720)
    y = rng.between(240, 540)
    return [
        f'<rect x="{x}" width="{1200 - x}" height="800" fill="{accent}" opacity=".18"/>',
        f'<rect x="{x - 8}" width="16" height="800" fill="{ink}"/>',
        f'<circle cx="{x}" cy="{y}" r="{rng.between(46, 78)}" fill="{accent}"/>',
    ]


def frame(rng, ink, accent, paper):
    x = rng.between(240, 420)
    y = rng.between(180, 280)
    return [
        f'<rect x="170" y="130" width="860" height="540" rx="36" stroke="{ink}" stroke-width="4"/>',
        f'<rect x="{x}" y="{y}" width="{rng.between(240, 400)}" height="{rng.between(160, 260)}" rx="22" fill="{accent}"/>',
    ]


def ruler(rng, ink, accent, paper):
    y = rng.between(340, 470)
    count = rng.between(14, 20)
    marked = rng.pick(count)
    parts = [f'<path d="M180 {y} H1020" stroke="{ink}" stroke-width="3"/>']
    for index in range(count):
        x = 200 + index * (800 // (count - 1))
        if index == marked:
            parts.append(f'<rect x="{x - 10}" y="{y - 72}" width="20" height="144" rx="10" fill="{accent}"/>')
        else:
            height = 48 if index % 4 == 0 else 24
            parts.append(f'<path d="M{x} {y - height} V{y + height}" stroke="{ink}" stroke-width="3"/>')
    return parts


def moon(rng, ink, accent, paper):
    cx, cy = rng.between(500, 720), rng.between(320, 480)
    radius = rng.between(140, 200)
    direction = 1 if rng.pick(2) else -1
    return [
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{accent}"/>',
        f'<circle cx="{cx + direction * rng.between(70, 120)}" cy="{cy - rng.between(8, 40)}" r="{radius - rng.between(24, 56)}" fill="{paper}"/>',
    ]


def target(rng, ink, accent, paper):
    cx, cy = rng.between(500, 700), rng.between(340, 470)
    radii = (200, 132, 68)
    marked = rng.pick(3)
    parts = []
    for index, radius in enumerate(radii):
        if index == marked:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="{accent}"/>')
        else:
            parts.append(f'<circle cx="{cx}" cy="{cy}" r="{radius}" stroke="{ink}" stroke-width="4"/>')
    return parts


def steps(rng, ink, accent, paper):
    count = rng.between(5, 7)
    marked = rng.pick(count)
    width, gap = 86, 16
    left = (1200 - (count * width + (count - 1) * gap)) // 2
    parts = []
    for index in range(count):
        height = 90 + index * rng.between(42, 68)
        color = accent if index == marked else ink
        x = left + index * (width + gap)
        parts.append(f'<rect x="{x}" y="{680 - height}" width="{width}" height="{height}" fill="{color}"/>')
    return parts


def cells(rng, ink, accent, paper):
    columns, rows = 4, 3
    width, height, gap = 150, 128, 22
    left = (1200 - (columns * width + (columns - 1) * gap)) // 2
    top = (800 - (rows * height + (rows - 1) * gap)) // 2
    marked = rng.pick(columns * rows)
    parts = []
    index = 0
    for row in range(rows):
        for column in range(columns):
            x = left + column * (width + gap)
            y = top + row * (height + gap)
            if index == marked:
                parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="18" fill="{accent}"/>')
            else:
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="18" stroke="{ink}" stroke-width="4"/>'
                )
            index += 1
    return parts


def orbit(rng, ink, accent, paper):
    cx, cy = rng.between(500, 700), rng.between(340, 470)
    radius = rng.between(150, 220)
    count = rng.between(6, 10)
    marked = rng.pick(count)
    parts = [f'<circle cx="{cx}" cy="{cy}" r="{radius}" stroke="{ink}" stroke-width="3"/>']
    for index in range(count):
        angle = -math.pi / 2 + index * (2 * math.pi / count)
        x = cx + int(radius * math.cos(angle))
        y = cy + int(radius * math.sin(angle))
        if index == marked:
            parts.append(f'<circle cx="{x}" cy="{y}" r="16" fill="{accent}"/>')
        else:
            parts.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{ink}"/>')
    return parts


def cluster(rng, ink, accent, paper):
    cx, cy = rng.between(500, 700), rng.between(360, 460)
    marked = rng.pick(3)
    offsets = (
        (-rng.between(80, 140), -rng.between(20, 70)),
        (rng.between(50, 130), rng.between(10, 60)),
        (rng.between(-30, 40), rng.between(70, 130)),
    )
    parts = []
    for index, (dx, dy) in enumerate(offsets):
        color = accent if index == marked else ink
        parts.append(f'<circle cx="{cx + dx}" cy="{cy + dy}" r="{rng.between(72, 118)}" fill="{color}"/>')
    return parts


def horizon(rng, ink, accent, paper):
    cx = rng.between(460, 740)
    y = rng.between(430, 540)
    radius = rng.between(120, 190)
    return [
        f'<path d="M{cx - radius} {y} A{radius} {radius} 0 0 1 {cx + radius} {y} Z" fill="{accent}"/>',
        f'<path d="M180 {y} H1020" stroke="{ink}" stroke-width="4"/>',
    ]


def echo(rng, ink, accent, paper):
    x, y = rng.between(280, 440), rng.between(190, 280)
    width, height = rng.between(360, 500), rng.between(220, 320)
    dx, dy = rng.between(40, 78), rng.between(36, 68)
    return [
        f'<rect x="{x + dx}" y="{y + dy}" width="{width}" height="{height}" rx="28" stroke="{ink}" stroke-width="4"/>',
        f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="28" fill="{accent}"/>',
    ]


def plus(rng, ink, accent, paper):
    cx, cy = rng.between(500, 700), rng.between(340, 470)
    arm = rng.between(170, 260)
    thickness = 34
    return [
        f'<rect x="{cx - arm}" y="{cy - thickness // 2}" width="{arm * 2}" height="{thickness}" fill="{ink}"/>',
        f'<rect x="{cx - thickness // 2}" y="{cy - arm}" width="{thickness}" height="{arm * 2}" fill="{ink}"/>',
        f'<circle cx="{cx}" cy="{cy}" r="20" fill="{accent}"/>',
    ]


def ladder(rng, ink, accent, paper):
    left = rng.between(430, 520)
    right = left + rng.between(180, 280)
    top = rng.between(150, 200)
    count = rng.between(4, 6)
    marked = rng.pick(count)
    gap = 460 // count
    parts = [
        f'<path d="M{left} {top} V{top + 500}" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>',
        f'<path d="M{right} {top} V{top + 500}" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>',
    ]
    for index in range(count):
        y = top + 36 + index * gap
        if index == marked:
            parts.append(f'<rect x="{left}" y="{y - 6}" width="{right - left}" height="16" fill="{accent}"/>')
        else:
            parts.append(f'<path d="M{left} {y} H{right}" stroke="{ink}" stroke-width="4"/>')
    return parts


def peak(rng, ink, accent, paper):
    cx = rng.between(480, 720)
    base = rng.between(520, 640)
    half = rng.between(170, 270)
    rise = rng.between(200, 320)
    return [
        f'<path d="M{cx - half} {base} L{cx} {base - rise} L{cx + half} {base} Z" fill="{accent}"/>',
        f'<path d="M180 {base} H1020" stroke="{ink}" stroke-width="3"/>',
    ]


def ring(rng, ink, accent, paper):
    cx, cy = rng.between(500, 700), rng.between(340, 470)
    radius = rng.between(120, 180)
    return [
        f'<circle cx="{cx}" cy="{cy}" r="{radius}" stroke="{accent}" stroke-width="{rng.between(28, 52)}"/>',
        f'<circle cx="{cx + rng.between(-24, 24)}" cy="{cy}" r="{rng.between(16, 32)}" fill="{ink}"/>',
    ]


def windows(rng, ink, accent, paper):
    width, height, gap = 230, 190, 26
    left = (1200 - (2 * width + gap)) // 2 + rng.between(-40, 40)
    top = (800 - (2 * height + gap)) // 2 + rng.between(-30, 30)
    marked = rng.pick(4)
    parts = []
    index = 0
    for row in range(2):
        for column in range(2):
            x = left + column * (width + gap)
            y = top + row * (height + gap)
            if index == marked:
                parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="20" fill="{accent}"/>')
            else:
                parts.append(
                    f'<rect x="{x}" y="{y}" width="{width}" height="{height}" rx="20" stroke="{ink}" stroke-width="4"/>'
                )
            index += 1
    return parts


def chevron(rng, ink, accent, paper):
    count = rng.between(3, 5)
    marked = rng.pick(count)
    y = rng.between(170, 230)
    parts = []
    for index in range(count):
        color = accent if index == marked else ink
        width = 16 if index == marked else 4
        parts.append(
            f'<path d="M300 {y} L600 {y + 86} L900 {y}" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
        )
        y += rng.between(88, 112)
    return parts


def barcode(rng, ink, accent, paper):
    count = rng.between(10, 16)
    marked = rng.pick(count)
    x = rng.between(250, 360)
    parts = []
    for index in range(count):
        width = rng.between(22, 40) if index == marked else rng.between(8, 26)
        height = rng.between(260, 460)
        color = accent if index == marked else ink
        y = (800 - height) // 2
        parts.append(f'<rect x="{x}" y="{y}" width="{width}" height="{height}" fill="{color}"/>')
        x += width + rng.between(10, 20)
        if x > 960:
            break
    return parts


def spokes(rng, ink, accent, paper):
    cx, cy = rng.between(500, 700), rng.between(340, 470)
    radius = rng.between(150, 220)
    count = rng.between(6, 12)
    marked = rng.pick(count)
    parts = []
    for index in range(count):
        angle = index * (2 * math.pi / count)
        x = cx + int(radius * math.cos(angle))
        y = cy + int(radius * math.sin(angle))
        color = accent if index == marked else ink
        width = 8 if index == marked else 3
        parts.append(
            f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>'
        )
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="16" fill="{accent}"/>')
    return parts


def stack(rng, ink, accent, paper):
    count = rng.between(3, 4)
    marked = rng.pick(count)
    width = rng.between(440, 600)
    height = rng.between(78, 108)
    x = (1200 - width) // 2 + rng.between(-30, 30)
    y = rng.between(170, 230)
    shift = rng.between(26, 46)
    parts = []
    for index in range(count):
        color = accent if index == marked else ink
        parts.append(
            f'<rect x="{x + index * shift}" y="{y}" width="{width}" height="{height}" rx="18" fill="{color}"/>'
        )
        y += height + rng.between(22, 36)
    return parts


def slash(rng, ink, accent, paper):
    if rng.pick(2):
        x1, y1, x2, y2 = 240, 190, 960, 630
    else:
        x1, y1, x2, y2 = 240, 630, 960, 190
    span = rng.between(36, 64) / 100
    cx = int(x1 + (x2 - x1) * span)
    cy = int(y1 + (y2 - y1) * span)
    return [
        f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{ink}" stroke-width="24" stroke-linecap="round"/>',
        f'<circle cx="{cx}" cy="{cy}" r="20" fill="{accent}"/>',
    ]


def blocks(rng, ink, accent, paper):
    count = rng.between(3, 4)
    marked = rng.pick(count)
    size = rng.between(140, 180)
    gap = rng.between(26, 44)
    left = (1200 - (count * size + (count - 1) * gap)) // 2
    y = (800 - size) // 2 + rng.between(-36, 36)
    parts = []
    for index in range(count):
        color = accent if index == marked else ink
        x = left + index * (size + gap)
        parts.append(f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="16" fill="{color}"/>')
    return parts


grounds = (
    ground_clear,
    ground_vsplit,
    ground_band,
    ground_corner,
    ground_diagonal,
    ground_dots,
    ground_frame,
    ground_rules,
)
figures = (
    disc,
    queue,
    columns,
    graph,
    arcs,
    split,
    frame,
    ruler,
    moon,
    target,
    steps,
    cells,
    orbit,
    cluster,
    horizon,
    echo,
    plus,
    ladder,
    peak,
    ring,
    windows,
    chevron,
    barcode,
    spokes,
    stack,
    slash,
    blocks,
)


def compose(title, topic):
    paper, ink, accent = families.get(topic, plain)
    rng = Rng(f"{topic}\n{title}")
    ground = grounds[rng.pick(len(grounds))]
    figure = figures[rng.pick(len(figures))]
    parts = ground(rng, ink, accent, paper) + figure(rng, ink, accent, paper)
    body = "\n".join(parts)
    svg = (
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" fill="none">'
        '<defs><clipPath id="plate"><rect width="1200" height="800"/></clipPath></defs>'
        f'<rect width="1200" height="800" fill="{paper}"/>\n{body}\n</svg>\n'
    )
    return svg, f"{ground.__name__[7:]}+{figure.__name__}"


def cover_svg(title, topic):
    return compose(title, topic)[0]


def slug_for(path):
    match = date_prefix.match(path.stem)
    if not match:
        sys.exit(f"{path.name}: filename must start with YYYY-MM-DD-")
    return match.group(1)


def write_note(path):
    path = pathlib.Path(path)
    front = read_front(path.read_text())
    title = front.get("title") or slug_for(path)
    svg, _pair = compose(title, front.get("topic", ""))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / f"{slug_for(path)}.svg"
    target.write_text(svg)
    return target


def main():
    if len(sys.argv) > 2:
        sys.exit("usage: python3 scripts/note_images.py [note.md]")
    posts = [pathlib.Path(sys.argv[1])] if len(sys.argv) == 2 else sorted((root / "_posts").glob("*.md"))
    if not posts:
        sys.exit("no notes")
    pairs = set()
    for path in posts:
        front = read_front(path.read_text())
        title = front.get("title") or slug_for(path)
        _svg, pair = compose(title, front.get("topic", ""))
        pairs.add(pair)
        write_note(path)
    print(f"wrote {len(posts)} cover(s), {len(pairs)} combinations, to public/images/notes/")


if __name__ == "__main__":
    main()
