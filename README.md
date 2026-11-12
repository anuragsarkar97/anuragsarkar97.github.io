# Anurag Sarkar’s blog

A static Jekyll publication. The site serves prebuilt CSS, self-hosted fonts, and small browser libraries from `public/`.

## Run locally

Use Ruby 4.0.6 (the version in `.ruby-version`) and Bundler:

```sh
bundle install
npm ci
npm run css
bundle exec jekyll serve
```

Open http://localhost:4000. Production build and validation:

```sh
JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter
bundle exec ruby scripts/check_site.rb _site
python3 scripts/check_notes.py
```

## Write a note

```sh
python3 scripts/new_note.py "Title of the note"
python3 scripts/check_notes.py
```

`new_note.py` writes `_posts/YYYY-MM-DD-title.md` from `docs/note-template.md`. Open with the problem, then Example, Determinations, Open questions, and External references. `check_notes.py` fails when a note drops that shape. Both scripts use the Python standard library.

Add the file, then build and publish through the usual GitHub workflow. Future-dated posts need a rebuild on or after their date. You can also add `_posts/YYYY-MM-DD-slug.md` by hand with `layout: post`, `title`, `dem`, and `style: rfd`. The date in the filename is the publication date, and the URL is `/YYYY/MM/DD/slug/`. Keep the filename once a note is published. Set optional `emoji` to a GitHub emoji shortcode without colons, such as `lock`. Add its PNG to `public/emoji/` using the shortcode as the filename. Notes default to `memo`. Use a language name on code fences and `##` for sections.

## Structure

- `_layouts/`: shared shell, article and content page.
- `_includes/article-list.html`: the list on the home page.
- `src/app.css`: Tailwind and daisyUI. `npm run css` writes `public/css/app.css`.
- `public/js/script.js`: wires List.js search, Tocbot outlines, and AnchorJS heading permalinks.
- `public/fonts/` and `public/vendor/`: self-hosted assets and licenses, refreshed by `npm run css`.
- `docs/note-template.md`: the shape of a new note.
- `sitemap.xml`, `robots.txt`: discovery.

The archive and articles render without JavaScript. Search and the article outline require JavaScript. Commit the generated CSS and assets when changing the reader. GitHub Pages builds this repository
with its existing Jekyll engine. The original theme’s MIT license remains in `LICENSE.md`.
