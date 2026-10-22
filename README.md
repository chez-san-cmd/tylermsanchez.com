# tylermsanchez.com

Tyler Sanchez's personal site. Plain HTML, no build step, hosted on GitHub Pages.

- `index.html` home
- `writing/` essays
- `how-i-work.html` principles, system diagrams, tools
- `projects.html` and `projects/` one page per project
- `reading.html` (Year in review is parked for v1; `PUBLISH_YEARS` in build.py)

Drafts live in Notion; this repo holds what is published. Pushes to `main` deploy.

## Editing

All page copy, the shared nav and the CSS live in `_build/build.py`; the diagrams in `_build/how-i-work-diagrams.html`.
Edit there, run `python3 _build/build.py` from the repo root to regenerate the HTML, commit, push.
(Editing the generated HTML directly works too, but is overwritten by the next build.)
For the private preview artifact, run with `ARTIFACT_PREVIEW=1 SITE_OUT=<dir>` and publish that folder.

## Style rules

- **Project names are proper nouns.** Capitalize every word: Command Center, Job Radar, Concert Radar,
  Purchase Advisor, What's for Dinner. New projects follow the same rule. The build fails if a name in
  `PROJECTS` isn't title case or if a project name appears in lowercase anywhere on the site.
- Links in body text are underlined; nav, contact row and book titles underline on hover.
