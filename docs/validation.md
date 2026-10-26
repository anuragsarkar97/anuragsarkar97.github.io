# Plain blog — validation, October 26, 2026

## Final design
A narrow column of ordinary text on white. The homepage has the author's name,
About, and six underlined article titles with dates. No introductory section,
excerpts, ornamental rules, accent colors, margin dates, or special index grid.
Papershelf and the drawing tool remain accessible from the footer. Article pages
keep a readable Georgia text column, native links, code highlighting, keyboard
scroll regions and dark mode. Article descriptions remain in source and metadata.

## Scope and measurements
Jekyll 3.10.0 is retained. No browser libraries or font downloads were added.
The original four stylesheets were consolidated into layout/type and syntax CSS.
The portfolio hero, skills cards, broken game promotions, hidden navigation,
disabled pagination/plugin, Tailwind CDN and web fonts were removed.

| Uncompressed file size | Original Git HEAD | Final working tree |
| --- | ---: | ---: |
| Shared CSS | 32,659 bytes | 6,419 bytes |
| Shared UI source | 47,666 bytes | 13,456 bytes |
| Homepage HTML | 13,308 bytes | 3,760 bytes |

Shared UI means includes, layouts, both indexes, CSS and JavaScript. It excludes
content, the standalone drawing app, build tooling and documentation. These are
file-size measurements; field Core Web Vitals were not measured.

## Verification
- Production Jekyll build with strict front matter passed on Ruby 4.0.6.
- `scripts/check_site.rb`: 12 HTML pages, six articles, local links and anchors,
  canonical URLs, metadata, JSON-LD, Atom XML and sitemap passed.
- All original published HTML output paths are preserved.
- Six article sources and the drawing application are byte-for-byte unchanged.
- Browser comparisons confirm article text, media URLs and heading IDs remain
  unchanged, as do all 24 paper descriptions and bibliographic details.
- Chrome rendered 11 reading routes at 320/390/768/1440px in light and dark:
  88 combinations, one H1 per page, no viewport horizontal overflow.
- Axe ran on all reading routes in desktop/light and mobile/dark: 22 runs,
  zero reported WCAG 2/2.1 A/AA violations. This is automated coverage,
  not a complete conformance certification.
- Keyboard skip link, scrollable code, no-JavaScript navigation, remembered and
  system themes, explicit preference overrides and blocked storage were checked.
- Temporary browser-only image/table fixtures verified responsive media and
  horizontal table scrolling. No fixture content is published.
- Desktop and mobile homepage and article screenshots were inspected.
- JavaScript syntax and `git diff --check` passed.

## Evidence
[Desktop](screenshots/home-desktop.png) · [Mobile](screenshots/home-mobile.png) ·
[Article](screenshots/article-desktop-viewport.png) ·
[Dark mobile article](screenshots/code-mobile-viewport.png) ·
[Browser results](browser-results.json)

## Limitations
External resources were blocked during deterministic checks: analytics, Giphy,
and baseline Tailwind/fonts. Baseline `tailwind is not defined` errors in the
report are caused by that block; redesigned pages have no JavaScript exceptions.
Media playback, analytics delivery, external paper URLs and drawing-library
availability were not verified. The drawing tool was preserved intact and is
excluded from reading-page axe checks. Physical devices, Firefox, Safari and
production hosting were not tested. No deploy, commit or push was performed.

## Major implementation files
`index.html`, `blog/index.html`, `_includes/article-list.html`, shared layouts,
`public/css/style.css`, `public/css/syntax.css`, `public/js/script.js`,
`papershelf.md`, head metadata, Atom/sitemap/robots, Jekyll build manifest and
`scripts/check_site.rb`. The old sidebar include and three obsolete theme
stylesheets were deleted. `README.md` documents authoring and local builds.
