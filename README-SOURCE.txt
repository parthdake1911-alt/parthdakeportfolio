PARTH DAKE PORTFOLIO — SOURCE PROJECT
=====================================

This folder holds the editable files that produce the website.
You don't need it to publish (use the Netlify upload ZIP for that). Keep it safe
for future changes, and give it to Claude or a developer when you want edits.


WHERE THINGS ARE
----------------
template.html            the homepage (hero, project cards, About, Contact)
cards/                   homepage images: project covers, portrait, logo
logos/                   client logos shown at the top of each case study
intro.mp4 / intro.webm   the hero video
resume/                  your original résumé PDF
amin/ anchor/ ultra/ ellen/ ica/ tata/
                         one folder per case study:
                           body.html   = the case-study text and layout
                           extra.css   = its styles
                           out/        = its screenshots
                           src/        = the original prototype file
anchor/base_style.css, base_script.js
                         shared look and behaviour of all case-study pages
vendor/                  jQuery (used by two prototypes), kept locally


REBUILDING THE WEBSITE AFTER A CHANGE
-------------------------------------
Rebuilding needs Python 3 with Pillow and pikepdf installed, plus ffmpeg.
Optional: the "html-minifier-terser" tool for slightly smaller pages.

    python3 build_all.py

This recreates the "site" folder, which is exactly what goes into the
upload folder (the Netlify upload ZIP has the same files). Then upload it as described in README.txt.
(make_packages.py recreates the two ZIP files.)

What the build does, in order:
  1. builds each case-study page from body.html + extra.css
  2. optimize_media.py      - AVIF/WebP images, video poster, smaller résumé
     optimize_prototypes.py - lighter copies of the prototypes
                              (originals in src/ are never changed)
  3. build_site.py          - assembles the site, adds image sizes,
                              404 page, caching rules, minifies pages
  4. build_preview.py       - a single-file offline preview


SIMPLE CHANGES WITHOUT REBUILDING
---------------------------------
- Replace your résumé: put the new PDF in the unzipped upload folder, inside "resume", with the
  same name, Parth-Dake-Resume.pdf, and upload the folder again.
- Replace a prototype: put the new file in that case study's folder inside
  the unzipped upload folder with the same name, prototype.html, and upload the folder.
  (Rebuilding later also re-optimizes it, if you copy it into src/ as well.)
