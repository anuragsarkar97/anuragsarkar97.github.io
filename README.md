# Anurag Sarkar’s blog

A static Jekyll publication. No frontend build, browser CSS compiler or web fonts.

## Run locally

Use Ruby 4.0.6 (the version in `.ruby-version`) and Bundler:

```sh
bundle install
bundle exec jekyll serve
```

Open http://localhost:4000. Production build and validation:

```sh
JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter
bundle exec ruby scripts/check_site.rb _site
node scripts/check_editor.js
```

## Publish an article

Open `/editor/` (the **Write** footer link). Write Markdown on the left and see
its rendered preview on the right; narrow screens stack the two panes.
Click **Save to posts folder** and choose this repository's `_posts/` directory.
The chosen folder is reused until the page reloads. Existing filenames require
confirmation before replacement. This uses the browser's File System Access API;
unsupported browsers retain **Download Markdown** as a fallback.

Save does not commit, push or publish. Build and publish through the usual GitHub
workflow after saving. Future-dated posts need a rebuild on/after their date.
One current draft is saved in this browser only; save a file before clearing
browser data or switching browsers. The sandboxed preview supports Markdown;
Jekyll/Liquid processing and server syntax highlighting happen at build time.

Alternatively, add `_posts/YYYY-MM-DD-slug.md` with `layout: post`, `title` and `dem` (the search description). Dates come from the filename. Existing URLs
use `/YYYY/MM/DD/slug/`; keep filenames stable to preserve incoming links.
Use language-labelled fences for code, ordinary paragraphs for prose, and H2
for article sections. Existing article sources are preserved; the post layout
normalizes legacy H1 sections and leaves their anchor IDs intact.

## Structure

- `_layouts/`: shared shell, article and content page.
- `_includes/article-list.html`: both homepage and existing `/blog/` archive.
- `public/css/style.css`: layout, typography, light/dark palettes, bibliography.
- `public/css/syntax.css`: server-rendered Rouge syntax highlighting.
- `public/js/script.js`: optional theme preference and keyboard scroll regions.
- `editor/index.html`, `public/js/editor.js`: browser draft, sandboxed preview and Markdown file saving.
- `papershelf.md`: research bibliography; `excalidraw.html`: independent drawing tool.
- `atom.xml`, `sitemap.xml`, `robots.txt`: discovery and syndication.

The theme follows the operating system unless changed with the footer button.
Reading and navigation work without JavaScript. Analytics is configured by
`google_analytics_id` in `_config.yml`. GitHub Pages can build this repository
with its existing Jekyll engine; no deployment settings were changed.

See [the audit and plan](docs/redesign.md) and [validation results](docs/validation.md).
The original theme’s MIT license remains in `LICENSE.md`.

The editor vendors Marked 18.1.1 under `public/js/vendor/` with its license. It
loads only on the editor page; the reading pages do not load a Markdown parser.
