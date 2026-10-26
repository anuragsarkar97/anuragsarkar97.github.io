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
| Shared CSS | 32,659 bytes | 7,106 bytes |
| Shared UI source | 47,666 bytes | 16,895 bytes |
| Homepage HTML | 13,308 bytes | 3,802 bytes |

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

## Markdown editor
The `/editor/` page, linked as Write in the footer, has title, publication date,
optional description and a Markdown text area. One current draft is saved in
localStorage on this browser/origin. Downloads contain escaped Jekyll front matter
and a dated slug filename. No backend or publish API was added; preview and direct saving are described below.
Editor JavaScript only loads on this route; the page is noindex and does not load
analytics. Browser storage is convenience, not a backup: download a copy to keep.

Verified `node scripts/check_editor.js`, a 13-page production build and local-link
checks. Chrome tests covered required/whitespace validation, reload restoration,
Unicode/quoted metadata, correct downloaded filename and body, blocked storage
with working downloads, and four mobile/desktop light/dark axe checks with no
violations. Desktop/mobile screenshots were inspected. The actual downloaded
file was built in a temporary site with seven articles; metadata, syntax
highlighting, index, feed and sitemap checks passed. No test article was added
to the real repository. Publishing remains the normal `_posts/` + GitHub flow.

## Direct saving and live preview
Added native folder selection with read/write access to the selected `_posts/`
folder, confirmed replacement of existing files, handling for cancelled pickers,
wrong folders, denied access and aborted writes. The chosen handle stays in
memory for this page session. Download remains the unsupported-browser fallback.
The live preview uses locally vendored Marked 18.1.1 in an opaque-origin iframe
with scripts disabled and a restrictive CSP. It shares the blog's reading styles.
Markdown and preview are adjacent above 800px and stack below that width.

Verified unit checks for folder reuse, successful writes, overwrite acceptance
and refusal, wrong folders, cancellation, permission errors and write abort.
Chrome integration exercised Markdown headings, lists, links, code and tables;
a mocked folder picker drove the actual save button and wrote the resulting
file to a temporary `_posts/` directory through a test binding. Native directory
picker interaction and permissions were not automated. Four editor responsive/
theme/axe checks passed with zero violations; script injection could not affect
the parent page, and unsupported-folder-API messaging was verified. Production
build and local links passed. Desktop and mobile screenshots were inspected.
No repository article was created by these tests.
