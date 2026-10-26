# AStellarSite
My static portfolio website. Pending.

## Building

The pages are generated, not hand-written. `build_pages.py` is the whole
pipeline: it holds the site's source (copy, data, templates, and the Atlas
map generator) and writes the HTML pages in this repo. Run it from this
directory:

    python3 build_pages.py

`make_resume_pdf.py` builds `resume.pdf` from the same resume content
(requires fpdf2). GitHub Pages serves the committed files as-is; there is
no build step on GitHub's side, so regenerate and commit the output with
any source change. (reading.html is a hand-kept redirect stub and is not
generated.)
