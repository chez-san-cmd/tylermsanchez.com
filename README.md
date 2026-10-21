# tylermsanchez.com

Tyler Sanchez's personal site. Plain HTML, no build step, hosted on GitHub Pages.

- `index.html` home
- `writing/` essays
- `how-i-work.html` principles, system diagrams, tools
- `reading.html`, `years-in-review.html`

Drafts live in Notion; this repo holds what is published. Pushes to `main` deploy.

## Editing

All page copy, the shared nav and the CSS live in `_build/build.py`; the diagrams in `_build/how-i-work-diagrams.html`.
Edit there, run `python3 _build/build.py` from the repo root to regenerate the HTML, commit, push.
(Editing the generated HTML directly works too, but is overwritten by the next build.)
For the private preview artifact, run with `ARTIFACT_PREVIEW=1 SITE_OUT=<dir>` and publish that folder.
