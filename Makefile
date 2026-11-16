# Review and publish notes. `make` prints targets. It does not publish.
# Publish builds into a temp directory so a running preview keeps _site.

.PHONY: help new preview css images review publish

TITLE ?=
MSG ?= Publish notes
HOST ?= 127.0.0.1
PORT ?= 4000

PUBLISH_PATHS = \
	_posts _layouts _includes _config.yml index.html 404.md \
	public src/app.css scripts docs Makefile AGENT.md \
	package.json package-lock.json Gemfile Gemfile.lock \
	README.md robots.txt sitemap.xml LICENSE.md .gitignore

help:
	@printf '%s\n' \
		'make new TITLE="Note title"   create _posts/YYYY-MM-DD-slug.md and its cover' \
		'make preview                   serve http://$(HOST):$(PORT)' \
		'make css                       rebuild public/css/app.css' \
		'make images                    rewrite every cover SVG' \
		'make review                    check notes, then a production build' \
		'make publish MSG="..."         review, commit the publication files, push origin'

new:
	@test -n "$(TITLE)" || { echo 'usage: make new TITLE="Note title"'; exit 1; }
	python3 scripts/new_note.py "$(TITLE)"

preview:
	bundle exec jekyll serve --host $(HOST) --port $(PORT) --watch

css:
	npm run css

images:
	python3 scripts/note_images.py

review:
	python3 scripts/check_notes.py
	python3 scripts/review_notes.py
	@dest=$$(mktemp -d /tmp/anurag-site.XXXXXX); \
	set +e; \
	JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter --destination "$$dest"; \
	build=$$?; \
	if [ $$build -eq 0 ]; then ruby scripts/check_site.rb "$$dest"; build=$$?; fi; \
	rm -rf "$$dest"; \
	exit $$build

publish: review
	git add -A -- $(PUBLISH_PATHS)
	git diff --cached --quiet || git commit -m "$(MSG)"
	git push origin HEAD
