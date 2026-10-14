PARTH DAKE PORTFOLIO — HOW TO PUT IT ONLINE WITH NETLIFY
==========================================================

You only need ONE thing to publish the website:

    the folder you get when you unzip  "Parth-Portfolio-Netlify-Upload.zip"

It is a ready-to-publish website. Nothing needs to be installed or built.
(The other ZIP, "Parth-Portfolio-Source-Project", is only for making changes
later. You do NOT upload that one.)


1. UNZIP FIRST
--------------
Double-click "Parth-Portfolio-Netlify-Upload.zip"
(on Windows: right-click > Extract All).
You get a folder called "Parth-Portfolio-Netlify-Upload". Open it: you should
see index.html, 404.html and folders like images, amin, ica. That folder is
your website. Netlify needs this unzipped folder, not the ZIP file.


2. MAKE A NETLIFY ACCOUNT (skip if you already have one)
-------------------------------------------------------
- Go to https://app.netlify.com/signup
- Sign up with your email, Google or GitHub account. The free plan is enough.


3. PUBLISH THE WEBSITE (first time)
-----------------------------------
- Go to https://app.netlify.com/drop
- Drag the whole "Parth-Portfolio-Netlify-Upload" folder onto the page
  (the folder itself, not the files inside it, and not the ZIP).
- Wait until the upload finishes (about a minute). Netlify shows
  "Your project is deployed" with a link.


4. GET YOUR PUBLIC LINK
-----------------------
- The link looks like https://something-random-123.netlify.app
- To get a nicer name: open your project in Netlify, then
  Project configuration > General > Project details > Change project name.
  For example "parth-dake" gives https://parth-dake.netlify.app
- That link is what you send to clients and recruiters.


5. UPDATE THE WEBSITE LATER (same link stays)
---------------------------------------------
- Open your project in Netlify and click the "Deploys" tab.
- Drag the NEW "Parth-Portfolio-Netlify-Upload" folder onto the box that says
  "Drag and drop your project output folder here".
- The new version replaces the old one. Your link does not change.

  Important: always upload the whole folder again. Do not try to edit
  files inside a ZIP. To change a single file (for example a prototype),
  replace that file inside the unzipped folder, then drag the whole folder.


GOOD TO KNOW
------------
- Upload folder vs source code: the upload folder is finished website files,
  so Netlify publishes it as-is with no build step. The Source Project contains
  the editable files and scripts that PRODUCE the upload folder; uploading it to
  Netlify would not work.
- The site uses Google Fonts (the Inter typeface). It loads automatically
  online, so nothing to set up.
- The AMIN Worldwide prototype shows country flags from flagcdn.com, a free
  public image service. It also loads automatically online.
- If someone opens a link that doesn't exist, they see a "Page not found" page
  with a button back to the portfolio.
- Each case study has its own link you can share, for example
  https://your-name.netlify.app/#ica  or  /#tatapower  /#amin  /#anchor
  /#ultratech  /#ellenbarrie
