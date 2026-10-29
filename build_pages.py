#!/usr/bin/env python3
"""Generate the multi-page AStellarSite from shared partials.
Extracts the resume section, photography section, and both scripts verbatim
from the current single-page index.html, then rebuilds every page."""
import re, os, zlib

SITE = os.path.expanduser("~/workspace/astellarsite")

def read_page(name):
    return open(os.path.join(SITE, name)).read()

def first_script(html):
    return re.findall(r"<script>(.*?)</script>", html, re.S)[0]

def section(html, sid):
    m = re.search(r'<section id="%s">.*?</section>' % sid, html, re.S)
    return m.group(0)

# Verbatim blocks live on their own pages since the multi-page split.
sky_js = first_script(read_page("index.html"))
gallery_js = first_script(read_page("photography.html"))
resume_section = section(read_page("resume.html"), "resume")
photo_section = section(read_page("photography.html"), "photography")

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Adam Laloge">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{og_image}">
<meta name="theme-color" content="#070b16">
{schema}<link rel="stylesheet" href="styles.css?v=69">
<link rel="alternate" type="application/rss+xml" title="Adam Laloge - Blog" href="https://adamlaloge.com/feed.xml">
</head>
<body>
"""

NAV_ITEMS = [
    ("index.html", "Home"),
    ("work.html", "Projects"),
    ("resume.html", "Resume"),
    ("about.html", "About"),
    ("photography.html", "Photography"),
    ("bookshelf.html", "Bookshelf"),
    ("blog.html", "Blog"),
    ("dreams.html", "Dreamscape"),
    ("latent-sitemap.html", "Atlas"),
]

def header(active):
    links = "\n      ".join(
        '<a href="%s"%s>%s</a>' % (href, ' class="active" aria-current="page"' if href == active else "", label)
        for href, label in NAV_ITEMS)
    return """<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="index.html">Adam Laloge</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-label="Menu">&#9776;</button>
    <nav id="site-nav">
      %s
    </nav>
  </div>
</header>
""" % links

FOOTER = """
<footer class="site-footer">
  <div class="wrap footer-inner">
    <span><strong>Adam Laloge</strong></span>
    <span class="footer-links"><a href="https://github.com/AStellarScene">GitHub</a> &middot; <a href="mailto:hello@adamlaloge.com">hello@adamlaloge.com</a></span>
  </div>
</footer>
"""

NAV_JS = """<script>
(function () {
  var btn = document.querySelector('.nav-toggle');
  var nav = document.getElementById('site-nav');
  if (!btn || !nav) return;
  btn.addEventListener('click', function () {
    var open = nav.classList.toggle('open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
})();
</script>
"""

def page(fname, title, desc, active, body, extra_js="", schema="", og_image="https://adamlaloge.com/art/obsidian-dragon.jpg"):
    url = "https://adamlaloge.com/" + ("" if fname == "index.html" else fname)
    html = (HEAD.format(title=title, desc=desc, url=url, schema=schema, og_image=og_image) + header(active)
            + '\n<main class="wrap">\n' + body + '\n</main>\n' + FOOTER
            + extra_js + NAV_JS + "\n</body>\n</html>\n")
    open(os.path.join(SITE, fname), "w").write(html)
    print("wrote", fname, len(html))

DESC = "Personal site of Adam Laloge: software projects, photography, and what I'm building lately."

PERSON_LD = """<script type="application/ld+json">
{"@context": "https://schema.org", "@type": "Person", "name": "Adam Laloge", "url": "https://adamlaloge.com/", "image": "https://adamlaloge.com/art/obsidian-dragon.jpg", "email": "mailto:hello@adamlaloge.com", "jobTitle": "Engineering Test Technician", "worksFor": {"@type": "Organization", "name": "Baxter International"}, "sameAs": ["https://github.com/AStellarScene"]}
</script>
"""

WORK_DESC = "Projects by Adam Laloge: BenchLab, Pace, Rotation, Slip, and Lucent Launcher \u2014 software built in the open, with an honest status line on each."
ABOUT_DESC = "About Adam Laloge: an engineering test technician in a medical-device lab who builds test software, is finishing a UX degree, photographs sunsets, and reads dark fantasy."
PROJ_DESCS = {
    "benchlab.html": "BenchLab, a testing simulator by Adam Laloge: a visual test builder, an in-browser simulated device, and traceability reports generated from the tests themselves.",
    "pace.html": "Pace, by Adam Laloge: a planner for self-paced degree programs. Enter your courses and a target finish date; get a week-by-week plan with an ahead-or-behind readout.",
    "rotation.html": "Rotation, by Adam Laloge: a five-day packed-lunch rotation as a tool \u2014 pick the week's meals and get the grocery list, checked against what you already have at home.",
    "slip.html": "Slip, by Adam Laloge: a pause before small purchases. Enter a price and how often it recurs; Slip translates it into days of delay on your savings targets. Local data only.",
    "lucent.html": "Lucent Launcher, by Adam Laloge: a native Minecraft launcher in Rust and GTK4, with a vendored core that installs Vanilla, Fabric, Quilt, Forge, and NeoForge.",
}

# ---------- Home ----------
home_body = """  <section class="hero">
    <canvas id="sky" aria-hidden="true"></canvas>
    <h1>Hi there</h1>
    <p class="intro">I like planning, building, and testing software. I'm finishing a UX degree. I photograph sunsets and read dark fantasy. Most of my work is internal and can't be shown, so I build in the open here: chasing digital experiences, taking new technologies to the maximum, creating science fiction in real life. That's my goal, anyway.</p>
    <div class="hero-links">
      <a class="pill pill-teal" href="resume.html">Resume &#8599;</a>
      <a class="pill pill-violet" href="latent-sitemap.html">Atlas &#8599;</a>
    </div>
  </section>

  <section id="work">
    <p class="label">Projects</p>
    <h2>Things I'm building</h2>
    <p class="section-note">Each one is labeled with where it actually stands. Nothing here is called finished before it is.</p>
    <div class="cards">
      <article class="card">
        <p class="label card-label">BenchLab</p>
        <p class="status">Now: In planning</p>
        <p>A testing simulator that runs in the browser. Build a test in a visual editor, run it against a simulated device, and get a traceability report.</p>
        <p><a class="card-link" href="benchlab.html">View project &#8599;</a></p>
      </article>
      <article class="card">
        <p class="label card-label">Pace</p>
        <p class="status">Now: In development</p>
        <p>A planner for self-paced degree programs, generalized from the system I run my own degree on. Courses and a finish date in; a week-by-week plan out.</p>
        <p><a class="card-link" href="pace.html">View project &#8599;</a></p>
      </article>
      <article class="card">
        <p class="label card-label">Rotation</p>
        <p class="status">Now: In development</p>
        <p>A five-day packed-lunch rotation, turned into a tool anyone can use. Pick the week's meals and get the grocery list, checked against what's already at home.</p>
        <p><a class="card-link" href="rotation.html">View project &#8599;</a></p>
      </article>
      <article class="card">
        <p class="label card-label">Slip</p>
        <p class="status">Now: Planned, not started</p>
        <p>A pause before small purchases. Enter a price and how often it recurs, and see it as days of delay on a savings target instead of dollars.</p>
        <p><a class="card-link" href="slip.html">View project &#8599;</a></p>
      </article>
      <article class="card">
        <p class="label card-label">Lucent Launcher</p>
        <p class="status">Now: In development</p>
        <p>A native Minecraft launcher in Rust and GTK4. Its vendored core installs Vanilla, Fabric, Quilt, Forge, and NeoForge, builds the launch command, and runs the game.</p>
        <p><a class="card-link" href="lucent.html">View project &#8599;</a></p>
      </article>
    </div>
  </section>

  <section id="about">
    <p class="label">About</p>
    <h2>About</h2>
    <p>I'm 22. I work as an engineering test technician at a medical-device lab in Batesville, Indiana, where most of my time goes to building test software. I'm also finishing a B.S. in UX Design at WGU.</p>
    <p><a href="about.html">More about me &#8599;</a></p>
  </section>

  <section id="photography">
    <p class="label">Photography</p>
    <h2>Off the clock</h2>
    <p><a href="photography.html"><img class="teaser-img" src="photos/sunset-grass.jpg" alt="Sunset over calm water, seen through silhouetted beach grass"></a></p>
    <p><a href="photography.html">See the photography &#8599;</a></p>
  </section>

  <section id="atlas">
    <p class="label">Atlas</p>
    <h2>The site, drawn as a galaxy</h2>
    <p>Every photo, book, world, and project here is a point of light in a living nebula, drifting near the things it belongs with &mdash; a sitemap built like latent space, and generated from the site itself.</p>
    <p><a href="latent-sitemap.html">Explore Atlas &#8599;</a></p>
  </section>

  <section id="contact">
    <p class="label">Contact</p>
    <h2>Get in touch</h2>
    <p>Code and public projects live on GitHub: <a href="https://github.com/AStellarScene">github.com/AStellarScene</a>. Email: <a href="mailto:hello@adamlaloge.com">hello@adamlaloge.com</a>.</p>
  </section>"""
page("index.html", "Adam Laloge", DESC, "index.html",
     home_body, "<script>" + sky_js + "</script>\n", schema=PERSON_LD, og_image="https://adamlaloge.com/photos/sunset-grass.jpg")

# ---------- Work index ----------
work_body = """  <section id="work">
    <p class="label">Projects</p>
    <h2>Things I'm building</h2>
    <p class="section-note">The status line is the part to trust. Descriptions say what each project is meant to do.</p>
    <div class="cards">
      <article class="card">
        <p class="label card-label">BenchLab</p>
        <p class="status">Now: In planning</p>
        <p>A testing simulator that runs in the browser. Build a test in a visual editor, run it against a simulated device, and get a traceability report. An agent layer turns plain-English test protocols into executable steps.</p>
        <p><a class="card-link" href="benchlab.html">View project &#8599;</a></p>
      </article>
      <article class="card">
        <p class="label card-label">Pace</p>
        <p class="status">Now: In development</p>
        <p>A planner for self-paced degree programs, built from the system I run my own degree on. Courses and a target finish date in; a week-by-week plan out. It only counts work that is actually finished.</p>
        <p><a class="card-link" href="pace.html">View project &#8599;</a></p>
      </article>
      <article class="card">
        <p class="label card-label">Rotation</p>
        <p class="status">Now: In development</p>
        <p>A five-day packed-lunch rotation, turned into a tool anyone can use. Pick the week's meals and get the grocery list, checked against what you already have at home.</p>
        <p><a class="card-link" href="rotation.html">View project &#8599;</a></p>
      </article>
      <article class="card">
        <p class="label card-label">Slip</p>
        <p class="status">Now: Planned, not started</p>
        <p>A pause before small purchases. Enter a price and how often it recurs, and see the cost as days of delay on a savings target. There is a 48-hour hold list for undecided items. Local data only, no bank connection.</p>
        <p><a class="card-link" href="slip.html">View project &#8599;</a></p>
      </article>
      <article class="card">
        <p class="label card-label">Lucent Launcher</p>
        <p class="status">Now: In development</p>
        <p>A native Minecraft launcher in Rust and GTK4. Its vendored core installs Vanilla, Fabric, Quilt, Forge, and NeoForge, builds the launch command, and runs the game.</p>
        <p><a class="card-link" href="lucent.html">View project &#8599;</a></p>
      </article>
    </div>
  </section>"""
page("work.html", "Projects — Adam Laloge", WORK_DESC, "work.html", work_body)

# ---------- Project pages ----------
def project(fname, name, status, paras, bullets=None):
    bl = ""
    if bullets:
        bl = "\n    <h3>What it does</h3>\n    <ul>\n" + "\n".join(
            "      <li>%s</li>" % b for b in bullets) + "\n    </ul>"
    body = """  <section>
    <p class="label">Projects</p>
    <h2>%s</h2>
    <p class="status">Now: %s</p>
%s%s
    <p><a href="work.html">&#8592; All projects</a></p>
  </section>""" % (name, status, "\n".join("    <p>%s</p>" % p for p in paras), bl)
    page(fname, "%s — Adam Laloge" % name, PROJ_DESCS.get(fname, DESC), "work.html", body)

project("benchlab.html", "BenchLab", "In planning",
    ["A testing simulator that runs in the browser. It's the public twin of the test-platform work I do at my job, rebuilt from scratch with nothing proprietary: the workflow is real, the device under test is simulated.",
     "I'm building it alongside my WGU prototyping courses. The first usability test is running now, and what it turns up decides what the next version changes."],
    ["Build a test in a visual editor, step by step",
     "Run it against a simulated device and watch it execute",
     "Get a traceability report tying each step to its requirement",
     "An agent layer turns plain-English protocols into executable test steps"])

project("pace.html", "Pace", "In development",
    ["A planner for self-paced degree programs. Enter your courses and a target finish date and get a week-by-week plan with an ahead-or-behind readout.",
     "Pace is generalized from the system I run my own WGU degree on: a fixed finish date, a weekly pace that has to hold, and no credit for work that hasn't happened yet."],
    ["Week-by-week plan from your course list and target date",
     "Ahead-or-behind readout based on what you have actually finished",
     "Replans when a course slips, instead of pretending it didn't"])

project("rotation.html", "Rotation", "In development",
    ["A five-day packed-lunch rotation, turned into a tool anyone can use. It's the rotation I'm adopting myself; Rotation is the version that doesn't live in my head.",
     "Pick the week's meals and get the grocery list for them, checked against what you already have at home so you don't buy a second bag of rice."],
    ["A five-day lunch rotation you can change to your own meals",
     "Grocery list generated from the week's picks",
     "Pantry check against what you already have"])

project("slip.html", "Slip", "Planned, not started",
    ["A pause before small purchases. Enter a price and how often it recurs, and Slip translates it into days of delay on your savings targets: not what it costs, but what it pushes back.",
     "Local data only. No bank connection, no account."],
    ["Price and frequency in, days of delay out",
     "A 48-hour park-it hold list for undecided purchases",
     "A running total of delay avoided"])

project("lucent.html", "Lucent Launcher", "In development",
    ["A native Minecraft launcher written in Rust with GTK4 and Libadwaita. The interface is declared in GtkBuilder XML; installation, metadata handling, launch-command construction, and process prep run in Rust worker code, off the UI thread.",
     "The launcher core is vendored in the repo (mc-launcher-core), so backend fixes don't wait on a registry release. It installs Vanilla, Fabric, Quilt, Forge, and NeoForge, merges version metadata and libraries, and constructs the Java launch command. The core's 38 tests pass.",
     "Where it stands: working in bursts, not released. The most recent work added resource-pack installation and management, Flatpak packaging, and a readiness-aware launch flow. Development happens in the open: <a href=\"https://github.com/AStellarScene/lucent-launcher\">github.com/AStellarScene/lucent-launcher</a>."],
    ["Install and launch Vanilla, Fabric, Quilt, Forge, and NeoForge",
     "Profiles with stable IDs and atomic saves",
     "Modrinth discovery and profile-scoped content, including resource packs",
     "Microsoft sign-in held in the system keyring"])

# ---------- About ----------
about_body = """  <section id="about">
    <p class="label">About</p>
    <h2>About</h2>
    <p>I'm Adam Laloge, 22. I work as an engineering test technician at a medical-device lab in Batesville, Indiana. Most of my time goes to building test software: the programs that run the tests, the interfaces technicians use, and the AI agent setups that help write them.</p>
    <p>I'm also finishing a B.S. in UX Design at WGU, on an accelerated schedule I'm holding myself to. Several projects here started as coursework. I would rather ship the working version than leave it sitting in a course document.</p>
    <p>Outside work and school, I take photographs, mostly sunsets and shoreline. I also do strength training and cardio, and I build side projects. One of them is a Minecraft launcher written in Rust, on GitHub.</p>
    <p>One habit the lab burned in: I don't trust a claim I can't measure, including my own. That's why everything on this site is labeled with where it actually stands.</p>
    <p>The software here is built with AI agents under my direction. I specify, review, and verify; the agents type.</p>
  </section>

  <section id="contact">
    <p class="label">Contact</p>
    <h2>Get in touch</h2>
    <p>Code and public projects live on GitHub: <a href="https://github.com/AStellarScene">github.com/AStellarScene</a>. Email: <a href="mailto:hello@adamlaloge.com">hello@adamlaloge.com</a>.</p>
  </section>"""
page("about.html", "About — Adam Laloge", ABOUT_DESC, "about.html", about_body)

# ---------- Latent Dreams ----------
# Layout rule (Adam, 2026-10-25): artwork is added in pairs. Each pair is
# its own two-image split band; additional pairs stack vertically below.
# Do not add a third or fourth slice to an existing band.
latent_body = """  <div class="world-ambient" aria-hidden="true"></div>
  <section class="latent-head">
    <p class="label">Dreamscape</p>
    <h2>Worlds imagined by computers</h2>
    <p class="section-note">I simply directed them.</p>
  </section>

  <div class="quilt" id="quilt">
    <canvas class="dream-gl" aria-hidden="true"></canvas>
    <button type="button" class="slice" data-world="golden" aria-expanded="false" aria-label="Open The Golden City">
      <img src="art/golden-city.jpg" alt="A golden city of spires and bridges in the clouds, built around a glowing ring" draggable="false">
      <span class="slice-title">The Golden City</span>
      <span class="slice-cap">
        <strong>The Golden City</strong>
        <span>A city that climbed into the clouds and never came back down.</span>
        <span class="slice-hint">Tap again to come back</span>
      </span>
    </button>
    <button type="button" class="slice" data-world="ember" aria-expanded="false" aria-label="Open Obsidian Dragon">
      <span class="seam" aria-hidden="true"></span>
      <img src="art/obsidian-dragon.jpg" alt="An obsidian dragon with lava-lit cracks roaring over a burning volcanic valley at night" draggable="false">
      <span class="slice-title">Obsidian Dragon</span>
      <span class="slice-cap">
        <strong>Obsidian Dragon</strong>
        <span>Stone that woke up burning, over a valley that never cools.</span>
        <span class="slice-hint">Tap again to come back</span>
      </span>
    </button>
    <button type="button" class="slice" data-world="abyss" aria-expanded="false" aria-label="Open The Drowned Bells">
      <span class="seam-h" aria-hidden="true"></span>
      <img src="art/drowned-bells.jpg" alt="A gothic cathedral-city half-drowned in a black ocean at night, its towers above the waterline and glowing teal ruins beneath the surface" draggable="false">
      <span class="slice-title">The Drowned Bells</span>
      <span class="slice-cap">
        <strong>The Drowned Bells</strong>
        <span>A cathedral-city drowned in a black sea. The windows are still lit.</span>
        <span class="slice-hint">Tap again to come back</span>
      </span>
    </button>
    <button type="button" class="slice" data-world="shore" aria-expanded="false" aria-label="Open The Far Shore">
      <span class="seam" aria-hidden="true"></span>
      <img src="art/far-shore.jpg" alt="A lone traveler on a grassy clifftop path above a calm alien sea, beneath a vast green ringed planet and a bright nebula sky" draggable="false">
      <span class="slice-title">The Far Shore</span>
      <span class="slice-cap">
        <strong>The Far Shore</strong>
        <span>A green world under a ringed giant, seen for the first time.</span>
        <span class="slice-hint">Tap again to come back</span>
      </span>
          <span class="seam-h" aria-hidden="true"></span>
    </button>
    <button type="button" class="slice" data-world="vending" aria-expanded="false" aria-label="Open The Vending Hall">
      <span class="seam-h" aria-hidden="true"></span>
      <img src="art/vending-hall.jpg" alt="A vast black warehouse under a radiant glass ceiling, solitary vending machines spaced far apart across a polished floor, receding to the horizon" draggable="false">
      <span class="slice-title">The Vending Hall</span>
      <span class="slice-cap">
        <strong>The Vending Hall</strong>
        <span>I dreamed this once, and it stayed with me. Everything here was arranged with great care, for no one, for no reason.</span>
        <span class="slice-hint">Tap again to come back</span>
      </span>
    </button>
    <button type="button" class="slice" data-world="watch" aria-expanded="false" aria-label="Open The Long Watch">
      <span class="seam" aria-hidden="true"></span>
      <img src="art/the-long-watch.jpg" alt="Thousands of cameras on tripods spread across a frozen lake at dusk, every one facing a low amber sunset under a deep blue sky" draggable="false">
      <span class="slice-title">The Long Watch</span>
      <span class="slice-cap">
        <strong>The Long Watch</strong>
        <span>They were set out to watch the sunset, and they never stopped. Devotion does not require a witness.</span>
        <span class="slice-hint">Tap again to come back</span>
      </span>
          <span class="seam-h" aria-hidden="true"></span>
    </button>
  </div>

  <p class="flow-hint">Tap a world to step inside &middot; tap again to come back</p>

  <section>
    <p class="section-note">More worlds arrive as I make them.</p>
  </section>"""
latent_js = "<script>\n" + r'''(function () {
  var quilt = document.querySelector('.quilt');
  if (!quilt) return;
  document.documentElement.classList.add('latent-live');
  // The opened quilt starts below the top bar; CSS needs the bar's real
  // height so the image is sized to the space under it, fully in view.
  // One world can be open at a time: opening another closes the first.
  var header = document.querySelector('.site-header');
  var slices = Array.prototype.slice.call(quilt.querySelectorAll('.slice'));
  var openSlice = null;
  function setBar() {
    if (!header) return;
    var h = header.offsetHeight;
    document.documentElement.style.setProperty('--bar-h', h + 'px');
    document.documentElement.style.setProperty('--bar-half', (h / 2) + 'px');
  }
  window.addEventListener('resize', function () { if (openSlice) setBar(); });
  function closeOpen() {
    if (!openSlice) return;
    openSlice = null;
    quilt.classList.remove('open');
    slices.forEach(function (s) {
      s.classList.remove('active'); s.setAttribute('aria-expanded', 'false');
    });
    document.documentElement.removeAttribute('data-world');
    document.documentElement.classList.remove('world-lock');
    document.documentElement.style.removeProperty('--bar-h');
    document.documentElement.style.removeProperty('--bar-half');
  }
  function toggle(slice) {
    if (openSlice === slice) { closeOpen(); return; }
    closeOpen();
    setBar();
    openSlice = slice;
    quilt.classList.add('open');
    slices.forEach(function (s) {
      var on = s === slice;
      s.classList.toggle('active', on);
      s.setAttribute('aria-expanded', on ? 'true' : 'false');
    });
    document.documentElement.setAttribute('data-world', slice.getAttribute('data-world'));
    document.documentElement.classList.add('world-lock');
  }
  slices.forEach(function (s) {
    s.addEventListener('click', function () { toggle(s); });
  });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && openSlice) closeOpen(); });
})();''' + "\n</script>\n" + "<script>\n" + r'''function initDreamQuilt(quilt, canvas) {
  // Dreamscape liquid-dimensional seam v5: THE QUILT.
  //
  // v3/v4 ran one WebGL engine per pair of worlds (own canvas, context,
  // textures and loop per band). v5 is a single engine for the whole
  // page: one context, one shader, one clock. The worlds form a grid of
  // cells whose rectangles are measured from the DOM layout, so the
  // seam effect is native to the grid: every pair of abutting cells
  // shares a liquid seam, horizontally AND vertically, including the
  // cross-junction where four worlds meet. Adding worlds is now data:
  // more slices in the grid, more cells in the atlas, no new engine.
  //
  // The per-seam math is the v3 math untouched -- same wave/slope
  // functions, same 0.055 band falloff, same refraction and glow terms,
  // same per-world stage framing (coverUv, focal 0.5/0.68, 1.15
  // overscan), same drift patterns (alternating by cell, as A/B did),
  // same exponential clock (tau ~190ms). What changed is the geometry
  // model: a split scalar became per-cell rectangles easing toward
  // measured targets on that same clock, and the two textures became
  // one packed atlas.
  //
  // Mobile budget, deliberate:
  // - One context and one rAF for the whole page (was: one per pair).
  // - Atlas cells cap at 1024px on small screens (2048 desktop), and
  //   the packer picks the shelf budget with the smallest POT area.
  // - DPR step-down [2, 1.75, 1.5] on sustained slow frames, as v4.
  // - IntersectionObserver + visibility gating, as v4: an off-screen
  //   quilt costs nothing. The rAF watchdog is kept too.
  // - Texture sources are read from each slice's own <img> (the v4
  //   lesson: no hardcoded art paths, ever).
  //
  // v6 (2026-10-28): a WebGL2 path runs alongside the atlas. One
  // texture per world at native size (SRGB8_ALPHA8), so quality no
  // longer dilutes as worlds are added and no packing budget can
  // starve a texture-capped device; samples arrive linear, so seam
  // blends stop dipping dark (the gamma-space mix was darkening
  // every seam midpoint), and highp fragment precision is
  // guaranteed. The seam math is untouched. WebGL1-only devices
  // run the v5 atlas engine exactly as before.
  if (!quilt || !canvas) return;
  var slices = Array.prototype.slice.call(quilt.querySelectorAll('.slice'));
  var N = slices.length, MAXC = 12;
  if (N < 2 || N > MAXC) return;

  var CTX = { alpha: false, depth: false, stencil: false, antialias: false, powerPreference: 'low-power' };
  var gl = null, isGL2 = false;
  try { gl = canvas.getContext('webgl2', CTX); if (gl) isGL2 = true; } catch (e) { gl = null; }
  if (!gl) { try { gl = canvas.getContext('webgl', CTX); } catch (e) { gl = null; } }
  if (!gl) return;

  // Dialect ladder. es3 = the WebGL2 dialect (ES 3.00 shaders,
  // per-world textures, linear blending). If anything in it fails --
  // too few texture units, or a shader construct a driver rejects --
  // the engine steps down to the ES 1.00 atlas dialect INSIDE the
  // same context (tryProgram below) instead of dying to the DOM
  // fallback. v6.0 shipped without the middle rung: ANGLE rejected
  // the ES 3.00 fragment shader and the whole quilt went dark.
  var es3 = isGL2 && gl.getParameter(gl.MAX_TEXTURE_IMAGE_UNITS) >= N;
  var mode = 'none';
  var VERT = '', FRAG = '';
  function buildShaders() {
    VERT = es3
      ? '#version 300 es\nin vec2 aPos;out vec2 vUv;void main(){vUv=aPos*0.5+0.5;gl_Position=vec4(aPos,0.0,1.0);}'
      : 'attribute vec2 aPos;varying vec2 vUv;void main(){vUv=aPos*0.5+0.5;gl_Position=vec4(aPos,0.0,1.0);}';
    var OUTC = es3 ? 'fragColor' : 'gl_FragColor';

  // Fragment shader, assembled in JS so the four seam sides (L,R,T,B)
  // are emitted as straight-line code with literal indices -- no
  // dynamic array indexing beyond loop indices anywhere.
  var F = [];
  if (es3) {
    F.push(
      '#version 300 es',
      'precision highp float;',
      'in vec2 vUv;',
      'out vec4 fragColor;',
      'uniform sampler2D uTex[' + MAXC + '];'
    );
  } else {
    F.push(
      'precision mediump float;',
      'varying vec2 vUv;',
      'uniform sampler2D uAtlas;',
      'uniform vec2 uAtlasSize;'
    );
  }
  F.push(
    'uniform float uTime;',
    'uniform float uBand;',
    'uniform float uQA;', // quilt aspect (width / height, CSS px)
    'uniform float uBw;', // canvas backing width in device px: seam shading scale
    'uniform float uCount;',
    'uniform vec4 uVis;', // visible region of the canvas (GL uv) -- off-view fragments exit cheap
    'uniform vec4 uRect[' + MAXC + '];', // cell rects, page space (x0, y0, x1, y1), y down
    'uniform vec4 uUVR[' + MAXC + '];', // atlas sub-rect per cell (scaleX, scaleY, offX, offY)
    'uniform float uTA[' + MAXC + '];', // texture aspect per cell
    'uniform vec4 uNbr[' + MAXC + '];', // neighbour cell index per side (L, R, T, B), -1 none
    'uniform vec4 uAct[' + MAXC + '];', // seam activity per side (L, R, T, B)
    'uniform vec4 uPhase[' + MAXC + '];', // per-edge wave phase per side -- an edge property,
    'uniform vec4 uTempo[' + MAXC + '];', // per-edge tempo per side -- identical from both
    'uniform vec4 uAmp[' + MAXC + '];', // per-edge amplitude per side -- sides or seams tear
    'vec2 coverUv(vec2 local, float ta, float va){',
    '  vec2 f = vec2(0.5, 0.68);',
    '  float r = va / ta;',
    '  vec2 u = local;',
    '  if (r >= 1.0) { float vf = 1.0 / r; u = vec2(local.x, f.y * (1.0 - vf) + local.y * vf); }',
    '  else { u = vec2(f.x * (1.0 - r) + local.x * r, local.y); }',
    '  return f + (u - f) / 1.15;',
    '}'
  );
  if (es3) {
    // Per-world textures: the cover uv IS the texture uv, and
    // CLAMP_TO_EDGE on a world's own texture smears its edge pixels
    // -- the v3 melt, restored by construction rather than by an
    // inset clamp. textureGrad with explicit gradients keeps
    // sampling well-defined inside the divergent per-side branches.
    // The sampler branches use LITERAL indices: indexing a sampler
    // array with a loop index is legal ES 3.00 on paper, but ANGLE
    // (Chrome's and Safari's WebGL translator alike) rejects it --
    // "array index for samplers must be constant integral
    // expressions" -- which is what killed v6.0 in the field.
    // Textures are SRGB8_ALPHA8, so samples arrive LINEAR: the seam
    // mixes stop dipping dark, and srgbEncode restores the display
    // curve once at the end.
    // v6.4 (2026-10-28): the sampler's gradients are FIXED, not
    // hardware-inferred. dFdx/dFdy are computed over 2x2 fragment
    // quads; a quad straddling a cell boundary mixes UVs from two
    // texture spaces, the inferred gradient explodes, and those
    // fragments sample the coarsest mip -- the whole texture
    // averaged -- drawing a straight line of average colour along
    // the boundary (bright over dark content, dark over bright).
    // It surfaced when the quilt grew to six worlds and the new
    // boundaries landed on straddling parities. Telling the
    // sampler a fixed fine gradient removes the inference; Adam
    // judged the result perfect on his phone (the ?diag=7 test)
    // and chose it as the shipping version.
    var swLines = [
      'vec3 sampleWorld(int idx, vec2 uv){',
      '  vec2 gx = vec2(0.001, 0.0); vec2 gy = vec2(0.0, 0.001);'
    ];
    for (var wi = 0; wi < MAXC; wi++) {
      swLines.push('  if (idx == ' + wi + ') return textureGrad(uTex[' + wi + '], uv, gx, gy).rgb;');
    }
    swLines.push('  return vec3(0.0);', '}');
    F.push.apply(F, swLines);
    F.push(
      'vec3 srgbEncode(vec3 c){',
      '  return pow(clamp(c, 0.0, 1.0), vec3(1.0 / 2.2));',
      '}'
    );
  } else {
    // Per-cell CLAMP_TO_EDGE inside the atlas. v3/v4 gave each world
    // its own texture, so samples pushed past the edge by the wave,
    // drift or refraction clamped to the world's edge pixels -- that
    // clamp IS the melt. In the atlas, past a cell's sub-rect lies
    // empty padding (black), which showed as a dark band at every
    // seam. Clamping the final sample to the sub-rect restores it.
    F.push(
      'vec3 sampleCell(vec2 uv, vec4 rect){',
      '  vec2 suv = uv * rect.xy + rect.zw;',
      '  vec2 pad = vec2(0.6) / uAtlasSize;',
      '  suv = clamp(suv, rect.zw + pad, rect.zw + rect.xy - pad);',
      '  return texture2D(uAtlas, suv).rgb;',
      '}'
    );
  }
  F.push(
    // The v3 waveform, unchanged -- but each edge runs it with its own
    // phase and tempo, so the seams no longer crest in lockstep. The
    // parameters belong to the EDGE (the unordered pair of cells), so
    // both sides compute the identical line and the seam cannot tear.
    'float waveP(float s, float t, float ph, float tm){',
    '  float tt = t * tm;',
    '  return 0.011 * sin(6.9 * s - tt * 0.70 + ph)',
    '       + 0.006 * sin(13.7 * s + tt * 0.42 + 1.7 + ph)',
    '       + 0.0025 * sin(27.0 * s - tt * 0.24 + 4.1 + ph);',
    '}',
    'float slopeP(float s, float t, float ph, float tm){',
    '  float tt = t * tm;',
    '  return 0.011 * 6.9 * cos(6.9 * s - tt * 0.70 + ph)',
    '       + 0.006 * 13.7 * cos(13.7 * s + tt * 0.42 + 1.7 + ph)',
    '       + 0.0025 * 27.0 * cos(27.0 * s - tt * 0.24 + 4.1 + ph);',
    '}',
    'float envW(float s){', // corner taper: full melt mid-edge, zero at the ends
    '  return smoothstep(0.0, 0.16, s) * smoothstep(1.0, 0.84, s);',
    '}',
    'vec2 driftFor(float idx, float t){',
    '  float ph = idx * 1.93;', // per-world phase: diagonal twins no longer drift together
    '  if (mod(idx, 2.0) < 0.5) return vec2(sin(t * 0.33 + ph), sin(t * 0.23 + 1.3 + ph)) * 0.020;',
    '  return vec2(sin(t * 0.19 + 2.1 + ph), sin(t * 0.27 + 0.4 + ph)) * 0.012;',
    '}',
    'void main(){',
    '  if (vUv.x < uVis.x || vUv.x > uVis.z || vUv.y < uVis.y || vUv.y > uVis.w) {',
    '    ' + OUTC + ' = vec4(0.0, 0.0, 0.0, 1.0); return;',
    '  }',
    '  vec2 p = vec2(vUv.x, 1.0 - vUv.y);', // page space: y down
    '  float t = uTime;',
    '  int ci = -1;',
    '  vec4 cr = vec4(0.0); vec4 cuv = vec4(0.0); float cta = 1.0;',
    '  vec4 nbr = vec4(-1.0); vec4 act4 = vec4(0.0);',
    '  vec4 phT = vec4(0.0); vec4 tmT = vec4(1.0); vec4 amT = vec4(1.0);',
    '  for (int i = 0; i < ' + MAXC + '; i++) {',
    '    if (float(i) >= uCount) break;',
    '    vec4 r = uRect[i];',
    '    if (p.x >= r.x && p.x <= r.z && p.y >= r.y && p.y <= r.w) {',
    '      ci = i; cr = r; cuv = uUVR[i]; cta = uTA[i]; nbr = uNbr[i]; act4 = uAct[i];',
    '      phT = uPhase[i]; tmT = uTempo[i]; amT = uAmp[i];',
    '    }',
    '  }',
    '  if (ci < 0) { ' + OUTC + ' = vec4(0.0, 0.0, 0.0, 1.0); return; }',
    '  vec2 cellSize = max(cr.zw - cr.xy, vec2(0.0001));',
    // Stage-local coords are built in GL orientation (y UP): coverUv
    // and its focal point are defined in that space (as in v3/v4, whose
    // locals came from vUv). Building local from page-space y-down
    // renders every world upside-down -- caught on the live page.
    '  vec2 local = vec2((p.x - cr.x) / cellSize.x, 1.0 - (p.y - cr.y) / cellSize.y);',
    '  float breathe = 1.0 + 0.2 * sin(t * 0.31 + 0.8);',
    '  vec2 refrSum = vec2(0.0);',
    // Interior fast path: beyond 0.10 of every edge, the seam terms
    // contribute under ~0.4% luminance (the band falloff sees to
    // that), so the per-side seam work is skipped entirely. Most of
    // the quilt is interior -- this is what keeps full DPR affordable.
    '  float edgeDist = min(min(p.x - cr.x, cr.z - p.x), min(p.y - cr.y, cr.w - p.y));',
    '  bool nearSeam = edgeDist < 0.10;'
  );
  var COMP = ['x', 'y', 'z', 'w'];
  // Per-side seam pre-pass: signed distance to the displaced edge line
  // (positive inside this cell), band falloff, slope, refraction vector.
  // Geometry mirrors v3: for a vertical seam the wave runs on uv.y
  // (GL-up, hence 1.0 - p.y), for a horizontal seam on uv.x.
  // The wave is parameterised by SEGMENT-LOCAL s (0..1 along this
  // cell's own edge) and tapered to zero at the segment ends. In the
  // quilt, four edges meet at the centre cross; with the old global
  // parameter each edge arrived at the cross at a different wave
  // value, so the boundary line jumped -- a visible ledge where the
  // four worlds meet. Zero displacement at every corner makes all
  // edges agree at the corners by construction, while mid-edge (most
  // of every seam) keeps the full v3 melt. Neighbours sharing an
  // edge extent compute the identical seg, so the line still cannot
  // tear.
  var GEO = [
    { pre: 'segS = 1.0 - (p.y - cr.y) / cellSize.y; lnS = cr.x + waveP(segS, t, phS, tmS) * envW(segS) * actS * amS; dS = p.x - lnS; slS = slopeP(segS, t, phS, tmS) * envW(segS) * amS;',
      post: 'rfS = vec2(-slS * 0.012 * bFS, 0.0);' },
    { pre: 'segS = 1.0 - (p.y - cr.y) / cellSize.y; lnS = cr.z + waveP(segS, t, phS, tmS) * envW(segS) * actS * amS; dS = lnS - p.x; slS = slopeP(segS, t, phS, tmS) * envW(segS) * amS;',
      post: 'rfS = vec2(slS * 0.012 * bFS, 0.0);' },
    { pre: 'segS = (p.x - cr.x) / cellSize.x; lnS = cr.y + waveP(segS, t, phS, tmS) * envW(segS) * actS * amS; dS = p.y - lnS; slS = slopeP(segS, t, phS, tmS) * envW(segS) * amS;',
      post: 'rfS = vec2(0.0, slS * 0.012 * bFS);' },
    { pre: 'segS = (p.x - cr.x) / cellSize.x; lnS = cr.w + waveP(segS, t, phS, tmS) * envW(segS) * actS * amS; dS = lnS - p.y; slS = slopeP(segS, t, phS, tmS) * envW(segS) * amS;',
      post: 'rfS = vec2(0.0, -slS * 0.012 * bFS);' }
  ];
  // The side placeholder is a word-final capital S (segS, lnS, dS,
  // slS, rfS, bFS...). A blind split on 'S' also eats the S inside
  // 'cellSize', emitting 'cell0ize' -- an undeclared identifier that
  // fails the whole shader compile and silently drops the page to
  // the DOM fallback. Replace only an S NOT followed by a lowercase
  // letter, which is every placeholder and nothing else.
  function subS(str, s) { return str.replace(/S(?![a-z])/g, String(s)); }
  for (var s = 0; s < 4; s++) {
    F.push(
      '  float nj' + s + ' = nbr.' + COMP[s] + ';',
      '  float act' + s + ' = act4.' + COMP[s] + ';',
      '  float ph' + s + ' = phT.' + COMP[s] + ';',
      '  float tm' + s + ' = tmT.' + COMP[s] + ';',
      '  float am' + s + ' = amT.' + COMP[s] + ';',
      '  vec4 nr' + s + ' = vec4(0.0); vec4 nuv' + s + ' = vec4(0.0); float nta' + s + ' = 1.0; float has' + s + ' = 0.0;',
      '  for (int j = 0; j < ' + MAXC + '; j++) {',
      '    if (float(j) >= uCount) break;',
      '    if (abs(float(j) - nj' + s + ') < 0.5) { nr' + s + ' = uRect[j]; nuv' + s + ' = uUVR[j]; nta' + s + ' = uTA[j]; has' + s + ' = 1.0; }',
      '  }',
      '  float ln' + s + ' = 0.0; float d' + s + ' = 1000.0; float bF' + s + ' = 0.0; float sl' + s + ' = 0.0; float seg' + s + ' = 0.0; vec2 rf' + s + ' = vec2(0.0);',
      '  if (nearSeam && has' + s + ' > 0.5 && act' + s + ' > 0.001) {',
      '    ' + subS(GEO[s].pre, s).replace(/act\d/g, 'act' + s),
      '    bF' + s + ' = exp(-abs(d' + s + ') / uBand) * act' + s + ';',
      '    ' + subS(GEO[s].post, s),
      '    refrSum += rf' + s + ';',
      '  }'
    );
  }
  F.push(
    '  vec2 drift = driftFor(float(ci), t);',
    '  float va = cellSize.x * uQA / cellSize.y;',
    '  vec2 ouv = coverUv(local, cta, va) + drift + refrSum * breathe;',
    '  vec3 col = ' + (es3 ? 'sampleWorld(ci, ouv)' : 'sampleCell(ouv, cuv)') + ';'
  );
  for (var s2 = 0; s2 < 4; s2++) {
    F.push(
      '  if (nearSeam && has' + s2 + ' > 0.5 && act' + s2 + ' > 0.001) {',
      '    vec2 nsz' + s2 + ' = max(nr' + s2 + '.zw - nr' + s2 + '.xy, vec2(0.0001));',
      '    vec2 nl' + s2 + ' = vec2((p.x - nr' + s2 + '.x) / nsz' + s2 + '.x, 1.0 - (p.y - nr' + s2 + '.y) / nsz' + s2 + '.y);',
      '    float nva' + s2 + ' = nsz' + s2 + '.x * uQA / nsz' + s2 + '.y;',
      '    vec2 nuv2_' + s2 + ' = coverUv(nl' + s2 + ', nta' + s2 + ', nva' + s2 + ') + driftFor(nj' + s2 + ', t) + rf' + s2 + ' * 1.6 * breathe;',
      '    vec3 ncol' + s2 + ' = ' + (es3 ? 'sampleWorld(int(nj' + s2 + ' + 0.5), nuv2_' + s2 + ')' : 'sampleCell(nuv2_' + s2 + ', nuv' + s2 + ')') + ';',
      '    col = mix(ncol' + s2 + ', col, smoothstep(-0.0015, 0.0015, d' + s2 + '));',
      '    col += clamp(sl' + s2 + ', -1.0, 1.0) * bF' + s2 + ' * 0.13;',
      '    col += exp(-abs(d' + s2 + ') * uBw * 0.28) * 0.08 * act' + s2 + ';',
      '    col -= exp(-abs(d' + s2 + ' - 4.5 / uBw) * uBw * 0.20) * 0.0 * act' + s2 + ';', // v6.2: groove zeroed — bisection (2026-10-28) convicted it of the straight centre line; slope light + glow keep the dimension
      '  }'
    );
  }
  F.push('  ' + OUTC + ' = vec4(' + (es3 ? 'srgbEncode(col)' : 'col') + ', 1.0);', '}');
    FRAG = F.join('\n');
  }

  function shader(type, src) {
    var sh = gl.createShader(type);
    gl.shaderSource(sh, src);
    gl.compileShader(sh);
    if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) return null;
    return sh;
  }
  function tryProgram() {
    buildShaders();
    var vs = shader(gl.VERTEX_SHADER, VERT), fs = shader(gl.FRAGMENT_SHADER, FRAG);
    if (!vs || !fs) return null;
    var p = gl.createProgram();
    gl.attachShader(p, vs); gl.attachShader(p, fs); gl.linkProgram(p);
    if (!gl.getProgramParameter(p, gl.LINK_STATUS)) { gl.deleteProgram(p); return null; }
    return p;
  }
  var prog = tryProgram();
  if (!prog && es3) { es3 = false; prog = tryProgram(); }
  if (!prog) return;
  mode = es3 ? 'webgl2' : (isGL2 ? 'webgl2-es1' : 'webgl1');
  gl.useProgram(prog);

  var buf = gl.createBuffer();
  gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  var aPos = gl.getAttribLocation(prog, 'aPos');
  gl.enableVertexAttribArray(aPos);
  gl.vertexAttribPointer(aPos, 2, gl.FLOAT, false, 0, 0);

  var U = {};
  ['uAtlas', 'uAtlasSize', 'uTime', 'uBand', 'uQA', 'uBw', 'uCount', 'uVis'].forEach(function (name) {
    U[name] = gl.getUniformLocation(prog, name);
  });
  U.uRect = gl.getUniformLocation(prog, 'uRect[0]');
  U.uUVR = gl.getUniformLocation(prog, 'uUVR[0]');
  U.uTA = gl.getUniformLocation(prog, 'uTA[0]');
  U.uNbr = gl.getUniformLocation(prog, 'uNbr[0]');
  U.uAct = gl.getUniformLocation(prog, 'uAct[0]');
  U.uPhase = gl.getUniformLocation(prog, 'uPhase[0]');
  U.uTempo = gl.getUniformLocation(prog, 'uTempo[0]');
  U.uAmp = gl.getUniformLocation(prog, 'uAmp[0]');
  gl.uniform1i(U.uAtlas, 0);
  gl.uniform1f(U.uBand, 0.055);
  gl.uniform1f(U.uBw, 1600);
  gl.uniform1f(U.uCount, N);

  var anisoExt = gl.getExtension('EXT_texture_filter_anisotropic') ||
                 gl.getExtension('WEBKIT_EXT_texture_filter_anisotropic');
  var maxAniso = anisoExt ? gl.getParameter(anisoExt.MAX_TEXTURE_MAX_ANISOTROPY_EXT) : 1;
  var maxTexSize = gl.getParameter(gl.MAX_TEXTURE_SIZE);

  function nextPow2(v) { var p = 1; while (p < v) p *= 2; return p; }

  // ---- Atlas: every world packed into ONE texture -------------------
  var atlasTex = null;
  var texReady = false;   // set by whichever texture path uploaded
  var cellUV = [];   // per cell: [sx, sy, ox, oy]
  var cellTA = [];   // per cell: natural aspect
  function buildAtlas() {
    // Atlas resolution follows the DISPLAY, not a screen-size guess
    // (the old 1024 cap starved landscape tablets/phones and read as
    // a filtering regression). A cell can be as wide as the whole
    // quilt (single-column portrait), so size for quilt width x DPR
    // with headroom; the attempt loop still shrinks if the packed
    // atlas would exceed texture limits.
    var dprNeed = Math.min(window.devicePixelRatio || 1, 2);
    var need = Math.ceil((quilt.clientWidth || 1200) * dprNeed * 1.1);
    var cellMax = Math.max(1024, Math.min(2048, need));
    var PAD = 16;
    var sized = slices.map(function (el, idx) {
      var img = el.querySelector('img');
      return { idx: idx, img: img, nw: img.naturalWidth, nh: img.naturalHeight };
    });
    // Fit, don't halve: try full resolution first across several
    // shelf budgets; if no packing fits the device's texture limit,
    // step the cell size down gently (0.85, 0.72, ...) and retry.
    // The old loop halved cellMax twice when the naive packing
    // overflowed, which baked every world at ~512px on tablets
    // whose GPUs cap textures at 2048-4096px -- the whole quilt
    // then upscaled into mosaic blocks.
    var cap = Math.min(8192, maxTexSize);
    var scales = [1, 0.85, 0.72, 0.6, 0.5, 0.42, 0.35];
    for (var attempt = 0; attempt < scales.length; attempt++) {
      var cm = Math.max(256, Math.floor(cellMax * scales[attempt]));
      var best = null;
      [cm, Math.floor(cm * 1.5), cm * 2, cm * 3, cm * 4].forEach(function (budget) {
        var x = 0, y = 0, rowH = 0, usedW = 0;
        var items = sized.map(function (it) {
          var sc = Math.min(1, cm / Math.max(it.nw, it.nh));
          var dw = Math.max(2, Math.round(it.nw * sc)), dh = Math.max(2, Math.round(it.nh * sc));
          if (x > 0 && x + dw > budget) { x = 0; y += rowH + PAD; rowH = 0; }
          var rec = { idx: it.idx, img: it.img, x: x, y: y, w: dw, h: dh };
          x += dw + PAD;
          if (x - PAD > usedW) usedW = x - PAD;
          if (dh > rowH) rowH = dh;
          return rec;
        });
        var usedH = y + rowH;
        var AW = nextPow2(usedW), AH = nextPow2(usedH);
        if (AW > cap || AH > cap) return; // infeasible at this budget
        var score = AW * AH, tie = Math.max(AW, AH);
        if (!best || score < best.score || (score === best.score && tie < best.tie)) {
          best = { items: items, AW: AW, AH: AH, score: score, tie: tie };
        }
      });
      if (best || attempt === scales.length - 1) {
        if (!best) { // last resort: smallest scale, widest shelf
          var x2 = 0, y2 = 0, rowH2 = 0, usedW2 = 0;
          var items2 = sized.map(function (it) {
            var sc2 = Math.min(1, cm / Math.max(it.nw, it.nh));
            var dw2 = Math.max(2, Math.round(it.nw * sc2)), dh2 = Math.max(2, Math.round(it.nh * sc2));
            if (x2 > 0 && x2 + dw2 > cm * 4) { x2 = 0; y2 += rowH2 + PAD; rowH2 = 0; }
            var rec2 = { idx: it.idx, img: it.img, x: x2, y: y2, w: dw2, h: dh2 };
            x2 += dw2 + PAD;
            if (x2 - PAD > usedW2) usedW2 = x2 - PAD;
            if (dh2 > rowH2) rowH2 = dh2;
            return rec2;
          });
          best = { items: items2, AW: nextPow2(usedW2), AH: nextPow2(y2 + rowH2), score: 0, tie: 0 };
        }
        var cv = document.createElement('canvas');
        cv.width = best.AW; cv.height = best.AH;
        var ctx = cv.getContext('2d');
        cellUV = new Array(N); cellTA = new Array(N);
        best.items.forEach(function (it) {
          ctx.drawImage(it.img, it.x, it.y, it.w, it.h);
          cellUV[it.idx] = [it.w / best.AW, it.h / best.AH, it.x / best.AW, 1 - (it.y + it.h) / best.AH];
          cellTA[it.idx] = it.img.naturalWidth / it.img.naturalHeight;
        });
        if (atlasTex) gl.deleteTexture(atlasTex);
        atlasTex = gl.createTexture();
        gl.activeTexture(gl.TEXTURE0);
        gl.bindTexture(gl.TEXTURE_2D, atlasTex);
        gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
        var IFMT = isGL2 ? gl.RGBA : gl.RGB; // ES 3.00 contexts take the sized-friendly form
        gl.texImage2D(gl.TEXTURE_2D, 0, IFMT, IFMT, gl.UNSIGNED_BYTE, cv);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
        gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
        if (anisoExt && maxAniso > 1) gl.texParameteri(gl.TEXTURE_2D, anisoExt.TEXTURE_MAX_ANISOTROPY_EXT, Math.min(16, maxAniso));
        gl.generateMipmap(gl.TEXTURE_2D);
        gl.uniform2f(U.uAtlasSize, best.AW, best.AH);
        texReady = true;
        return true;
      }
    }
    return false;
  }

  // ---- WebGL2: one texture per world, native size, sRGB ------------
  // No packing, no budget staircase, no shared cap: each world is
  // uploaded once at its natural resolution, so adding worlds never
  // dilutes the ones already there. SRGB8_ALPHA8 makes the GPU hand
  // the shader linear values; the seam mixes then average light the
  // way light actually averages.
  var worldTex = [];
  function buildWorldTextures() {
    cellUV = new Array(N); cellTA = new Array(N);
    for (var i = 0; i < N; i++) {
      var img = slices[i].querySelector('img');
      if (!img || !img.naturalWidth) return false;
      var tx = gl.createTexture();
      gl.activeTexture(gl.TEXTURE0 + i);
      gl.bindTexture(gl.TEXTURE_2D, tx);
      gl.pixelStorei(gl.UNPACK_FLIP_Y_WEBGL, true);
      gl.texImage2D(gl.TEXTURE_2D, 0, gl.SRGB8_ALPHA8, gl.RGBA, gl.UNSIGNED_BYTE, img);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, gl.CLAMP_TO_EDGE);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR_MIPMAP_LINEAR);
      gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
      if (anisoExt && maxAniso > 1) gl.texParameteri(gl.TEXTURE_2D, anisoExt.TEXTURE_MAX_ANISOTROPY_EXT, Math.min(16, maxAniso));
      gl.generateMipmap(gl.TEXTURE_2D);
      worldTex.push(tx);
      cellUV[i] = [1, 1, 0, 0];   // draw() still uploads uUVR; unused by the GL2 shader
      cellTA[i] = img.naturalWidth / img.naturalHeight;
    }
    var loc = gl.getUniformLocation(prog, 'uTex[0]');
    var arr = [];
    for (var k = 0; k < MAXC; k++) arr.push(k < N ? k : 0);
    gl.uniform1iv(loc, arr);
    gl.activeTexture(gl.TEXTURE0);
    texReady = true;
    return true;
  }
  function buildTextures() { return es3 ? buildWorldTextures() : buildAtlas(); }

  // ---- Cell geometry: measured rects, eased on the v3 clock ---------
  var home = [], target = [], cur = [], nbrs = [];
  var quiltW = 0, quiltH = 0;
  function clamp01(v) { return Math.min(1, Math.max(0, v)); }
  function measureLayout() {
    var q = quilt.getBoundingClientRect();
    if (!q.width || !q.height) return false;
    quiltW = q.width; quiltH = q.height;
    home = slices.map(function (el) {
      var r = el.getBoundingClientRect();
      return [
        clamp01((r.left - q.left) / q.width), clamp01((r.top - q.top) / q.height),
        clamp01((r.right - q.left) / q.width), clamp01((r.bottom - q.top) / q.height)
      ];
    });
    // Neighbours from the settled layout: cells whose home rects abut
    // within a tolerance, with real overlap on the cross axis.
    nbrs = home.map(function () { return [-1, -1, -1, -1]; });
    for (var i = 0; i < N; i++) {
      for (var j = 0; j < N; j++) {
        if (i === j) continue;
        var a = home[i], b = home[j];
        var ovY = Math.min(a[3], b[3]) - Math.max(a[1], b[1]);
        var ovX = Math.min(a[2], b[2]) - Math.max(a[0], b[0]);
        if (Math.abs(a[2] - b[0]) < 0.01 && ovY > 0.05) nbrs[i][1] = j; // j right of i
        if (Math.abs(a[0] - b[2]) < 0.01 && ovY > 0.05) nbrs[i][0] = j; // j left of i
        if (Math.abs(a[3] - b[1]) < 0.01 && ovX > 0.05) nbrs[i][3] = j; // j below i
        if (Math.abs(a[1] - b[3]) < 0.01 && ovX > 0.05) nbrs[i][2] = j; // j above i
      }
    }
    if (!quilt.classList.contains('open')) {
      gridNbrs = nbrs.map(function (r) { return r.slice(); });
    }
    return true;
  }
  function computeTargets() {
    target = home.map(function (h) { return h.slice(); });
    if (!quilt.classList.contains('open')) return;
    var ai = -1;
    slices.forEach(function (el, i) { if (el.classList.contains('active')) ai = i; });
    if (ai < 0) return;
    for (var i = 0; i < N; i++) {
      if (i === ai) { target[i] = [0, 0, 1, 1]; continue; }
      // Collapse the other worlds onto the quilt edge nearest their
      // home, keeping the cross-axis span, so a close re-opens them
      // from that edge -- the v3 split-parking behaviour, generalised.
      var h = home[i];
      var cx = (h[0] + h[2]) / 2, cy = (h[1] + h[3]) / 2;
      if (Math.abs(cx - 0.5) >= Math.abs(cy - 0.5)) {
        var ex = cx < 0.5 ? 0 : 1;
        target[i] = [ex, h[1], ex, h[3]];
      } else {
        var ey = cy < 0.5 ? 0 : 1;
        target[i] = [h[0], ey, h[2], ey];
      }
    }
  }
  // The quilt canvas is ~124vh tall but only ~100vh is ever on
  // screen: fragments outside the visible region exit at the top of
  // the shader instead of paying for the seam machinery.
  var vis = [0, 0, 1, 1];
  function updateVis() {
    var r = quilt.getBoundingClientRect();
    if (!r.width || !r.height) return;
    var M = 0.03;
    var x0 = Math.max(0, -r.left / r.width - M), x1 = Math.min(1, (window.innerWidth - r.left) / r.width + M);
    var yt = Math.max(0, -r.top / r.height - M), yb = Math.min(1, (window.innerHeight - r.top) / r.height + M);
    vis = [x0, 1 - yb, x1, 1 - yt]; // GL uv: y up
  }
  window.addEventListener('scroll', updateVis, { passive: true });
  function retarget() {
    resize();
    if (!measureLayout()) return;
    computeTargets();
    updateVis();
    if (quilt.classList.contains('open')) fixedTop = quilt.getBoundingClientRect().top;
  }
  function smoothstepJS(e0, e1, x) {
    var t = Math.min(1, Math.max(0, (x - e0) / (e1 - e0)));
    return t * t * (3 - 2 * t);
  }
  // Per-edge character: an edge is the unordered pair of cells, so a
  // hash of the pair gives both sides the same phase/tempo/amplitude
  // (the seam line is one physical thing, computed identically from
  // either cell). Tap impulses ride on top: poking a world swells its
  // edges, decaying over ~2s like a disturbed membrane settling.
  function edgeKey(i, j) { return Math.min(i, j) * 16 + Math.max(i, j); }
  function edgeHash(key, salt) {
    var h = Math.sin(key * 127.1 + salt * 311.7) * 43758.5453;
    return h - Math.floor(h);
  }
  function edgeParams(i, j) {
    var key = edgeKey(i, j);
    return {
      key: key,
      ph: edgeHash(key, 1) * 6.2832,
      tm: 0.92 + edgeHash(key, 2) * 0.16,
      amp: 0.85 + edgeHash(key, 3) * 0.3
    };
  }
  var impulses = {}; // edgeKey -> tSec of last poke
  var lastOpenIdx = -1;
  var gridNbrs = []; // adjacency from the closed layout (the true grid)
  function pokeEdges(cellIdx) {
    if (cellIdx < 0 || !gridNbrs[cellIdx]) return;
    gridNbrs[cellIdx].forEach(function (j) {
      if (j >= 0) impulses[edgeKey(cellIdx, j)] = tSec;
    });
  }
  function activities() {
    // Per side: the seam calms as either side's across-extent parks at
    // an edge -- v3's edge factor, computed from the eased rects.
    var acts = [];
    for (var i = 0; i < N; i++) {
      var a = cur[i], out = [0, 0, 0, 0];
      for (var s = 0; s < 4; s++) {
        var j = nbrs[i] ? nbrs[i][s] : -1;
        if (j < 0 || !cur[j] || !a) continue;
        var b = cur[j], v;
        if (s === 0 || s === 1) {
          var ovY = Math.min(a[3], b[3]) - Math.max(a[1], b[1]);
          v = smoothstepJS(0, 0.07, Math.min(a[2] - a[0], b[2] - b[0])) * smoothstepJS(0, 0.05, ovY);
        } else {
          var ovX = Math.min(a[2], b[2]) - Math.max(a[0], b[0]);
          v = smoothstepJS(0, 0.07, Math.min(a[3] - a[1], b[3] - b[1])) * smoothstepJS(0, 0.05, ovX);
        }
        out[s] = v;
      }
      acts.push(out[0], out[1], out[2], out[3]);
    }
    return acts;
  }

  // ---- Loop machinery: ported from v4, now singular ------------------
  var mq = window.matchMedia('(prefers-reduced-motion: reduce)');
  var dprSteps = [2, 1.75, 1.5], stepIdx = 0;
  var inView = true, running = false, raf = 0, lastTs = 0, tSec = 0;
  var lastTickAt = 0, lastRafAt = 0, intervalDriver = null;
  var ftSum = 0, ftCount = 0;
  var TAU = 0.19;
  var quiltOffset = 0;     // FLIP counter-shift for the close drop
  var fixedTop = 0;        // quilt's viewport top while open (recorded)
  var needsRetarget = false;
  var ready = false;

  function resize() {
    var w = quilt.clientWidth, h = quilt.clientHeight;
    if (!w || !h) return;
    var dpr = Math.min(window.devicePixelRatio || 1, dprSteps[stepIdx]);
    var bw = Math.round(w * dpr), bh = Math.round(h * dpr);
    if (canvas.width !== bw || canvas.height !== bh) {
      canvas.width = bw; canvas.height = bh;
      gl.viewport(0, 0, bw, bh);
      if (U.uBw) gl.uniform1f(U.uBw, bw);
    }
  }
  function animating() {
    if (quiltOffset !== 0) return true;
    for (var i = 0; i < N; i++) {
      if (!cur[i] || !target[i]) return true;
      for (var c = 0; c < 4; c++) {
        if (Math.abs(target[i][c] - cur[i][c]) > 0.0015) return true;
      }
    }
    return false;
  }
  var rectBuf = new Float32Array(MAXC * 4);
  var uvBuf = new Float32Array(MAXC * 4);
  var taBuf = new Float32Array(MAXC);
  var nbrBuf = new Float32Array(MAXC * 4);
  var actBuf = new Float32Array(MAXC * 4);
  var phaseBuf = new Float32Array(MAXC * 4);
  var tempoBuf = new Float32Array(MAXC * 4);
  var ampBuf = new Float32Array(MAXC * 4);
  function draw(time) {
    if (!texReady || !cur.length) return;
    var i, c;
    for (i = 0; i < N; i++) {
      for (c = 0; c < 4; c++) {
        rectBuf[i * 4 + c] = cur[i][c];
        uvBuf[i * 4 + c] = cellUV[i][c];
        var j = nbrs[i] ? nbrs[i][c] : -1;
        nbrBuf[i * 4 + c] = j;
        if (j >= 0) {
          var ep = edgeParams(i, j);
          var amp = ep.amp;
          var t0 = impulses[ep.key];
          if (t0 !== undefined) {
            var age = time - t0;
            if (age < 2.5) amp *= 1 + 1.5 * Math.exp(-age / 0.6);
            else delete impulses[ep.key];
          }
          phaseBuf[i * 4 + c] = ep.ph;
          tempoBuf[i * 4 + c] = ep.tm;
          ampBuf[i * 4 + c] = amp;
        } else {
          phaseBuf[i * 4 + c] = 0;
          tempoBuf[i * 4 + c] = 1;
          ampBuf[i * 4 + c] = 0;
        }
      }
      taBuf[i] = cellTA[i];
    }
    // Glue shared edges: two neighbours measure the SAME geometric
    // edge as two independent floats, and they can round a fraction
    // apart -- a fragment in the crack belongs to no cell (the shader
    // paints it black: a straight dark line on the boundary), and
    // offset edges put the two cells' seam lines a hair apart (a
    // bright hairline). Seen on the six-world quilt, 2026-10-28; an
    // overlap epsilon traded one for the other. Instead, average
    // each shared edge into both cells as the rects upload, so the
    // boundary is one identical value by construction. Shader
    // untouched (still v6.2, byte-identical).
    var SIDE_EDGE = [0, 2, 1, 3], OPP_EDGE = [2, 0, 3, 1];
    for (i = 0; i < N; i++) {
      if (!nbrs[i]) continue;
      for (c = 0; c < 4; c++) {
        var j = nbrs[i][c];
        if (j > i) {
          var ea = SIDE_EDGE[c], eb = OPP_EDGE[c];
          var eavg = (rectBuf[i * 4 + ea] + rectBuf[j * 4 + eb]) / 2;
          rectBuf[i * 4 + ea] = eavg;
          rectBuf[j * 4 + eb] = eavg;
        }
      }
    }
    var acts = activities();
    for (i = 0; i < N * 4; i++) actBuf[i] = acts[i];
    gl.uniform1f(U.uTime, time);
    gl.uniform4f(U.uVis, vis[0], vis[1], vis[2], vis[3]);
    gl.uniform1f(U.uQA, quiltW / Math.max(1, quiltH));
    gl.uniform4fv(U.uRect, rectBuf);
    gl.uniform4fv(U.uUVR, uvBuf);
    gl.uniform1fv(U.uTA, taBuf);
    gl.uniform4fv(U.uNbr, nbrBuf);
    gl.uniform4fv(U.uAct, actBuf);
    gl.uniform4fv(U.uPhase, phaseBuf);
    gl.uniform4fv(U.uTempo, tempoBuf);
    gl.uniform4fv(U.uAmp, ampBuf);
    gl.drawArrays(gl.TRIANGLES, 0, 3);
  }
  function drawStatic() {
    if (!ready) return;
    resize();
    if (!measureLayout()) return;
    computeTargets();
    cur = target.map(function (r) { return r.slice(); });
    draw(0.001);
  }
  function tick(ts) {
    lastTickAt = performance.now();
    if (!lastTs) lastTs = ts;
    var dt = Math.min(0.05, Math.max(0, (ts - lastTs) / 1000));
    lastTs = ts;
    tSec += dt;
    var k = 1 - Math.exp(-dt / TAU);
    for (var i = 0; i < N; i++) {
      if (!cur[i] || !target[i]) continue;
      for (var c = 0; c < 4; c++) cur[i][c] += (target[i][c] - cur[i][c]) * k;
    }
    if (quiltOffset !== 0) {
      quiltOffset += (0 - quiltOffset) * k;
      if (Math.abs(quiltOffset) < 0.15) {
        quiltOffset = 0;
        quilt.style.transform = '';
        quilt.style.willChange = '';
      } else {
        quilt.style.transform = 'translateY(' + (-quiltOffset).toFixed(1) + 'px)';
      }
    }
    draw(tSec);
    if (!animating() && needsRetarget) {
      needsRetarget = false;
      stepIdx = 0;
      retarget();
    }
    if (dt > 0) { ftSum += dt * 1000; ftCount++; }
    if (ftCount >= 90) {
      if (ftSum / ftCount > 26 && stepIdx < dprSteps.length - 1 && !animating()) { stepIdx++; resize(); }
      ftSum = 0; ftCount = 0;
    }
  }
  function rafFrame(ts) {
    if (!running) return;
    lastRafAt = performance.now();
    tick(ts);
    raf = requestAnimationFrame(rafFrame);
  }
  function startLoop() {
    if (running || mq.matches) return;
    running = true; lastTs = 0;
    raf = requestAnimationFrame(rafFrame);
  }
  function stopLoop() {
    running = false;
    if (raf) cancelAnimationFrame(raf);
    if (intervalDriver) { clearInterval(intervalDriver); intervalDriver = null; }
  }
  function shouldRun() {
    return ready && !mq.matches && inView && document.visibilityState === 'visible';
  }
  function gate() {
    if (!ready) return;
    if (mq.matches) { stopLoop(); drawStatic(); return; }
    if (shouldRun()) startLoop(); else stopLoop();
  }
  // Watchdog: if rAF stalls on a device while the quilt should be
  // animating, an interval takes over so taps still move the seams.
  setInterval(function () {
    if (!shouldRun() || !running) return;
    var now = performance.now();
    if (now - lastTickAt > 700 && !intervalDriver) {
      intervalDriver = setInterval(function () { tick(performance.now()); }, 50);
    }
    if (intervalDriver && now - lastRafAt <= 700) {
      clearInterval(intervalDriver); intervalDriver = null;
    }
  }, 400);

  if (window.IntersectionObserver) {
    new IntersectionObserver(function (entries) {
      inView = entries[0].isIntersecting;
      gate();
    }, { threshold: 0.02 }).observe(quilt);
  }
  document.addEventListener('visibilitychange', gate);
  if (mq.addEventListener) mq.addEventListener('change', gate);

  var resizeTimer = 0;
  function onResize() {
    if (animating()) { needsRetarget = true; return; }
    stepIdx = 0;
    retarget();
    if (!quilt.classList.contains('open')) {
      cur = target.map(function (r) { return r.slice(); });
    }
    if (mq.matches) drawStatic();
    else if (ready) draw(tSec); // same cleared-canvas guard as open/close
  }
  if (window.ResizeObserver) {
    new ResizeObserver(function () {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(onResize, 120);
    }).observe(quilt);
  }
  window.addEventListener('resize', onResize);

  var rmTimer = null;
  new MutationObserver(function () {
    var nowOpen = quilt.classList.contains('open');
    if (!nowOpen && fixedTop && !mq.matches && ready) {
      // The quilt just teleported back into flow: counter-shift it so
      // this frame renders exactly where the fixed quilt was, then the
      // tick eases the shift away (the v3.1 FLIP, kept).
      var drop = quilt.getBoundingClientRect().top - fixedTop;
      if (drop > 1) {
        quiltOffset = drop;
        quilt.style.willChange = 'transform';
        quilt.style.transform = 'translateY(' + (-drop) + 'px)';
      }
    }
    if (nowOpen) {
      quiltOffset = 0;
      quilt.style.transform = '';
      quilt.style.willChange = '';
    }
    // Physical feedback: opening or closing a world disturbs the
    // membrane along its edges; the swell decays in draw().
    var ai = -1;
    slices.forEach(function (el, i) { if (el.classList.contains('active')) ai = i; });
    if (nowOpen && ai >= 0) { pokeEdges(ai); lastOpenIdx = ai; }
    if (!nowOpen && lastOpenIdx >= 0) { pokeEdges(lastOpenIdx); lastOpenIdx = -1; }
    retarget();
    // Flicker fix: retarget may have resized (cleared) the canvas for
    // the new fixed/in-flow geometry. Repaint synchronously, before
    // the browser composites, so the cleared canvas never shows as a
    // black frame mid-gesture.
    if (ready && !mq.matches) draw(tSec);
    if (!mq.matches || !ready) return;
    var until = performance.now() + 950;
    if (rmTimer) clearInterval(rmTimer);
    rmTimer = setInterval(function () {
      drawStatic();
      if (performance.now() > until) { clearInterval(rmTimer); rmTimer = null; }
    }, 40);
  }).observe(quilt, { attributes: true, attributeFilter: ['class'] });

  canvas.addEventListener('webglcontextlost', function (e) {
    e.preventDefault();
    stopLoop();
    ready = false;
    quilt.classList.remove('gl-live');
    canvas.style.opacity = '0';
  });
  canvas.addEventListener('webglcontextrestored', function () {
    if (buildTextures()) start();
  });

  function start() {
    ready = true;
    retarget();
    cur = target.map(function (r) { return r.slice(); });
    draw(0.001);
    // First successful frame drawn: reveal the canvas over the DOM.
    quilt.style.transform = '';
    quilt.setAttribute('data-gl', mode);
    quilt.classList.add('gl-live');
    canvas.style.opacity = '1';
    gate();
  }

  // Wait for the slices' own images (already loading as DOM <img>s),
  // then pack the atlas and start. Any failure leaves the DOM fallback.
  var pending = 0, failed = false;
  function maybeStart() {
    if (failed || pending > 0 || ready) return;
    try {
      if (buildTextures()) start();
    } catch (e) { /* texture failure: fallback stays, no gl-live */ }
  }
  slices.forEach(function (el) {
    var img = el.querySelector('img');
    if (!img) { failed = true; return; }
    if (img.complete && img.naturalWidth > 0) return;
    if (img.complete && img.naturalWidth === 0) { failed = true; return; }
    pending++;
    img.addEventListener('load', function () { pending--; maybeStart(); });
    img.addEventListener('error', function () { failed = true; });
  });
  maybeStart();
}
initDreamQuilt(document.querySelector('.quilt'), document.querySelector('.quilt canvas.dream-gl'));''' + "\n</script>\n"

# The quilt's grid metrics derive from the slice count itself: the
# stylesheet sizes rows from --rows (pairs) and the portrait column
# from --cells, so adding a pair can never strand a row outside a
# hardcoded grid (the six-world ship did exactly that: CSS still
# declared two rows / four portrait rows and row three was clipped).
_cells = latent_body.count('class="slice"')
latent_body = latent_body.replace(
    '<div class="quilt" id="quilt">',
    '<div class="quilt" id="quilt" style="--rows:%d;--cells:%d">' % ((_cells + 1) // 2, _cells))
page("dreams.html", "Dreamscape — Adam Laloge",
     "AI artwork directed by Adam Laloge. Worlds are quilted into a single grid, with liquid seams between every pair. Open one and it fills the screen while the page takes on its colors.",
     "dreams.html", latent_body, latent_js)

# ---------- Bookshelf ----------
# List-driven: add one entry per book (title, author, status, blurb) and the
# shelf renders it automatically, grouped onto a shelf per status. `style`
# (spine color, width, height, depth in px) is optional; when omitted it is
# derived deterministically from the title so new books need no design work.
BOOKS = [
    {"t": "Between Two Fires", "a": "Christopher Buehlman", "s": "The bar",
     "b": "The standard. Plague-era France, a disgraced knight, and a war between heaven and hell fought at ground level. Everything else on this shelf gets measured against it.",
     "style": ("#4a1f1f", 52, 228, 34)},
    {"t": "The Shadow of the Gods", "a": "John Gwynne", "s": "Up next",
     "b": "Grimdark with dragons, and the one that asks the least homework up front.",
     "style": ("#1f2a44", 56, 224, 36)},
    {"t": "The Rage of Dragons", "a": "Evan Winter", "s": "Up next",
     "b": "The fast one. A dragon war and a nobody fighting his way up through it.",
     "style": ("#5a2d16", 44, 208, 28)},
    {"t": "The Ruin of Kings", "a": "Jenn Lyons", "s": "Up next",
     "b": "First of A Chorus of Dragons. The main character is living under a stolen identity, and the dragons sit at the center of the story.",
     "style": ("#2e1f3d", 58, 230, 38)},
    {"t": "Of Blood and Fire", "a": "Ryan Cahill", "s": "Up next",
     "b": "Classic-shape epic with dragon riders.",
     "style": ("#6b3410", 46, 212, 30)},
    {"t": "Gardens of the Moon", "a": "Steven Erikson", "s": "Reading now",
     "b": "Malazan, book one. The deep end: a huge world that explains nothing and trusts you to keep up.",
     "style": ("#1c2b26", 60, 226, 40)},
    {"t": "The Darkness That Comes Before", "a": "R. Scott Bakker", "s": "Up next",
     "b": "The darkest of the six. Fair warning I gave myself: the dragons here are ancient history, mostly backstory.",
     "style": ("#171310", 54, 222, 36)},
]

SHELF_ORDER = ["The bar", "Reading now", "Up next", "Finished"]
SPINE_PALETTE = ["#4a1f1f", "#1f2a44", "#5a2d16", "#2e1f3d", "#6b3410",
                 "#1c2b26", "#171310", "#3d2b18", "#233026", "#33222e",
                 "#26343d", "#402a3a"]

def book_style(b):
    if b.get("style"):
        return b["style"]
    h = zlib.crc32(b["t"].encode("utf-8"))
    return (SPINE_PALETTE[h % len(SPINE_PALETTE)],
            42 + (h >> 4) % 19,      # spine width 42-60px
            206 + (h >> 9) % 27,     # height 206-232px
            28 + (h >> 14) % 13)     # depth 28-40px

def book_html(b, selected=False):
    color, _w, _h, d = book_style(b)
    return """        <button type="button" class="cov%s" style="--bd:%dpx;--cov:%s" data-title="%s" data-author="%s" data-status="%s" data-blurb="%s" aria-pressed="%s" aria-label="%s by %s">
          <span class="cov-edge cov-edge-left"></span>
          <span class="cov-edge cov-edge-right"></span>
          <span class="cov-front">
            <span class="cov-status">%s</span>
            <span class="cov-title">%s</span>
            <span class="cov-author">%s</span>
          </span>
        </button>""" % (" selected" if selected else "", d, color,
                      b["t"], b["a"], b["s"], b["b"],
                      "true" if selected else "false", b["t"], b["a"],
                      b["s"], b["t"], b["a"])

# Two shelves (Cover Flow each): "Reading" and "To read". A book's status in
# the list decides which shelf it lands on; empty shelves are not rendered.
FLOWS = [("Reading", ["Reading now", "The bar", "Finished"]),
         ("To read", ["Up next"])]

def flow_block(label, books):
    items = "\n".join(book_html(b, selected=(i == 0))
                      for i, b in enumerate(books))
    f = books[0]
    return """    <div class="flow-block">
      <p class="label flow-label">%s</p>
      <div class="flow-scene">
        <div class="flow-track">
%s
        </div>
        <p class="flow-hint">Drag or swipe to browse</p>
      </div>
      <article class="card book-detail">
        <p class="label card-label bd-status">%s</p>
        <p><strong class="bd-title">%s</strong> <span class="book-byline">by <span class="bd-author">%s</span></span></p>
        <p class="bd-blurb">%s</p>
      </article>
    </div>""" % (label, items, f["s"], f["t"], f["a"], f["b"])

_flow_blocks = []
for _label, _statuses in FLOWS:
    _group = [b for _s in _statuses for b in BOOKS if b["s"] == _s]
    if _group:
        _flow_blocks.append(flow_block(_label, _group))

bookshelf_body = """  <section id="bookshelf">
    <p class="label">Bookshelf</p>
    <h2>The bookshelf</h2>
    <p>My reading runs to historical horror, dark fantasy, and sci-fi: plagues and dragons, dead gods and far-future wars. Two shelves: what I'm reading, and what is waiting. Drag or swipe through the covers. Tap one to bring it to the front.</p>
%s
    <p class="section-note">The to-read shelf is the shortlist I'm picking between. I haven't started one yet; when I do, it moves to the top shelf.</p>
  </section>""" % "\n".join(_flow_blocks)

BOOKSHELF_JS = """<script>
(function () {
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.flow-block').forEach(function (block) {
    var track = block.querySelector('.flow-track');
    if (!track) return;
    var detail = {
      status: block.querySelector('.bd-status'),
      title: block.querySelector('.bd-title'),
      author: block.querySelector('.bd-author'),
      blurb: block.querySelector('.bd-blurb')
    };
    var items = Array.prototype.slice.call(track.querySelectorAll('.cov'));
    var centered = -1;

    function select(i) {
      if (i === centered) return;
      centered = i;
      items.forEach(function (x, j) {
        x.classList.toggle('selected', j === i);
        x.setAttribute('aria-pressed', j === i ? 'true' : 'false');
      });
      var b = items[i];
      detail.status.textContent = b.getAttribute('data-status');
      detail.title.textContent = b.getAttribute('data-title');
      detail.author.textContent = b.getAttribute('data-author');
      detail.blurb.textContent = b.getAttribute('data-blurb');
    }

    function layout() {
      var mid = track.scrollLeft + track.clientWidth / 2;
      var best = 0, bestDist = Infinity;
      items.forEach(function (it, i) {
        var c = it.offsetLeft + it.offsetWidth / 2;
        var off = (c - mid) / it.offsetWidth; // distance from center, in book widths
        var rot = Math.max(-62, Math.min(62, off * -55));
        var z = -Math.min(240, Math.abs(off) * 75);
        // Transform and z-index only: per-frame filter updates caused the jank.
        it.style.transform = 'rotateY(' + rot.toFixed(1) + 'deg) translateZ(' + z.toFixed(0) + 'px)';
        it.style.zIndex = String(100 - Math.round(Math.abs(off) * 10));
        if (Math.abs(c - mid) < bestDist) { bestDist = Math.abs(c - mid); best = i; }
      });
      select(best);
    }

    var ticking = false, settleTimer = null;
    track.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(function () { layout(); ticking = false; }); }
      // Settle: once scrolling rests, glide the nearest book the last bit
      // into center. CSS scroll-snap used to do this, but snap fought the
      // scripted wheel glide (the gallery had the same bug and the same
      // fix), so JS owns centering here too. Skipped while a wheel glide
      // or a click glide is still moving the track.
      clearTimeout(settleTimer);
      settleTimer = setTimeout(function () {
        if (wheelTarget !== null || centered < 0) return;
        var it = items[centered];
        var off = (it.offsetLeft + it.offsetWidth / 2) - (track.scrollLeft + track.clientWidth / 2);
        if (Math.abs(off) > 3) centerItem(centered, true);
      }, 150);
    }, { passive: true });
    // Wheel routing — each axis does its own job:
    // - Trackpad sideways swipe: the flow glides on deltaX, and the events
    //   are captured whole so the page never moves mid-gesture.
    // - Trackpad vertical scroll: never intercepted. The page scrolls and
    //   the flow is pinned, so diagonal drift can't wiggle it.
    // - Mouse wheel (line/page mode, or a coarse full-size first step):
    //   vertical notches convert to a sideways glide — a wheel has no
    //   sideways to give.
    // The axis is judged once per gesture from its first deltas and held
    // until the stream goes quiet (~140ms); judging event-by-event
    // flip-flopped on diagonal trackpad input.
    var wheelTarget = null, wheelRaf = null;
    var gesture = null, gestureTimer = null;
    function stopWheel() {
      wheelTarget = null;
      if (wheelRaf) { cancelAnimationFrame(wheelRaf); wheelRaf = null; }
    }
    function stepWheel() {
      if (wheelTarget === null) { wheelRaf = null; return; }
        var diff = wheelTarget - track.scrollLeft;
      if (Math.abs(diff) < 0.6) {
        track.scrollLeft = wheelTarget;
        wheelTarget = null;
        wheelRaf = null;
        return;
      }
      track.scrollLeft += diff * 0.22;
      wheelRaf = requestAnimationFrame(stepWheel);
    }
    function armGesture() {
      clearTimeout(gestureTimer);
      gestureTimer = setTimeout(function () { gesture = null; }, 140);
    }
    track.addEventListener('wheel', function (e) {
        if (e.ctrlKey) return; // trackpad pinch-zoom: not ours to take
      var dx = e.deltaX, dy = e.deltaY;
      if (e.deltaMode === 1) { dx *= 24; dy *= 24; }              // lines to px
      else if (e.deltaMode === 2) { dx *= track.clientWidth; dy *= track.clientWidth; }
      armGesture();
      if (!gesture) {
        gesture = { ax: 0, ay: 0, bx: 0, by: 0, axis: null,
                    mouse: e.deltaMode !== 0 || Math.abs(e.deltaY) >= 50 || Math.abs(e.deltaX) >= 50,
                    left: track.scrollLeft };
      }
      var g = gesture;
      g.ax += Math.abs(dx); g.ay += Math.abs(dy); g.bx += dx; g.by += dy;
      if (!g.axis) {
        if (!g.mouse && Math.max(g.ax, g.ay) < 8) return;  // too small to judge yet
        g.axis = g.ax > g.ay ? 'x' : (g.mouse ? 'convert' : 'y');
        if (g.axis === 'y') stopWheel();                   // a page scroll cancels any glide
        dx = g.bx; dy = g.by;                              // spend the buffered deltas whole
      }
      if (g.axis === 'y') {
        if (track.scrollLeft !== g.left) track.scrollLeft = g.left;
        return;
      }
      var d = g.axis === 'x' ? dx : dy;
      if (!d) return;
      var max = track.scrollWidth - track.clientWidth;
      if (max <= 0) return;
      var base = wheelTarget !== null ? wheelTarget : track.scrollLeft;
      var target = Math.max(0, Math.min(max, base + d));
      if (Math.abs(target - track.scrollLeft) < 1) { stopWheel(); return; }
      e.preventDefault();
        wheelTarget = target;
      if (reduced) {
        track.scrollLeft = wheelTarget;
        wheelTarget = null;
        return;
      }
      if (!wheelRaf) wheelRaf = requestAnimationFrame(stepWheel);
    }, { passive: false });
    ['pointerdown', 'touchstart', 'keydown'].forEach(function (ev) {
      track.addEventListener(ev, stopWheel, { passive: true });
    });
    window.addEventListener('resize', layout);

    function centerItem(i, smooth) {
      stopWheel();
      var it = items[i];
      track.scrollTo({
        left: it.offsetLeft - (track.clientWidth - it.offsetWidth) / 2,
        behavior: smooth && !reduced ? 'smooth' : 'auto'
      });
    }
    items.forEach(function (it, i) {
      it.addEventListener('click', function () { centerItem(i, true); });
    });

    centerItem(0, false);
    layout();
    // Deep link (from Atlas): #book-<slug> brings that cover to the
    // front of its shelf instead of just landing on the page.
    (function () {
      var m = /^#book-(.+)$/.exec(location.hash || '');
      if (!m) return;
      var slug = m[1], found = -1;
      items.forEach(function (it, i) {
        var t = (it.getAttribute('data-title') || '').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '');
        if (t === slug) found = i;
      });
      if (found < 0) return;
      centerItem(found, false);
      layout();
      block.scrollIntoView({ block: 'center' });
    })();
  });
})();
</script>
"""
page("bookshelf.html", "Bookshelf — Adam Laloge",
     "Adam Laloge's bookshelf: historical horror, dark fantasy, and sci-fi — what he's reading and what's next.",
     "bookshelf.html", bookshelf_body, BOOKSHELF_JS)

# ---------- Photography / Resume (verbatim sections) ----------
page("photography.html", "Photography — Adam Laloge",
     "Photographs by Adam Laloge: landscapes and sunsets.", "photography.html",
     "  " + photo_section.replace("\n", "\n  ").rstrip(),
     "<script>" + gallery_js + "</script>\n")

page("resume.html", "Resume — Adam Laloge",
     "Resume of Adam Laloge, UI/UX software engineer.", "resume.html",
     "  " + resume_section.replace("\n", "\n  ").rstrip())

# ---------- Latent Sitemap ----------
# The art visualizer, promoted to a real page: a map of the whole site
# drawn as a latent space. The map data is generated from the site's own
# content at build time (the same step prototyped in
# ~/workspace/latent-poc/build_latent_poc.py): photos and artworks are
# colored by a saturation-weighted average of the actual image, books by
# their cover color, projects in the teal family. Layout is deterministic
# (crc32 of the title), so rebuilds don't reshuffle it.
import json, math
from PIL import Image

def _vibrant_color(path):
    im = Image.open(path).convert("RGB").resize((24, 24))
    tr = tg = tb = tw = 0.0
    for r, g, b in im.getdata():
        mx, mn = max(r, g, b), min(r, g, b)
        sat = (mx - mn) / mx if mx else 0.0
        w = 0.15 + sat * 1.6
        tr += r * w; tg += g * w; tb += b * w; tw += w
    r, g, b = tr / tw, tg / tw, tb / tw
    mx = max(r, g, b)
    if mx > 1:
        f = min(2.4, 215.0 / mx)
        r, g, b = r * f, g * f, b * f
    return [int(min(255, r)), int(min(255, g)), int(min(255, b))]

def _hex_rgb(h):
    return [int(h[i:i + 2], 16) for i in (1, 3, 5)]

def _lighten(rgb, amt):
    return [int(c + (255 - c) * amt) for c in rgb]

def _jitter(title, span):
    h = zlib.crc32(title.encode("utf-8"))
    return ((h % 1000) / 1000.0 - 0.5) * 2 * span

def _slug(title):
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")


# ---------- Blog ----------
# Posts are Markdown files in posts/, named YYYY-MM-DD-slug.md with a
# small front-matter block (title, date, description, optional
# draft: true). The generator renders the index, one page per post,
# the RSS feed, the sitemap entries and the Atlas points -- add a
# file, rebuild, and the post appears everywhere it should. Nothing
# about a post is hand-listed anywhere else, on purpose: hand-kept
# lists go stale silently.
import datetime as _dt
import email.utils as _eu
from html import escape as _esc
import markdown as _md

POSTS_DIR = os.path.join(SITE, "posts")
BLOG_DESC = "Blog by Adam Laloge: notes and essays on building software, testing, design, and whatever else is on the workbench."


def _fm_value(fm, key, default=""):
    m = re.search(r"^%s:\s*(.+)$" % key, fm, re.M)
    return m.group(1).strip().strip('"').strip("'") if m else default


def load_posts():
    posts = []
    if not os.path.isdir(POSTS_DIR):
        return posts
    for name in sorted(os.listdir(POSTS_DIR)):
        if not name.endswith(".md"):
            continue
        raw = open(os.path.join(POSTS_DIR, name), encoding="utf-8").read()
        m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
        if not m:
            continue
        fm, body = m.groups()
        if _fm_value(fm, "draft").lower() == "true":
            continue
        stem = name[:-3]
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", stem)
        try:
            d = _dt.date.fromisoformat(_fm_value(fm, "date"))
        except ValueError:
            dm = re.match(r"(\d{4})-(\d{2})-(\d{2})-", stem)
            if not dm:
                continue
            d = _dt.date(int(dm.group(1)), int(dm.group(2)), int(dm.group(3)))
        words = len(body.split())
        # Blog layout system: the first paragraph renders as the lede,
        # and any paragraph opening with a bold "Lesson N:" lead renders
        # as a callout card. Authors opt in purely by writing that way;
        # every post inherits the treatment (styles: .post-body .lede /
        # .lesson, plus .statband / .figbox / .seefirst raw-HTML blocks —
        # .seefirst is an invitation card linking out to the thing the
        # post is about, placed by the author at the top of the body).
        _html = _md.markdown(body, extensions=["extra"])
        _html = _html.replace("<p>", '<p class="lede">', 1)
        _html = _html.replace("<p><strong>Lesson", '<p class="lesson"><strong>Lesson')
        posts.append({
            "slug": slug,
            "fname": "blog-" + slug + ".html",
            "title": _fm_value(fm, "title", slug.replace("-", " ").title()),
            "desc": _fm_value(fm, "description"),
            "date": d,
            "date_long": d.strftime("%B ") + str(d.day) + d.strftime(", %Y"),
            "mins": max(1, -(-words // 200)),
            "html": _html,
        })
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


POSTS = load_posts()


def blog_index_body():
    rows = []
    for p in POSTS:
        rows.append("""    <article class="post-card">
      <h2><a href="%s">%s</a></h2>
      <p class="post-meta">%s &middot; %d min read</p>
      <p>%s</p>
    </article>""" % (p["fname"], _esc(p["title"]), p["date_long"], p["mins"], _esc(p["desc"])))
    listing = "\n".join(rows) if rows else "    <p>Nothing here yet.</p>"
    return """  <section class="blog-head">
    <h1>Blog</h1>
    <p class="intro">Notes and essays, newest first. Short field notes and longer pieces run on the same rails here.</p>
  </section>
  <section class="post-list">
%s
  </section>""" % listing


def blog_post_body(p):
    return """  <article class="post">
    <p class="post-meta">%s &middot; %d min read</p>
    <h1>%s</h1>
    <div class="post-body">
%s
    </div>
    <p class="post-foot"><a href="blog.html">&larr; All posts</a></p>
  </article>""" % (p["date_long"], p["mins"], _esc(p["title"]), p["html"])


def write_feed():
    items = []
    for p in POSTS:
        dt = _dt.datetime(p["date"].year, p["date"].month, p["date"].day, 12, 0, tzinfo=_dt.timezone.utc)
        items.append("""    <item>
      <title>%s</title>
      <link>https://adamlaloge.com/%s</link>
      <guid isPermaLink="true">https://adamlaloge.com/%s</guid>
      <pubDate>%s</pubDate>
      <description>%s</description>
    </item>""" % (_esc(p["title"]), p["fname"], p["fname"], _eu.format_datetime(dt), _esc(p["desc"])))
    feed = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Adam Laloge - Blog</title>
    <link>https://adamlaloge.com/blog.html</link>
    <description>%s</description>
%s
  </channel>
</rss>
""" % (BLOG_DESC, "\n".join(items))
    open(os.path.join(SITE, "feed.xml"), "w", encoding="utf-8").write(feed)
    print("wrote feed.xml", len(feed))


def write_sitemap():
    path = os.path.join(SITE, "sitemap.xml")
    existing = open(path, encoding="utf-8").read()
    have = set(re.findall(r"<loc>([^<]+)</loc>", existing))
    blocks = re.findall(r"  <url>.*?</url>\n", existing)
    latest = POSTS[0]["date"].isoformat() if POSTS else _dt.date.today().isoformat()
    new = []
    cand = [("https://adamlaloge.com/blog.html", latest, "0.7")]
    cand += [("https://adamlaloge.com/" + p["fname"], p["date"].isoformat(), "0.6") for p in POSTS]
    for loc, lastmod, prio in cand:
        if loc not in have:
            new.append('  <url><loc>%s</loc><lastmod>%s</lastmod><priority>%s</priority></url>\n' % (loc, lastmod, prio))
    out = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "".join(blocks) + "".join(new) + "</urlset>\n")
    open(path, "w", encoding="utf-8").write(out)
    print("wrote sitemap.xml", len(out))



def latent_map_data():
    items = []
    group_angle = {"sunsets": -90, "shoreline": 0, "landscapes": 90, "details": 180}
    photos_block = re.search(r"var PHOTOS = \[(.*?)\];", gallery_js, re.S).group(1)
    for m in re.finditer(r"src: '(photos/[^']+)',\s+title: '([^']+)',\s+group: '([^']+)'", photos_block):
        src, title, group = m.groups()
        ang = math.radians(group_angle.get(group, 0) + _jitter(title, 26))
        rad = 0.052 + (zlib.crc32(title.encode()) % 100) / 100.0 * 0.075
        items.append({"kind": "photo", "title": title, "sub": group,
                      "rgb": _vibrant_color(os.path.join(SITE, src)), "size": 19,
                      "dx": round(math.cos(ang) * rad, 4), "dy": round(math.sin(ang) * rad * 0.78, 4),
                      "region": "photography", "href": "photography.html#photo-" + _slug(title)})
    for i, b in enumerate(BOOKS):
        rgb = _lighten(_hex_rgb(b["style"][0] if b.get("style") else "#3d2b18"), 0.34)
        if b["s"] == "The bar":
            dx, dy = 0.0, -0.055
        else:
            ang = math.radians(-160 + i * 42)
            dx, dy = math.cos(ang) * 0.075, math.sin(ang) * 0.055
        items.append({"kind": "book", "title": b["t"], "sub": b["s"] + " · " + b["a"],
                      "rgb": rgb, "size": 18, "dx": round(dx, 4), "dy": round(dy, 4),
                      "region": "bookshelf", "href": "bookshelf.html#book-" + _slug(b["t"])})
    # Worlds derive from the Dreamscape slices declared in this
    # file, so a new pair joins the map the day it ships.
    src_self = open(os.path.abspath(__file__)).read()
    world_hits = re.findall(r'<img src="art/([\w.-]+\.jpg)"[^>]*>\s*<span class="slice-title">([^<]+)</span>', src_self)
    nw = len(world_hits)
    for wi, (fname, title) in enumerate(world_hits):
        frac = (wi + 0.5) / nw if nw else 0.5
        items.append({"kind": "world", "title": title, "sub": "Dreamscape",
                      "rgb": _vibrant_color(os.path.join(SITE, "art", fname)), "size": 33,
                      "dx": round((frac - 0.5) * 0.19, 4), "dy": -0.04 if wi % 2 == 0 else 0.04,
                      "region": "worlds", "href": "dreams.html"})
    src_text = open(os.path.abspath(__file__)).read()
    for m in re.finditer(r'project\("(\w+)\.html", "([^"]+)", "([^"]+)"', src_text):
        slug, name, status = m.groups()
        h = zlib.crc32(name.encode())
        ang = math.radians(h % 360)
        items.append({"kind": "project", "title": name, "sub": status,
                      "rgb": _lighten([94, 234, 212], 0.1 + (h % 40) / 100.0), "size": 22,
                      "dx": round(math.cos(ang) * 0.07, 4), "dy": round(math.sin(ang) * 0.05, 4),
                      "region": "projects", "href": slug + ".html"})
    for i, p in enumerate(POSTS):
        h = zlib.crc32(p["title"].encode())
        ang = math.radians(-160 + i * 42)
        items.append({"kind": "post", "title": p["title"], "sub": "Blog \u00b7 " + p["date"].strftime("%b %Y"),
                      "rgb": _lighten([150, 130, 255], 0.1 + (h % 30) / 100.0), "size": 18,
                      "dx": round(math.cos(ang) * 0.075, 4), "dy": round(math.sin(ang) * 0.055, 4),
                      "region": "writing", "href": p["fname"]})
    # Clusters breathe a tad: each region's offsets scale out from
    # their own centroid, then a deterministic relaxation enforces a
    # minimum separation so no two points sit on top of each other.
    by_region = {}
    for it in items:
        by_region.setdefault(it["region"], []).append(it)
    for lst in by_region.values():
        cx = sum(i["dx"] for i in lst) / len(lst)
        cy = sum(i["dy"] for i in lst) / len(lst)
        for i in lst:
            i["dx"] = round(cx + (i["dx"] - cx) * 1.3, 4)
            i["dy"] = round(cy + (i["dy"] - cy) * 1.3, 4)
        for _pass in range(80):
            moved = False
            for a in range(len(lst)):
                for b in range(a + 1, len(lst)):
                    ddx = lst[b]["dx"] - lst[a]["dx"]
                    ddy = lst[b]["dy"] - lst[a]["dy"]
                    d2 = ddx * ddx + ddy * ddy
                    if d2 < 0.001024:  # 0.032 ** 2
                        d = math.sqrt(d2)
                        if d < 0.0005:
                            ddx, ddy, d = 0.001, 0.0, 0.001
                        push = (0.032 - d) / 2 + 0.001
                        ux, uy = ddx / d, ddy / d
                        lst[a]["dx"] -= ux * push; lst[a]["dy"] -= uy * push
                        lst[b]["dx"] += ux * push; lst[b]["dy"] += uy * push
                        moved = True
            if not moved:
                break
        for i in lst:
            i["dx"] = round(i["dx"], 4); i["dy"] = round(i["dy"], 4)

    regions = {
        # Fog hues are fixed saturated anchors, not averages of the
        # items' colors -- averaging a dozen hues lands on brown-gray.
        # Composed like a nebula: teal upper-left, rose upper-right,
        # ember lower-left, gold lower-right.
        "photography": {"label": "PHOTOGRAPHY", "fx": 0.30, "fy": 0.44, "rgb": [34, 190, 205]},
        "bookshelf": {"label": "BOOKSHELF", "fx": 0.76, "fy": 0.40, "rgb": [216, 96, 158]},
        "worlds": {"label": "DREAMSCAPE", "fx": 0.24, "fy": 0.80, "rgb": [228, 96, 52]},
        "projects": {"label": "PROJECTS", "fx": 0.74, "fy": 0.79, "rgb": [226, 182, 92]},
        "writing": {"label": "WRITING", "fx": 0.50, "fy": 0.32, "rgb": [150, 130, 255]},
    }
    return {"regions": regions, "items": items}

LATENT_DATA = latent_map_data()

def _map_group(heading, page_href, region):
    lis = "\n".join(
        '        <li><a href="%s">%s</a></li>' % (it["href"], it["title"])
        for it in LATENT_DATA["items"] if it["region"] == region)
    return ('      <div class="map-group">\n'
            '        <h3><a href="%s">%s</a></h3>\n'
            '        <ul>\n%s\n        </ul>\n'
            '      </div>') % (page_href, heading, lis)

sitemap_body = """  <canvas id="latent-map" aria-hidden="true"></canvas>
  <div id="latent-hit"></div>
  <div class="latent-glass-layer" aria-hidden="true" style="background: radial-gradient(60% 50% at 30% 44%, rgba(34, 190, 205, 0.27), rgba(34, 190, 205, 0) 70%), radial-gradient(55% 45% at 76% 40%, rgba(216, 96, 158, 0.25), rgba(216, 96, 158, 0) 70%), radial-gradient(60% 50% at 24% 80%, rgba(228, 96, 52, 0.27), rgba(228, 96, 52, 0) 70%), radial-gradient(55% 45% at 74% 79%, rgba(226, 182, 92, 0.23), rgba(226, 182, 92, 0) 70%), rgba(6, 8, 16, 0.47);"></div>
  <script>document.body.classList.add('sitemap-body');</script>
  <div class="sitemap-flow">
  <section class="latent-intro">
    <div class="latent-glass latent-phead">
      <p class="label">Sitemap</p>
      <h1>Atlas</h1>
      <p class="phead-note">Drag to explore &middot; tap a point to select it &middot; tap again to open it</p>
    </div>
    <button class="latent-scrollzone" id="scroll-zone" type="button" aria-label="Scroll down to the list">
      <span class="zone-label">Scroll for the list</span>
      <span class="cue-arrow" aria-hidden="true"><i></i><i></i></span>
    </button>
  </section>
  <section class="sitemap-list-sec">
    <h2>Everything, as a list</h2>
    <p class="section-note">The same map with the magic turned off: every piece of the site, grouped the way the space groups it.</p>
    <div class="map-groups">
/*__GROUPS__*/
    </div>
  </section>
  </div>
""".replace("/*__GROUPS__*/", "\n".join([
    _map_group("Photography", "photography.html", "photography"),
    _map_group("Bookshelf", "bookshelf.html", "bookshelf"),
    _map_group("Blog", "blog.html", "writing"),
    _map_group("Dreamscape", "dreams.html", "worlds"),
    _map_group("Projects", "work.html", "projects"),
]))


LATENT_MAP_JS = r"""<script>
(function () {
  'use strict';
  // Baked in at build time by build_pages.py: every item on this site is
  // a point here, colored by a measured feature of itself. The canvas is
  // a fixed full-page background; scrolling fades the map's content out
  // and raises a frosted-glass layer with the plain list on it.
  var DATA = /*__DATA__*/null;
  var canvas = document.getElementById('latent-map');
  var glassEl = document.querySelector('.latent-glass-layer');
  var hit = document.getElementById('latent-hit');
  var zone = document.getElementById('scroll-zone');
  var cueEl = zone;
  if (!canvas || !DATA) return;
  var ctx = canvas.getContext('2d');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W = 0, H = 0, DPR = 1;
  var fogC = null, fctx = null, FOGRES = 0.65;

  function boost(rgb) {
    var avg = (rgb[0] + rgb[1] + rgb[2]) / 3;
    var out = rgb.map(function (c) { return Math.max(0, Math.min(255, Math.round(avg + (c - avg) * 2.55))); });
    var mx = Math.max(out[0], out[1], out[2]);
    if (mx > 1) { var f = Math.min(2.0, 225 / mx); out = out.map(function (c) { return Math.min(255, Math.round(c * f)); }); }
    return out;
  }
  function makeGlow(rgb) {
    var c = document.createElement('canvas'); c.width = c.height = 64;
    var g = c.getContext('2d');
    var grad = g.createRadialGradient(32, 32, 0, 32, 32, 32);
    grad.addColorStop(0, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.9)');
    grad.addColorStop(0.22, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.42)');
    grad.addColorStop(0.58, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.09)');
    grad.addColorStop(1, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0)');
    g.fillStyle = grad; g.fillRect(0, 0, 64, 64);
    return c;
  }
  function makeSpark(rgb) {
    var c = document.createElement('canvas'); c.width = c.height = 48;
    var g = c.getContext('2d');
    g.translate(24, 24);
    var grad = g.createRadialGradient(0, 0, 0, 0, 0, 24);
    grad.addColorStop(0, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.95)');
    grad.addColorStop(0.4, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0.4)');
    grad.addColorStop(1, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0)');
    g.fillStyle = grad;
    g.beginPath();
    g.moveTo(0, -24); g.quadraticCurveTo(2.5, -2.5, 24, 0); g.quadraticCurveTo(2.5, 2.5, 0, 24);
    g.quadraticCurveTo(-2.5, 2.5, -24, 0); g.quadraticCurveTo(-2.5, -2.5, 0, -24);
    g.fill();
    return c;
  }
  var probeSprite = makeGlow([45, 212, 191]);
  var cometSprite = makeSpark([45, 212, 191]);

  // The dynamic nebula: the demo's Improved implementation, lifted
  // whole. Shared periodic fbm + ridge fields are sampled as ALPHA
  // MASKS and colorized by a three-stop palette per region (deep,
  // anchor, hot). Density throws the field's bottom third away
  // (smoothstep 0.36-0.80) -- that is where the contrast lives:
  // transparent depths, structured bodies, hot filaments.
  function mulberry32(a) { return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; }; }
  function clampF(v, a, b) { return v < a ? a : (v > b ? b : v); }
  function lerpF(a, b, t) { return a + (b - a) * t; }
  function smoothstepF(a, b, x) { var t = clampF((x - a) / (b - a), 0, 1); return t * t * (3 - 2 * t); }
  function paletteAt(pal, t) {
    var c1 = t < 0.5 ? pal[0] : pal[1], c2 = t < 0.5 ? pal[1] : pal[2], u = t < 0.5 ? t * 2 : (t - 0.5) * 2;
    return [lerpF(c1[0], c2[0], u), lerpF(c1[1], c2[1], u), lerpF(c1[2], c2[2], u)];
  }
  var PALS = {
    photography: [[36, 84, 186], [34, 190, 205], [178, 246, 240]],
    bookshelf: [[146, 62, 198], [216, 96, 158], [255, 198, 226]],
    worlds: [[166, 34, 46], [228, 96, 52], [255, 216, 148]],
    projects: [[216, 118, 36], [226, 182, 92], [255, 242, 198]],
    writing: [[72, 52, 168], [150, 130, 255], [226, 218, 255]]
  };
  var fbmField = null, ridgeField = null, distArr = null, angBinArr = null;
  var improvedSprites = {}, filamentSprites = {}, dustFieldSprite = null, improvedReady = false;
  function makePeriodicNoise(freq, seed) {
    var r = mulberry32(seed), grid = [];
    for (var i = 0; i < freq * freq; i++) grid.push(r());
    return function (u, v) {
      var x = u * freq, y = v * freq;
      var x0 = Math.floor(x), y0 = Math.floor(y);
      var fx = x - x0, fy = y - y0;
      var sx = fx * fx * (3 - 2 * fx), sy = fy * fy * (3 - 2 * fy);
      function at(a, b) { return grid[(((b % freq) + freq) % freq) * freq + (((a % freq) + freq) % freq)]; }
      return lerpF(lerpF(at(x0, y0), at(x0 + 1, y0), sx), lerpF(at(x0, y0 + 1), at(x0 + 1, y0 + 1), sx), sy);
    };
  }
  function buildFields(size) {
    var octF = [makePeriodicNoise(3, 11), makePeriodicNoise(6, 23), makePeriodicNoise(12, 37), makePeriodicNoise(24, 51)];
    var octR = [makePeriodicNoise(3, 71), makePeriodicNoise(6, 83), makePeriodicNoise(12, 97)];
    fbmField = new Float32Array(size * size); ridgeField = new Float32Array(size * size);
    var gains = [1, 0.5, 0.25, 0.125], rGains = [1, 0.5, 0.25];
    for (var y = 0; y < size; y++) for (var x = 0; x < size; x++) {
      var u = x / size, v = y / size, f = 0, rg = 0, i;
      for (i = 0; i < 4; i++) f += gains[i] * octF[i](u, v); f /= 1.875;
      for (i = 0; i < 3; i++) { var n = octR[i](u, v); rg += rGains[i] * (1 - Math.abs(2 * n - 1)); } rg /= 1.75;
      fbmField[y * size + x] = f; ridgeField[y * size + x] = rg;
    }
  }
  function buildGeom(size) {
    distArr = new Float32Array(size * size); angBinArr = new Uint16Array(size * size);
    var half = size / 2;
    for (var y = 0; y < size; y++) for (var x = 0; x < size; x++) {
      var i = y * size + x, dx = (x - half) / half, dy = (y - half) / half;
      distArr[i] = Math.sqrt(dx * dx + dy * dy);
      angBinArr[i] = Math.floor((Math.atan2(dy, dx) + Math.PI) / (2 * Math.PI) * 719.99);
    }
  }
  function edgeTable(ph1, ph2) {
    var e = new Float32Array(720);
    for (var b = 0; b < 720; b++) { var ang = b / 720 * 2 * Math.PI - Math.PI; e[b] = 0.86 + 0.16 * Math.sin(ang * 3 + ph1) + 0.12 * Math.sin(ang * 5 + ph2) + 0.08 * Math.sin(ang * 8 + ph1 * 2); }
    return e;
  }
  function wrappedIdx(size, off) { var a = new Int32Array(size); for (var i = 0; i < size; i++) { var v = i + off; a[i] = v >= size ? v - size : (v < 0 ? v + size : v); } return a; }
  function buildImprovedSprite(pal, fx, fy, spriteIdx, size) {
    var c = document.createElement('canvas'); c.width = c.height = size; var g = c.getContext('2d');
    var img = g.createImageData(size, size), d = img.data;
    var ox = (spriteIdx * 67 + (pal[0][0] % 40)) % size, oy = (spriteIdx * 41 + 13) % size, ox2 = (ox * 2) % size;
    var colIdx = wrappedIdx(size, ox), rowIdx = wrappedIdx(size, oy), colIdx2 = wrappedIdx(size, ox2);
    var edge = edgeTable(spriteIdx * 1.93 + fx * 9, spriteIdx * 3.71 + fy * 7);
    for (var y = 0; y < size; y++) {
      var rowBase = rowIdx[y] * size, rowBaseSrc = y * size;
      for (var x = 0; x < size; x++) {
        var i = rowBaseSrc + x, pi = i * 4;
        var v = fbmField[rowBase + colIdx[x]];
        var rd = ridgeField[rowBase + colIdx2[x]];
        var fall = smoothstepF(edge[angBinArr[i]], edge[angBinArr[i]] - 0.55, distArr[i]);
        if (fall <= 0.001) { d[pi + 3] = 0; continue; }
        var dens = smoothstepF(0.36, 0.80, v);
        var alpha = clampF(dens * 1.15 - 0.08, 0, 1) * fall;
        var fil = smoothstepF(0.72, 0.95, rd) * fall;
        var t = clampF(dens + 0.35 * fil, 0, 1);
        var col = paletteAt(pal, t);
        alpha = clampF(alpha + fil * 0.25, 0, 1);
        if (alpha <= 0.003) { d[pi + 3] = 0; continue; }
        for (var ch = 0; ch < 3; ch++) {
          var cv = col[ch]; var cf = Math.min(1, cv, 255 - cv); if (cf < 0) cf = 0;
          d[pi + ch] = clampF(cv + (Math.random() + Math.random() - 1) * cf, 0, 255);
        }
        d[pi + 3] = alpha * 255;
      }
    }
    g.putImageData(img, 0, 0); return c;
  }
  function buildFilamentSprite(pal, idx, size) {
    var c = document.createElement('canvas'); c.width = c.height = size; var g = c.getContext('2d');
    var img = g.createImageData(size, size), d = img.data;
    var colIdx = wrappedIdx(size, (idx * 89 + 31) % size), rowIdx = wrappedIdx(size, (idx * 53 + 7) % size);
    for (var y = 0; y < size; y++) {
      var rowBase = rowIdx[y] * size, rowBaseSrc = y * size;
      for (var x = 0; x < size; x++) {
        var i = rowBaseSrc + x, pi = i * 4;
        var rd = ridgeField[rowBase + colIdx[x]];
        var fall = smoothstepF(1.0, 0.35, distArr[i]);
        var a = smoothstepF(0.78, 0.97, rd) * fall;
        if (a <= 0.01) { d[pi + 3] = 0; continue; }
        var col = paletteAt(pal, 0.65 + 0.35 * a);
        d[pi] = col[0]; d[pi + 1] = col[1]; d[pi + 2] = col[2]; d[pi + 3] = a * 255;
      }
    }
    g.putImageData(img, 0, 0); return c;
  }
  function buildDustSprite(size) {
    var c = document.createElement('canvas'); c.width = c.height = size; var g = c.getContext('2d');
    var img = g.createImageData(size, size), d = img.data;
    var colIdx = wrappedIdx(size, 120 % size), rowIdx = wrappedIdx(size, 45 % size);
    for (var y = 0; y < size; y++) {
      var rowBase = rowIdx[y] * size, rowBaseSrc = y * size;
      for (var x = 0; x < size; x++) {
        var i = rowBaseSrc + x, pi = i * 4;
        var rd = ridgeField[rowBase + colIdx[x]];
        var fall = smoothstepF(1.05, 0.3, distArr[i]);
        var a = smoothstepF(0.74, 0.96, rd) * fall;
        d[pi] = 255; d[pi + 1] = 255; d[pi + 2] = 255; d[pi + 3] = a * 255;
      }
    }
    g.putImageData(img, 0, 0); return c;
  }
  // Regions added by the generator may have no hand-tuned palette;
  // derive a 3-stop ramp from the region's own colour so a new
  // region can never take the map down or arrive unstyled.
  function derivePal(rgb) {
    var deep = rgb.map(function (c) { return Math.round(c * 0.42); });
    var pale = rgb.map(function (c) { return Math.round(c + (255 - c) * 0.72); });
    return [deep, rgb.slice(), pale];
  }

  function generateImproved() {
    var size = 256;
    buildFields(size); buildGeom(size);
    var t0 = performance.now();
    var probeSet = [];
    for (var k = 0; k < 4; k++) probeSet.push(buildImprovedSprite(PALS.photography, 0.30, 0.44, k, size));
    if ((performance.now() - t0) * 4.2 > 200) { size = 192; buildFields(size); buildGeom(size); probeSet = null; }
    Object.keys(DATA.regions).forEach(function (k) {
      var r = DATA.regions[k], pal = PALS[k] || derivePal(r.rgb), a = [], f = [];
      for (var i2 = 0; i2 < 4; i2++) a.push(probeSet && k === 'photography' ? probeSet[i2] : buildImprovedSprite(pal, r.fx, r.fy, i2, size));
      for (var j2 = 0; j2 < 2; j2++) f.push(buildFilamentSprite(pal, j2, size));
      improvedSprites[k] = a; filamentSprites[k] = f;
    });
    dustFieldSprite = buildDustSprite(size);
    improvedReady = true;
  }
  // Living weather: 9 advecting stamps + 1 huge faint ambient wash
  // per region. Centres ride the same wander current the points use,
  // held by a soft home spring weak enough that border stamps stray
  // into neighbouring hues -- screen overlaps mix the intermediate
  // colours on their own. Homes themselves orbit slowly.
  var fogStamps = {}, allStamps = [], fogTime = -1;
  function buildFogStamps() {
    fogStamps = {}; allStamps = [];
    var r = mulberry32(2027);
    Object.keys(DATA.regions).forEach(function (k) {
      var arr = [];
      arr.push({ key: k, wash: true, bx: (r() * 2 - 1) * 0.08, by: (r() * 2 - 1) * 0.08, x: -1, y: -1, vx: 0, vy: 0, wx: 0, wy: 0, sizeMul: 2.9, alpha: 0.065, rot: r() * 6.283, rotV: (r() < 0.5 ? -1 : 1) * 0.0009, ph: r() * 6.283, sp: 0.4 + r() * 0.5, spr: 1, bright: 0, orbit: 14 });
      for (var k2 = 0; k2 < 9; k2++) {
        var ang = r() * 6.283, rad = Math.pow(r(), 0.65);
        arr.push({ key: k, wash: false, bx: Math.cos(ang) * rad * 0.36, by: Math.sin(ang) * rad * 0.32, x: -1, y: -1, vx: 0, vy: 0, wx: 0, wy: 0, sizeMul: 1.25 + r() * 0.75, alpha: 0.16 + r() * 0.10, rot: r() * 6.283, rotV: (r() < 0.5 ? -1 : 1) * (0.0006 + r() * 0.0012), ph: r() * 6.283, sp: 0.5 + r() * 0.7, spr: k2 % 4, bright: 0, orbit: 30 + r() * 110 });
      }
      fogStamps[k] = arr;
      for (var j = 0; j < arr.length; j++) allStamps.push(arr[j]);
    });
  }
  function stepFogStamps(dt, tSec) {
    if (!allStamps.length) return;
    if (fogTime < 0) fogTime = tSec; else fogTime += dt;
    var minWH = Math.min(W, H), f60 = dt * 60;
    for (var si = 0; si < allStamps.length; si++) {
      var s = allStamps[si], reg = DATA.regions[s.key];
      var hx = reg.cx + s.bx * minWH + Math.sin(fogTime * 0.017 * s.sp + s.ph) * s.orbit;
      var hy = reg.cy + s.by * minWH + Math.cos(fogTime * 0.013 * s.sp + s.ph * 1.3) * s.orbit * 0.8;
      if (s.x < 0) { s.x = hx; s.y = hy; }
      if (dt > 0) {
        var ang = Math.sin(s.x * 0.0016 + fogTime * 0.21) * 1.7 + Math.cos(s.y * 0.0019 - fogTime * 0.17) * 1.7 + Math.sin((s.x + s.y) * 0.0006 + fogTime * 0.07) * 0.9;
        var adv = s.wash ? 0.004 : 0.009;
        s.vx += Math.cos(ang) * adv * f60; s.vy += Math.sin(ang) * adv * f60;
        s.vx += (hx - s.x) * 0.00015 * f60; s.vy += (hy - s.y) * 0.00015 * f60;
        var dampF2 = Math.pow(0.95, f60);
        s.vx *= dampF2; s.vy *= dampF2;
        s.x += s.vx * f60 + s.wx * f60; s.y += s.vy * f60 + s.wy * f60;
        var wakeDamp = Math.pow(0.955, f60);
        s.wx *= wakeDamp; s.wy *= wakeDamp;
        s.rot += s.rotV * dt;
        var bTarget = 0;
        if (probe.active && probe.x > -500) {
          var pdx = s.x - probe.x, pdy = s.y - probe.y, pd2 = Math.sqrt(pdx * pdx + pdy * pdy);
          if (pd2 < 200) {
            var fall = 1 - pd2 / 200;
            s.wx += probeVx * 60 * dt * fall * 0.5; s.wy += probeVy * 60 * dt * fall * 0.5;
            bTarget = fall;
          }
        }
        s.bright += (bTarget - s.bright) * Math.min(1, dt * (bTarget > s.bright ? 6 : 2));
      }
    }
  }

  // Living grain: four noise tiles cycled at 1:1 -- the researched
  // counter to 8-bit banding in the painting's smooth gradients.
  var grainTiles = [], grainPats = null;
  for (var gi = 0; gi < 4; gi++) {
    var gc = document.createElement('canvas'); gc.width = gc.height = 140;
    var gg = gc.getContext('2d');
    var gid = gg.createImageData(140, 140);
    for (var gq = 0; gq < gid.data.length; gq += 4) {
      var gv = 116 + Math.floor(Math.random() * 24);
      gid.data[gq] = gid.data[gq + 1] = gid.data[gq + 2] = gv; gid.data[gq + 3] = 255;
    }
    gg.putImageData(gid, 0, 0);
    grainTiles.push(gc);
  }

  var regionKeys = Object.keys(DATA.regions);
  regionKeys.forEach(function (k, i) {
    var r = DATA.regions[k];
    r.key = k; r.seed = i * 1.73 + 0.6; r.cx = 0; r.cy = 0;
    r.anchor = !!r.rgb; // baked-in saturated fog hue beats the average
    if (!r.rgb) r.rgb = [120, 120, 160];
  });

  var items = DATA.items.map(function (d) {
    var rgb = boost(d.rgb);
    return {
      kind: d.kind, title: d.title, sub: d.sub, rgb: rgb, size: d.size,
      dx: d.dx, dy: d.dy, region: d.region, href: d.href,
      sprite: makeGlow(rgb),
      css: 'rgb(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ')',
      x: 0, y: 0, vx: 0, vy: 0, lit: 0, flash: 0, ph: Math.random() * Math.PI * 2
    };
  });
  regionKeys.forEach(function (k) {
    if (DATA.regions[k].anchor) return; // anchored fog hue stands
    var list = items.filter(function (p) { return p.region === k; });
    if (!list.length) return;
    var r = [0, 0, 0];
    list.forEach(function (p) { r[0] += p.rgb[0]; r[1] += p.rgb[1]; r[2] += p.rgb[2]; });
    DATA.regions[k].rgb = [Math.round(r[0] / list.length), Math.round(r[1] / list.length), Math.round(r[2] / list.length)];
  });
  generateImproved();
  buildFogStamps();

  var filler = [];
  var seed = 987654321;
  function rnd() { seed = (seed * 1103515245 + 12345) & 0x7fffffff; return seed / 0x7fffffff; }
  function buildFiller() {
    filler = [];
    var n = Math.round(Math.min(1050, Math.max(420, W * H / 2100)));
    for (var i = 0; i < n; i++) {
      var src = items[Math.floor(rnd() * items.length)];
      filler.push({ hx: rnd(), hy: rnd(), x: 0, y: 0, vx: 0, vy: 0, sprite: src.sprite, rgb: src.rgb, s: 3 + rnd() * 8, ph: rnd() * Math.PI * 2, lit: 0, flash: 0 });
    }
  }
  var stars = [];
  function buildStars() {
    stars = [];
    var n = Math.round(Math.min(560, Math.max(220, W * H / 3400)));
    for (var i = 0; i < n; i++) {
      var r = rnd();
      var tintRoll = rnd();
      stars.push({
        hx: rnd(), hy: rnd(),
        s: r < 0.7 ? 1 : (r < 0.95 ? 1.7 : 2.5),
        a: 0.24 + rnd() * 0.52, ph: rnd() * Math.PI * 2, sp: 0.3 + rnd() * 1.1,
        tint: tintRoll < 0.1 ? '255,227,179' : (tintRoll < 0.22 ? '207,228,255' : '255,255,255')
      });
    }
  }
  var sparks = [];
  function buildSparks() {
    sparks = [];
    for (var i = 0; i < 48; i++) { var sit = items[Math.floor(Math.random() * items.length)]; sparks.push({ x: Math.random() * W, y: Math.random() * H, s: 10 + Math.random() * 24, ph: Math.random() * Math.PI * 2, sp: 0.4 + Math.random() * 1.0, sprite: makeSpark(sit.rgb) }); }
  }

  // The constellation web: each point keeps faint permanent threads
  // to its two nearest neighbors in its own region, so the map reads
  // as a connected space even when the probe is somewhere else. The
  // probe's bright threads layer on top of these.
  var webPairs = [];
  (function () {
    var seen = {};
    items.forEach(function (p, i) {
      var near = items.map(function (q, j) {
        if (j === i || q.region !== p.region) return null;
        var ddx = q.dx - p.dx, ddy = q.dy - p.dy;
        return { j: j, d: ddx * ddx + ddy * ddy };
      }).filter(Boolean).sort(function (a, b) { return a.d - b.d; }).slice(0, 2);
      near.forEach(function (nb) {
        var key = Math.min(i, nb.j) + '-' + Math.max(i, nb.j);
        if (!seen[key]) { seen[key] = 1; webPairs.push([items[i], items[nb.j]]); }
      });
    });
  })();

  var probe = { x: 0, y: 0, tx: 0, ty: 0, active: false, last: 0 };
  var trail = [];
  var bursts = [];
  var comets = [];
  var nextComet = 4000, nextAuto = 5000, nextFixate = 8000;
  var fixate = null;
  var probeVx = 0, probeVy = 0;
  var nearItem = null, nearItemD = 1e9;

  // The glass turn: scroll position drives a target; the render loop
  // eases toward it, fading the map's content while the DOM glass layer
  // rises over the still-living nebula.
  var glassTarget = 0, glassCur = 0, lastGlassWrite = -1;
  // The view state flip, with hysteresis: past 60% of a screen the
  // page is content (the hit surface goes inert via data-view and
  // the page scrolls like any other page); back under 35% it is the
  // map again. Between the thresholds the previous state stands, so
  // a visitor parked mid-turn never faces a surface that does
  // neither. The flip only ever affects the NEXT gesture, and the
  // initial state is read from the actual scroll position, so a
  // restored or deep-linked page starts in the right one.
  var viewState = '';
  function onScroll() {
    var vh = window.innerHeight || 1;
    var y = window.scrollY || window.pageYOffset || 0;
    glassTarget = Math.max(0, Math.min(1, (y - vh * 0.42) / (vh * 0.55)));
    var st = viewState;
    if (viewState === '') st = y > vh * 0.6 ? 'content' : 'map';
    else if (y > vh * 0.6) st = 'content';
    else if (y < vh * 0.35) st = 'map';
    if (st !== viewState) {
      viewState = st;
      document.body.setAttribute('data-view', st);
    }
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  var lastRW = 0, lastRH = 0;
  // Runtime layout, written for this map. The baked anchors are the
  // composition: centres start at their anchors and move only when a
  // hard constraint forces it, by the least amount that satisfies
  // the constraint (project out along the axis of least penetration;
  // separation corrections split evenly). Hard constraints: centres
  // stay in the safe rect, out of the overlay chrome (header, title
  // card, scroll cue -- measured live from the DOM), with clearance
  // for the label above each centre; and NO object -- no centre, no
  // label, and no point of any cluster -- may sit under the title
  // card, enforced by testing each centre against the card rect
  // grown by that cluster's own point reach (offsets + point radius
  // + sway/breathing margin). Everything keys off the centres, so
  // the solve adapts fog, labels and points together, and a new
  // region needs nothing but its anchor.
  function layoutRegions() {
    var mX = Math.max(20, W * 0.07), mY = Math.max(20, H * 0.06);
    var zones = [], card = null;
    ['.site-header', '.latent-phead', '.latent-scrollzone'].forEach(function (sel) {
      var el = document.querySelector(sel);
      if (!el) return;
      var b = el.getBoundingClientRect(), pad = 44;
      var z = { x0: b.left - pad, y0: b.top - pad, x1: b.right + pad, y1: b.bottom + pad };
      zones.push(z);
      if (sel === '.latent-phead') card = z;
    });
    var labelLift = H * 0.16 + 10; // region labels sit above their centers
    var reach = {};
    regionKeys.forEach(function (k) {
      var rx = 0, ry = 0, rs = 0;
      items.forEach(function (p) {
        if (p.region !== k) return;
        rx = Math.max(rx, Math.abs(p.dx) * W); ry = Math.max(ry, Math.abs(p.dy) * H);
        rs = Math.max(rs, p.size);
      });
      reach[k] = { x: rx + rs / 2 + 40, y: ry + rs / 2 + 40 }; // + sway & breathing margin
    });
    function project(p, z, liftExtra) {
      var y1 = z.y1 + (liftExtra || 0);
      if (p.x > z.x0 && p.x < z.x1 && p.y > z.y0 && p.y < y1) {
        var dl = p.x - z.x0, dr = z.x1 - p.x, dtp = p.y - z.y0, db = y1 - p.y;
        var m = Math.min(dl, dr, dtp, db);
        if (m === db) p.y = y1; else if (m === dtp) p.y = z.y0; else if (m === dl) p.x = z.x0; else p.x = z.x1;
        return true;
      }
      return false;
    }
    function pushOut(p, k) {
      zones.forEach(function (z) { project(p, z, labelLift); });
      if (card) { // the title card, grown by this cluster's reach: no object under it
        var r = reach[k];
        project(p, { x0: card.x0 - r.x, y0: card.y0 - r.y, x1: card.x1 + r.x, y1: card.y1 + r.y }, 0);
        project(p, card, labelLift); // label clearance stands as before
      }
    }
    var pos = {};
    regionKeys.forEach(function (k) {
      var r = DATA.regions[k];
      pos[k] = { x: Math.min(Math.max(r.fx * W, mX), W - mX), y: Math.min(Math.max(r.fy * H, mY), H - mY) };
    });
    var minD = Math.min(W, H) * 0.30;
    for (var it = 0; it < 40; it++) {
      regionKeys.forEach(function (k) { pushOut(pos[k], k); });
      for (var a = 0; a < regionKeys.length; a++) for (var b2 = a + 1; b2 < regionKeys.length; b2++) {
        var pa = pos[regionKeys[a]], pb = pos[regionKeys[b2]];
        var dx = pb.x - pa.x, dy = pb.y - pa.y, d = Math.sqrt(dx * dx + dy * dy) || 1;
        if (d < minD) {
          var push = (minD - d) / 2, ux = dx / d, uy = dy / d;
          pa.x -= ux * push; pa.y -= uy * push; pb.x += ux * push; pb.y += uy * push;
        }
      }
      regionKeys.forEach(function (k) {
        var p = pos[k];
        p.x = Math.min(Math.max(p.x, mX), W - mX); p.y = Math.min(Math.max(p.y, mY), H - mY);
      });
    }
    regionKeys.forEach(function (k) { pushOut(pos[k], k); var r = DATA.regions[k]; r.x = pos[k].x; r.y = pos[k].y; });
  }

  function resize() {
    var nw = window.innerWidth, nh = window.innerHeight;
    // iOS fires resize as its URL bar collapses mid-scroll; rebuilding
    // the canvas then is a visible flash, so height-only jitter under
    // 180px with the same width is ignored — the fixed canvas is sized
    // by CSS anyway and a few hidden pixels cost nothing.
    if (lastRW && nw === lastRW && Math.abs(nh - lastRH) < 180) return;
    lastRW = nw; lastRH = nh;
    DPR = Math.min(window.devicePixelRatio || 1, 1.5);
    W = nw; H = nh;
    if (!W || !H) return;
    canvas.width = Math.round(W * DPR); canvas.height = Math.round(H * DPR);
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
    if (!fogC) { fogC = document.createElement('canvas'); fctx = fogC.getContext('2d'); }
    fogC.width = Math.max(2, Math.round(W * FOGRES)); fogC.height = Math.max(2, Math.round(H * FOGRES));
    layoutRegions();
    if (!filler.length) { buildFiller(); buildSparks(); buildStars(); }
    items.forEach(function (p) { if (!p.x) { var r = DATA.regions[p.region]; p.x = r.x + p.dx * W; p.y = r.y + p.dy * H; } });
    filler.forEach(function (p) { if (!p.x) { p.x = p.hx * W; p.y = p.hy * H; } });
    if (!probe.x) { probe.x = probe.tx = W * 0.5; probe.y = probe.ty = H * 0.45; }
    ctx.fillStyle = '#030209'; ctx.fillRect(0, 0, W, H);
    onScroll();
  }
  window.addEventListener('resize', resize);

  // Interaction discipline: exploring never navigates by accident.
  // Hovering or dragging brings the magnetic probe onto a point and
  // its name shows on its own; stopping there selects it; tapping or
  // clicking the selected point again opens it. A drag never opens,
  // so browsing can't fire a link.
  var coarse = window.matchMedia('(pointer: coarse)').matches;
  var hitR = coarse ? 74 : 54;
  var selected = null, selectedAt = 0;
  var downPt = null, downAt = 0, downType = '';

  function sample(x, y) {
    bursts.push({ x: x, y: y, r: 6, a: 1 });
    if (bursts.length > 5) bursts.shift();
    items.concat(filler).forEach(function (p) {
      var dx = p.x - x, dy = p.y - y, d = Math.sqrt(dx * dx + dy * dy);
      if (d < 210) p.flash = Math.max(p.flash, 1 - d / 210);
    });
  }

  // Input lives on a dedicated hit surface over the canvas (the
  // canvas itself stays pointer-events: none, purely visual). The
  // surface is the canvas's SIBLING, never a parent or child, so its
  // touch-action: none is never intersected with the scroll zone's
  // pan-y. Ownership of a touch is decided by hit-testing at
  // touchstart -- which element the finger landed on -- never by
  // classifying the gesture after it has begun: on iOS that window
  // closes before a classifier can act (claims must land on
  // touchstart or the first touchmove, root listeners are passive by
  // default, and moves turn uncancelable once scrolling starts).
  if (hit) {
    hit.addEventListener('pointermove', function (e) {
      probe.tx = e.clientX; probe.ty = e.clientY; probe.active = true; probe.last = performance.now();
    }, { passive: true });
    hit.addEventListener('pointerdown', function (e) {
      probe.tx = e.clientX; probe.ty = e.clientY; probe.active = true; probe.last = performance.now();
      downPt = { x: e.clientX, y: e.clientY }; downAt = performance.now(); downType = e.pointerType || 'mouse';
      try { hit.setPointerCapture(e.pointerId); } catch (err) {}
    }, { passive: true });
    // pointercancel is a normal end of a drag (system gesture,
    // second finger, rotation), never an error: reset and move on.
    hit.addEventListener('pointercancel', function () { downPt = null; probe.last = 0; }, { passive: true });
    // No long-press callout or menu over the map itself.
    hit.addEventListener('contextmenu', function (e) { e.preventDefault(); });
    hit.addEventListener('pointerup', function (e) {
      if (!downPt) return;
      var moved = Math.abs(e.clientX - downPt.x) + Math.abs(e.clientY - downPt.y);
      var dt = performance.now() - downAt;
      var type = downType;
      downPt = null;
      if (glassCur > 0.4) return; // the map is glassed over; taps belong to the page
      if (moved > 16 || dt > 450) {
        // A drag, not a tap: it selects only if it came to rest
        // right on a point (within tap range of the release point).
        // Passing over points while browsing selects nothing -- the
        // names that lit up on the way were just the browse.
        var rest = null, restD = 1e9;
        items.forEach(function (p) {
          var dx = p.x - e.clientX, dy = p.y - e.clientY, d = dx * dx + dy * dy;
          if (d < restD) { restD = d; rest = p; }
        });
        if (rest && restD < hitR * hitR) { selected = rest; selectedAt = performance.now(); }
        return;
      }
      var best = null, bestD = 1e9;
      items.forEach(function (p) {
        var dx = p.x - e.clientX, dy = p.y - e.clientY, d = dx * dx + dy * dy;
        if (d < bestD) { bestD = d; best = p; }
      });
      if (best && bestD < hitR * hitR) {
        // First contact selects; tapping the selected point again
        // opens it -- one model for mouse and touch alike.
        if (selected === best) {
          window.location.href = best.href;
          return;
        }
        selected = best; selectedAt = performance.now();
        probe.x = probe.tx = e.clientX; probe.y = probe.ty = e.clientY;
        return;
      }
      selected = null;
      sample(e.clientX, e.clientY);
    }, { passive: true });

    // Fallback claim for engines that ignore touch-action: none
    // (pre-13 iOS, embedded WebViews): non-passive listeners on the
    // surface ELEMENT itself -- window/document/body listeners are
    // passive by default in both Chrome and WebKit, so a claim there
    // would be ignored -- registered once at init, never inside a
    // handler, so the first touchmove is already covered.
    var claim = function (e) { if (e.cancelable) e.preventDefault(); };
    hit.addEventListener('touchstart', claim, { passive: false });
    hit.addEventListener('touchmove', claim, { passive: false });
  }

  // The scroll zone is the one place on the first screen where a
  // touch scrolls the page: it carries touch-action: pan-y in the
  // CSS, so drags starting on it are native browser scrolls. It is
  // also a button -- a tap (or Enter/Space) scrolls the list into
  // view directly. Once the page reaches the content, the state
  // flip above makes the hit surface inert and the whole page
  // scrolls normally, the zone included in what scrolls away.
  if (zone) {
    zone.addEventListener('click', function () {
      var sec = document.querySelector('.sitemap-list-sec');
      if (sec && sec.scrollIntoView) sec.scrollIntoView({ behavior: 'smooth', block: 'start' });
      else window.scrollTo(0, window.innerHeight || 0);
    });
  }

  var running = true, raf = null;

  function physics(p, hx, hy, t) {
    var ang = Math.sin(p.x * 0.0016 + t * 0.21) * 1.7 + Math.cos(p.y * 0.0019 - t * 0.17) * 1.7
            + Math.sin((p.x + p.y) * 0.0006 + t * 0.07) * 0.9;
    p.vx += Math.cos(ang) * 0.03 + (hx - p.x) * 0.0016 + (-(p.y - H / 2)) * 0.000016;
    p.vy += Math.sin(ang) * 0.03 + (hy - p.y) * 0.0016 + ((p.x - W / 2)) * 0.000016;
    for (var b = 0; b < bursts.length; b++) {
      var bu = bursts[b];
      var bdx = p.x - bu.x, bdy = p.y - bu.y, bd = Math.sqrt(bdx * bdx + bdy * bdy) || 1;
      var band = Math.abs(bd - bu.r);
      if (band < 46 && bd > 4) {
        var push = (1 - band / 46) * 0.6 * bu.a;
        p.vx += (bdx / bd) * push; p.vy += (bdy / bd) * push;
      }
    }
    if (fixate) {
      var fdx = fixate.item.x - p.x, fdy = fixate.item.y - p.y;
      var fd = Math.sqrt(fdx * fdx + fdy * fdy) || 1;
      if (fd < 320 && fd > 6) {
        var pull = (1 - fd / 320) * 0.05 * fixate.strength;
        p.vx += (fdx / fd) * pull; p.vy += (fdy / fd) * pull;
      }
    }
    p.vx *= 0.93; p.vy *= 0.93;
    p.x += p.vx; p.y += p.vy;
    var dx = p.x - probe.x, dy = p.y - probe.y, d2 = dx * dx + dy * dy;
    var target = d2 < 19600 ? 1 - Math.sqrt(d2) / 140 : 0;
    p.lit += (target - p.lit) * (target > p.lit ? 0.28 : 0.08);
    p.flash *= 0.94;
  }

  function step(now) {
    var t = now * 0.001;
    // Ease the glass turn; cf is what remains of the map's content.
    glassCur += (glassTarget - glassCur) * 0.09;
    if (Math.abs(glassTarget - glassCur) < 0.002) glassCur = glassTarget;
    var cf = 1 - glassCur;
    // Style writes are throttled hard: a full-screen layer repainted
    // every frame is what made WebKit flicker.
    if (glassEl && Math.abs(glassCur - lastGlassWrite) >= 0.02) {
      lastGlassWrite = glassCur;
      glassEl.style.opacity = glassCur.toFixed(2);
      glassEl.style.visibility = glassCur < 0.01 ? 'hidden' : 'visible';
      // The scroll zone belongs to the map screen only: once the
      // turn begins it gets out of the way.
      if (cueEl) cueEl.classList.toggle('cue-gone', glassCur > 0.05);
    }

    // Full repaint every frame. The old translucent fade fill let
    // screen-blended fog integrate upward frame over frame into a
    // pastel white-out; the base now goes down opaque and the whole
    // field is drawn fresh. (The probe's trail is an explicit
    // polyline, so nothing the map needs came from the residue.)
    ctx.globalCompositeOperation = 'source-over';
    ctx.globalAlpha = 1;
    ctx.fillStyle = '#030209';
    ctx.fillRect(0, 0, W, H);

    regionKeys.forEach(function (k) {
      var r = DATA.regions[k];
      r.cx = r.x + Math.sin(t * 0.11 + r.seed) * 26;
      r.cy = r.y + Math.cos(t * 0.09 + r.seed * 1.3) * 20;
    });

    var attract = !probe.active || now - probe.last > 3500;
    if (attract) {
      probe.tx = W * (0.5 + 0.36 * Math.sin(t * 0.23));
      probe.ty = H * (0.48 + 0.32 * Math.sin(t * 0.17 + 1.4));
      if (now > nextAuto && glassCur < 0.5) { sample(probe.x, probe.y); nextAuto = now + 4200 + Math.random() * 2800; }
    }
    // A whisper of magnetism, visual only: the probe light leans a
    // few pixels toward a point it drifts near -- enough to feel
    // the field breathe, never enough to steer the browse. No
    // capture, no lock-on, no riding: the pointer goes exactly
    // where it is put, and points are chosen deliberately.
    var pTx = probe.tx, pTy = probe.ty;
    if (!attract && glassCur < 0.5 && nearItem) {
      var ndx = nearItem.x - probe.tx, ndy = nearItem.y - probe.ty;
      var nd = Math.sqrt(ndx * ndx + ndy * ndy);
      if (nd < 170 && nd > 1) {
        var pull = (1 - nd / 170) * 0.16;
        pTx = probe.tx + ndx * pull; pTy = probe.ty + ndy * pull;
      }
    }
    var sprK = attract ? 0.05 : 0.22, sprD = attract ? 0.80 : 0.62;
    probeVx = (probeVx + (pTx - probe.x) * sprK) * sprD;
    probeVy = (probeVy + (pTy - probe.y) * sprK) * sprD;
    probe.x += probeVx;
    probe.y += probeVy;
    trail.unshift({ x: probe.x, y: probe.y });
    if (trail.length > 26) trail.pop();

    if (!fixate && now > nextFixate && glassCur < 0.5) {
      fixate = { item: items[Math.floor(Math.random() * items.length)], until: now + 3400, strength: 0 };
      nextFixate = now + 9000 + Math.random() * 7000;
    }
    if (fixate) {
      fixate.strength = Math.min(1, fixate.strength + 0.02);
      if (now > fixate.until) fixate = null;
    }

    // The nebula itself never fades: stars, fog, dust stay alive behind
    // the glass for the whole page.
    // The dynamic nebula, live (the demo's Improved draw): stamps
    // in screen blend, filaments and a 'lighter' hot core per
    // region, then dust lanes carved with destination-out.
    if (improvedReady) {
      // The fog is painted on its own low-res surface and composited
      // in a single blit below. Every heavy blend pass in this block
      // (screen stamps, lighter cores, destination-out dust lanes)
      // then costs FOGRES^2 of the main canvas's pixels -- that is
      // what keeps the drift and the touch-push smooth on phone GPUs.
      // The fog is soft gradient work, so the upscale is invisible;
      // no constant, palette, alpha or motion term changes -- only
      // the surface the fog is painted on moved.
      var _mctx = ctx; ctx = fctx;
      ctx.setTransform(FOGRES, 0, 0, FOGRES, 0, 0);
      ctx.globalCompositeOperation = 'source-over';
      ctx.globalAlpha = 1;
      ctx.fillStyle = '#030209';
      ctx.fillRect(0, 0, W, H);
      var tt = t * 1000;
      var dtF = Math.min(0.05, Math.max(0.001, t - (stepFogStamps._lt === undefined ? t - 1 / 60 : stepFogStamps._lt)));
      stepFogStamps._lt = t;
      stepFogStamps(dtF, t);
      var minWH = Math.min(W, H), R = minWH * 0.60, regionSize = minWH * 0.52;
      ctx.globalCompositeOperation = 'screen';
      regionKeys.forEach(function (k, ridx) {
        var r = DATA.regions[k], cx = r.cx, cy = r.cy;
        var arr = fogStamps[k] || [];
        for (var k3 = 0; k3 < arr.length; k3++) {
          var s = arr[k3];
          if (s.x < 0) continue;
          var breathe = Math.sin(tt * 0.00045 * s.sp + s.ph);
          var size2 = R * s.sizeMul * (1 + 0.06 * breathe);
          var spr = improvedSprites[k][s.spr % improvedSprites[k].length];
          ctx.save();
          ctx.globalAlpha = clampF(s.alpha * (1 + 0.18 * breathe) + 0.11 * s.bright, 0, 0.52);
          ctx.translate(s.x, s.y);
          ctx.rotate(s.rot);
          ctx.scale(1, 0.75 + 0.25 * Math.sin(s.ph));
          ctx.drawImage(spr, -size2 / 2, -size2 / 2, size2, size2);
          ctx.restore();
        }
        for (var f = 0; f < 2; f++) {
          var fs = filamentSprites[k][f];
          var fsize = regionSize * (1.05 + f * 0.2) * (1 + 0.04 * Math.sin(tt * 0.0004 + f * 2 + ridx));
          ctx.save(); ctx.globalAlpha = 0.13 + 0.03 * Math.sin(tt * 0.0005 + f + ridx * 2);
          ctx.translate(cx + Math.sin(tt * 0.0001 + f * 3 + ridx) * 16, cy + Math.cos(tt * 0.00009 + f * 2) * 12);
          ctx.rotate(f * 1.7 + ridx + tt * 0.000015); ctx.scale(1, 0.42);
          ctx.drawImage(fs, -fsize / 2, -fsize / 2, fsize, fsize); ctx.restore();
        }
        ctx.globalCompositeOperation = 'lighter';
        var core = improvedSprites[k][0];
        var cs = regionSize * 0.42 * (1 + 0.05 * Math.sin(tt * 0.0006 + ridx * 2));
        ctx.save(); ctx.globalAlpha = 0.42;
        ctx.translate(cx, cy); ctx.drawImage(core, -cs / 2, -cs / 2, cs, cs); ctx.restore();
        ctx.globalCompositeOperation = 'screen';
      });
      ctx.globalCompositeOperation = 'destination-out';
      var lanes = [
        { x: 0.50 * W, y: 0.55 * H, s: R * 2.4, rot: 0.7, a: 0.68, ph: 0.0 },
        { x: DATA.regions.photography.cx, y: DATA.regions.photography.cy, s: R * 1.7, rot: 2.2, a: 0.55, ph: 1.7 },
        { x: 0.52 * W, y: 0.18 * H, s: R * 1.9, rot: 1.4, a: 0.5, ph: 3.1 },
        { x: DATA.regions.projects.cx, y: DATA.regions.projects.cy, s: R * 1.5, rot: 0.2, a: 0.48, ph: 4.4 },
        { x: 0.60 * W, y: 0.62 * H, s: R * 2.0, rot: 1.05, a: 0.52, ph: 5.6 }
      ];
      lanes.forEach(function (L) {
        var lx = L.x + Math.sin(tt * 0.00007 + L.ph) * 20;
        var ly = L.y + Math.cos(tt * 0.00006 + L.ph) * 14;
        ctx.save(); ctx.globalAlpha = L.a;
        ctx.translate(lx, ly); ctx.rotate(L.rot + Math.sin(tt * 0.00005 + L.ph) * 0.08); ctx.scale(1, 0.45);
        ctx.drawImage(dustFieldSprite, -L.s / 2, -L.s / 2, L.s, L.s); ctx.restore();
      });
      ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
      ctx = _mctx;
      ctx.globalCompositeOperation = 'source-over';
      ctx.globalAlpha = 1;
      ctx.drawImage(fogC, 0, 0, W, H);
    }
      // The probe's wake: light dragged through the gas, decaying
      // along the trail the probe leaves behind it.
      ctx.globalCompositeOperation = 'lighter';
      for (var wi = trail.length - 1; wi >= 0; wi--) {
        var wpk = trail[wi];
        var wa = (1 - wi / trail.length) * (probe.active && now - probe.last < 3000 ? 0.15 : 0.05);
        if (wa < 0.012) continue;
        var wr = 130 - wi * 3.5;
        ctx.globalAlpha = wa;
        ctx.drawImage(probeSprite, wpk.x - wr, wpk.y - wr, wr * 2, wr * 2);
      }
      ctx.globalAlpha = 1;
      ctx.globalCompositeOperation = 'source-over';
    var si, st;
    for (si = 0; si < stars.length; si++) {
      st = stars[si];
      var sa = st.a * (0.72 + 0.28 * Math.sin(t * st.sp + st.ph));
      ctx.fillStyle = 'rgba(' + st.tint + ',' + sa.toFixed(3) + ')';
      ctx.fillRect(st.hx * W, st.hy * H, st.s, st.s);
    }
    ctx.globalCompositeOperation = 'lighter';

    var i, p;
    for (i = 0; i < filler.length; i++) {
      p = filler[i];
      physics(p, p.hx * W + Math.sin(t * 0.4 + p.ph) * 10, p.hy * H + Math.cos(t * 0.34 + p.ph) * 9, t);
      var tw = 0.72 + 0.28 * Math.sin(t * 2.0 + p.ph);
      var size = p.s * tw * (0.75 + p.lit * 1.0 + p.flash * 0.7);
      ctx.globalAlpha = Math.min(1, 0.13 + p.lit * 0.6 + p.flash * 0.55);
      ctx.drawImage(p.sprite, p.x - size / 2, p.y - size / 2, size, size);
    }
    ctx.globalAlpha = 1;

    // Everything below is the map's content: it fades with the turn.
    if (cf > 0.01) {
      var links = [];
      nearItem = null; nearItemD = 1e9;
      for (i = 0; i < items.length; i++) {
        p = items[i];
        var r2 = DATA.regions[p.region];
        physics(p, r2.cx + p.dx * W, r2.cy + p.dy * H, t);
        // The top band is reserved empty nebula for the title bar:
        // content points are never allowed to drift up into it.
        if (p.y < H * 0.19) p.vy += (H * 0.19 - p.y) * 0.012;
        var dx = p.x - probe.x, dy = p.y - probe.y, d = dx * dx + dy * dy;
        if (d < nearItemD) { nearItemD = d; nearItem = p; }
        if (p.lit > 0.25 && links.length < 14) links.push(p);
        var isFix = fixate && fixate.item === p;
        var tw2 = 0.82 + 0.18 * Math.sin(t * 2.1 + p.ph);
        var sz = p.size * tw2 * (1 + p.lit * 1.25 + p.flash * 0.7 + (isFix ? 0.55 : 0));
        ctx.globalAlpha = Math.min(1, 0.64 + p.lit * 0.3 + p.flash * 0.35) * cf;
        ctx.drawImage(p.sprite, p.x - sz * 0.72, p.y - sz * 0.72, sz * 1.44, sz * 1.44);
        ctx.globalCompositeOperation = 'source-over';
        ctx.globalAlpha = Math.min(1, 0.72 + p.lit * 0.35 + p.flash * 0.4) * cf;
        ctx.fillStyle = p.css;
        ctx.beginPath(); ctx.arc(p.x, p.y, Math.max(1.9, sz * 0.185), 0, Math.PI * 2); ctx.fill();
        ctx.globalCompositeOperation = 'lighter';
        if (isFix) {
          ctx.globalCompositeOperation = 'source-over';
          ctx.globalAlpha = (0.5 + 0.25 * Math.sin(t * 3)) * cf;
          ctx.strokeStyle = p.css;
          ctx.lineWidth = 1;
          ctx.beginPath(); ctx.arc(p.x, p.y, sz * 1.25 + Math.sin(t * 3) * 3, 0, Math.PI * 2); ctx.stroke();
          ctx.globalAlpha = 1;
          ctx.globalCompositeOperation = 'lighter';
        }
        if (selected === p) {
          ctx.globalCompositeOperation = 'source-over';
          ctx.globalAlpha = (0.55 + 0.3 * Math.sin(t * 3.4)) * cf;
          ctx.strokeStyle = p.css;
          ctx.lineWidth = 1.4;
          ctx.beginPath(); ctx.arc(p.x, p.y, sz * 1.3 + Math.sin(t * 3.4) * 3, 0, Math.PI * 2); ctx.stroke();
          ctx.globalAlpha = 1;
          ctx.globalCompositeOperation = 'lighter';
        }
      }

      // The web first, under everything: faint, in the point's color.
      ctx.globalCompositeOperation = 'source-over';
      ctx.lineWidth = 1;
      for (var wpi = 0; wpi < webPairs.length; wpi++) {
        var wp = webPairs[wpi];
        ctx.strokeStyle = 'rgba(' + wp[0].rgb[0] + ',' + wp[0].rgb[1] + ',' + wp[0].rgb[2] + ',' + (0.13 * cf).toFixed(3) + ')';
        ctx.beginPath(); ctx.moveTo(wp[0].x, wp[0].y); ctx.lineTo(wp[1].x, wp[1].y); ctx.stroke();
      }
      ctx.globalCompositeOperation = 'lighter';

      ctx.lineWidth = 1.5;
      for (var j = 0; j < links.length; j++) {
        var lp = links[j];
        ctx.strokeStyle = 'rgba(' + lp.rgb[0] + ',' + lp.rgb[1] + ',' + lp.rgb[2] + ',' + ((0.1 + lp.lit * 0.5) * cf).toFixed(3) + ')';
        ctx.beginPath(); ctx.moveTo(probe.x, probe.y); ctx.lineTo(lp.x, lp.y); ctx.stroke();
      }

      for (var s2 = trail.length - 1; s2 > 0; s2--) {
        var a2 = trail[s2], b2 = trail[s2 - 1];
        ctx.strokeStyle = 'hsla(' + Math.round((t * 46 + s2 * 7) % 360) + ', 95%, 72%, ' + (0.34 * (1 - s2 / trail.length) * cf).toFixed(3) + ')';
        ctx.lineWidth = 2.2 - s2 * 0.07;
        ctx.beginPath(); ctx.moveTo(a2.x, a2.y); ctx.lineTo(b2.x, b2.y); ctx.stroke();
      }

      for (var k = bursts.length - 1; k >= 0; k--) {
        var rb = bursts[k];
        rb.r += 12; rb.a *= 0.94;
        if (rb.a < 0.02) { bursts.splice(k, 1); continue; }
        var nr = regionKeys[0], nd = 1e9;
        regionKeys.forEach(function (key) {
          var rr2 = DATA.regions[key];
          var ddx = rb.x - rr2.cx, ddy = rb.y - rr2.cy, dd = ddx * ddx + ddy * ddy;
          if (dd < nd) { nd = dd; nr = key; }
        });
        var rc = DATA.regions[nr].rgb;
        ctx.lineWidth = 1.6;
        ctx.strokeStyle = 'rgba(94, 234, 212,' + (rb.a * 0.5 * cf).toFixed(3) + ')';
        ctx.beginPath(); ctx.arc(rb.x, rb.y, rb.r, 0, Math.PI * 2); ctx.stroke();
        ctx.strokeStyle = 'rgba(232, 121, 249,' + (rb.a * 0.3 * cf).toFixed(3) + ')';
        ctx.beginPath(); ctx.arc(rb.x, rb.y, rb.r * 0.72, 0, Math.PI * 2); ctx.stroke();
        ctx.strokeStyle = 'rgba(' + rc[0] + ',' + rc[1] + ',' + rc[2] + ',' + (rb.a * 0.4 * cf).toFixed(3) + ')';
        ctx.beginPath(); ctx.arc(rb.x, rb.y, rb.r * 0.45, 0, Math.PI * 2); ctx.stroke();
      }

      if (now > nextComet) {
        var ang2 = Math.random() * Math.PI * 2;
        comets.push({ x: Math.random() * W, y: Math.random() * H * 0.7, vx: Math.cos(ang2) * 7 + 4, vy: Math.sin(ang2) * 3 + 2, life: 1 });
        nextComet = now + 5000 + Math.random() * 6000;
      }
      for (var c2 = comets.length - 1; c2 >= 0; c2--) {
        var cm = comets[c2];
        cm.x += cm.vx; cm.y += cm.vy; cm.life *= 0.985;
        if (cm.life < 0.05 || cm.x > W + 60 || cm.y > H + 60) { comets.splice(c2, 1); continue; }
        ctx.globalAlpha = cm.life * 0.9 * cf;
        ctx.drawImage(cometSprite, cm.x - 13, cm.y - 13, 26, 26);
        ctx.strokeStyle = 'rgba(45,212,191,' + (cm.life * 0.4 * cf).toFixed(3) + ')';
        ctx.lineWidth = 1.4;
        ctx.beginPath(); ctx.moveTo(cm.x, cm.y); ctx.lineTo(cm.x - cm.vx * 5, cm.y - cm.vy * 5); ctx.stroke();
      }
      ctx.globalAlpha = 1;

      ctx.globalCompositeOperation = 'source-over';
      ctx.globalAlpha = cf;
      ctx.font = '10px ui-monospace, Menlo, Consolas, monospace';
      ctx.textAlign = 'center';
      regionKeys.forEach(function (k) {
        var r = DATA.regions[k];
        var wtxt = ctx.measureText(r.label).width;
        ctx.fillStyle = 'rgba(3,2,9,0.6)';
        ctx.fillRect(r.cx - wtxt / 2 - 7, r.cy - H * 0.16 - 6, wtxt + 14, 15);
        ctx.fillStyle = 'rgba(226,240,255,0.66)';
        ctx.fillText(r.label, r.cx, r.cy - H * 0.16 + 5);
      });

      // Selection persists: a point you stopped on stays identified
      // until you choose another or tap empty space.
      var showItem = selected || ((fixate && now < fixate.until) ? fixate.item : (nearItem && nearItemD < 140 * 140 ? nearItem : null));
      if (showItem) {
        var label2 = showItem.title + '  ·  ' + showItem.sub;
        ctx.font = '11px ui-monospace, Menlo, Consolas, monospace';
        var w2 = ctx.measureText(label2).width;
        var lx = Math.max(10, Math.min(W - w2 - 24, showItem.x - w2 / 2));
        var ly = showItem.y - showItem.size - 30;
        if (ly < 16) ly = showItem.y + showItem.size + 26;
        ctx.fillStyle = 'rgba(3,2,9,0.85)';
        ctx.fillRect(lx - 4, ly - 12, w2 + 16, 19);
        ctx.fillStyle = '#f4f7fb';
        ctx.textAlign = 'left';
        ctx.fillText(label2, lx + 4, ly + 2);
        ctx.textAlign = 'center';
      }
      ctx.globalAlpha = 1;

      ctx.globalCompositeOperation = 'lighter';
      ctx.globalAlpha = cf;
      var pr = 23 + Math.sin(t * 2.4) * 3;
      ctx.drawImage(probeSprite, probe.x - pr, probe.y - pr, pr * 2, pr * 2);
      ctx.globalAlpha = 1;
      ctx.globalCompositeOperation = 'source-over';
      ctx.globalAlpha = cf;
      ctx.strokeStyle = 'rgba(45,212,191,0.9)';
      ctx.lineWidth = 1.2;
      ctx.beginPath(); ctx.arc(probe.x, probe.y, 14 + Math.sin(t * 2.4) * 1.6, 0, Math.PI * 2); ctx.stroke();
      ctx.fillStyle = '#2dd4bf';
      ctx.beginPath(); ctx.arc(probe.x, probe.y, 2.4, 0, Math.PI * 2); ctx.fill();
      ctx.globalAlpha = 1;
      var wantCursor = (nearItem && nearItemD < 54 * 54) ? 'pointer' : '';
      var curEl = hit || document.body;
      if (curEl.style.cursor !== wantCursor) curEl.style.cursor = wantCursor;
    } else {
      // Fully glassed: keep the points parked at their homes so the map
      // is composed when the visitor scrolls back up.
      for (i = 0; i < items.length; i++) {
        p = items[i];
        var r3 = DATA.regions[p.region];
        physics(p, r3.cx + p.dx * W, r3.cy + p.dy * H, t);
        p.lit *= 0.9;
      }
    }

    // Ambient sparkles belong to the nebula: they shine through glass.
    for (var s3 = 0; s3 < sparks.length; s3++) {
      var sp = sparks[s3];
      var a3 = Math.pow(Math.max(0, Math.sin(t * sp.sp + sp.ph)), 6) * 0.6;
      if (a3 > 0.02) {
        ctx.globalCompositeOperation = 'lighter';
        ctx.globalAlpha = a3;
        ctx.drawImage(sp.sprite, sp.x - sp.s / 2, sp.y - sp.s / 2, sp.s, sp.s);
      }
    }
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = 'source-over';

    // The frost's depth: as the glass rises, a dark veil settles over
    // the canvas itself, so the nebula reads as behind something.
    if (glassCur > 0.01) {
      ctx.fillStyle = 'rgba(3, 4, 10,' + (glassCur * 0.38).toFixed(3) + ')';
      ctx.fillRect(0, 0, W, H);
    }
    if (!reduced && grainTiles.length) {
      if (!grainPats) grainPats = grainTiles.map(function (tc) { return ctx.createPattern(tc, 'repeat'); });
      var gPat = grainPats[Math.floor(now / 90) % 4];
      if (gPat) {
        ctx.globalCompositeOperation = 'overlay';
        ctx.globalAlpha = 0.05;
        ctx.fillStyle = gPat;
        ctx.fillRect(0, 0, W, H);
        ctx.globalAlpha = 1;
        ctx.globalCompositeOperation = 'source-over';
      }
    }

    if (running) raf = requestAnimationFrame(step);
  }

  function start() {
    if (reduced) return;
    if (raf) cancelAnimationFrame(raf);
    if (running) raf = requestAnimationFrame(step);
  }

  resize();
  onScroll();
  if (reduced) {
    regionKeys.forEach(function (k) { var r = DATA.regions[k]; r.cx = r.x; r.cy = r.y; });
    items.forEach(function (p) { var r = DATA.regions[p.region]; p.x = r.x + p.dx * W; p.y = r.y + p.dy * H; });
    filler.forEach(function (p) { p.x = p.hx * W; p.y = p.hy * H; });
    probe.x = W * 0.5; probe.y = H * 0.45;
    glassCur = glassTarget;
    running = false;
    step(0);
  } else {
    start();
    document.addEventListener('visibilitychange', function () {
      if (document.hidden) { running = false; if (raf) cancelAnimationFrame(raf); }
      else { running = true; start(); }
    });
  }
})();
</script>
""".replace("/*__DATA__*/null", json.dumps(LATENT_DATA))

page("blog.html", "Blog \u2014 Adam Laloge", BLOG_DESC, "blog.html", blog_index_body())
for _p in POSTS:
    page(_p["fname"], _p["title"] + " \u2014 Adam Laloge", _p["desc"] or BLOG_DESC, "blog.html", blog_post_body(_p))
write_feed()
write_sitemap()

page("latent-sitemap.html", "Atlas — Adam Laloge",
     "A sitemap drawn as a latent space: every photo, book, artwork, and project on Adam Laloge's site as a point in one flowing map.",
     "latent-sitemap.html", sitemap_body, LATENT_MAP_JS)

print("done")
