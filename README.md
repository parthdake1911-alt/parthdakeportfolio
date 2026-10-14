# Parth Dake — Portfolio

UI/UX design portfolio: animated homepage plus case studies for Tata Power (Customer Smile), ICA, Ellenbarrie, UltraTech Cement, AMIN Worldwide and Anchor.

## What's where
- **`site/`** — the finished website. This is what gets published (it has `index.html` at the top).
- **`template.html`** — the homepage source.
- **`amin/ anchor/ ultra/ ellen/ ica/ tata/`** — case-study sources (`body.html`, `extra.css`, screenshots in `out/`, original prototypes in `src/`).
- **`cards/`, `logos/`, `resume/`** — homepage images, client logos, résumé.
- **`build_all.py`** — rebuilds `site/` from the sources (see `README-SOURCE.txt`).

## Publishing on Netlify
`netlify.toml` tells Netlify to publish the `site` folder with no build step.
In Netlify: **Add new project → Import an existing project → GitHub → this repository**. Every push to `main` then updates the live site.
(Drag-and-drop of the `site` folder still works too — see `README.txt`.)
