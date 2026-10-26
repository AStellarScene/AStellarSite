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
<link rel="stylesheet" href="styles.css?v=47">
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
    ("dreams.html", "Dreamscape"),
    ("latent-sitemap.html", "Atlas"),
]

def header(active):
    links = "\n      ".join(
        '<a href="%s"%s>%s</a>' % (href, ' class="active"' if href == active else "", label)
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
    <span class="footer-links"><a href="https://github.com/AStellarScene">GitHub</a></span>
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

def page(fname, title, desc, active, body, extra_js=""):
    html = (HEAD.format(title=title, desc=desc) + header(active)
            + '\n<main class="wrap">\n' + body + '\n</main>\n' + FOOTER
            + extra_js + NAV_JS + "\n</body>\n</html>\n")
    open(os.path.join(SITE, fname), "w").write(html)
    print("wrote", fname, len(html))

DESC = "Personal site of Adam Laloge: software projects, photography, and what I'm building lately."

# ---------- Home ----------
home_body = """  <section class="hero">
    <canvas id="sky" aria-hidden="true"></canvas>
    <h1>Hi there</h1>
    <p class="intro">I build test software, and I'm finishing a UX degree. I photograph sunsets and read dark fantasy. Most of my work is internal and can't be shown, so I build in the open here: chasing digital experiences, taking new technologies to the maximum, creating science fiction in real life. That's my goal, anyway.</p>
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
        <p class="status">Now: Prototype built, first usability test running</p>
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
        <p>My five-day packed-lunch rotation, turned into a tool anyone can use. Pick the week's meals and get the grocery list, checked against what's already at home.</p>
        <p><a class="card-link" href="rotation.html">View project &#8599;</a></p>
      </article>
      <article class="card">
        <p class="label card-label">Slip</p>
        <p class="status">Now: Planned, not started</p>
        <p>A pause before small purchases. Enter a price and how often it recurs, and see it as days of delay on a savings target instead of dollars.</p>
        <p><a class="card-link" href="slip.html">View project &#8599;</a></p>
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

  <section id="latent">
    <p class="label">Dreamscape</p>
    <h2>Worlds imagined by computers</h2>
    <p><a href="dreams.html"><img class="teaser-img" src="art/golden-city.jpg" alt="A golden city of spires and bridges in the clouds, built around a glowing ring"></a></p>
    <p><a href="dreams.html">Enter Dreamscape &#8599;</a></p>
  </section>

  <section id="contact">
    <p class="label">Contact</p>
    <h2>Get in touch</h2>
    <p>Code and public projects live on GitHub: <a href="https://github.com/AStellarScene">github.com/AStellarScene</a>.</p>
  </section>"""
page("index.html", "Adam Laloge", DESC, "index.html",
     home_body, "<script>" + sky_js + "</script>\n")

# ---------- Work index ----------
work_body = """  <section id="work">
    <p class="label">Projects</p>
    <h2>Things I'm building</h2>
    <p class="section-note">The status line is the part to trust. Descriptions say what each project is meant to do.</p>
    <div class="cards">
      <article class="card">
        <p class="label card-label">BenchLab</p>
        <p class="status">Now: Prototype built, first usability test running</p>
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
        <p>My five-day packed-lunch rotation, turned into a tool anyone can use. Pick the week's meals and get the grocery list, checked against what you already have at home.</p>
        <p><a class="card-link" href="rotation.html">View project &#8599;</a></p>
      </article>
      <article class="card">
        <p class="label card-label">Slip</p>
        <p class="status">Now: Planned, not started</p>
        <p>A pause before small purchases. Enter a price and how often it recurs, and see the cost as days of delay on a savings target. There is a 48-hour hold list for undecided items. Local data only, no bank connection.</p>
        <p><a class="card-link" href="slip.html">View project &#8599;</a></p>
      </article>
    </div>
  </section>"""
page("work.html", "Projects — Adam Laloge", DESC, "work.html", work_body)

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
    page(fname, "%s — Adam Laloge" % name, DESC, "work.html", body)

project("benchlab.html", "BenchLab", "Prototype built, first usability test running",
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
    ["My five-day packed-lunch rotation, turned into a tool anyone can use. I run this system every week; Rotation is the version that doesn't live in my head.",
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
    <p>Code and public projects live on GitHub: <a href="https://github.com/AStellarScene">github.com/AStellarScene</a>.</p>
  </section>"""
page("about.html", "About — Adam Laloge", DESC, "about.html", about_body)

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

  <div class="latent-band" id="latent-band">
    <button type="button" class="slice" data-world="golden" aria-expanded="false" aria-label="Open The Golden City">
      <img src="art/golden-city.jpg" alt="A golden city of spires and bridges in the clouds, built around a glowing ring" draggable="false">
      <span class="slice-title">The Golden City</span>
      <span class="slice-cap">
        <strong>The Golden City</strong>
        <span>A city in the clouds, built around a ring of light.</span>
        <span class="slice-hint">Tap again to come back</span>
      </span>
    </button>
    <button type="button" class="slice" data-world="ember" aria-expanded="false" aria-label="Open Obsidian Dragon">
      <span class="seam" aria-hidden="true"></span>
      <img src="art/obsidian-dragon.jpg" alt="An obsidian dragon with lava-lit cracks roaring over a burning volcanic valley at night" draggable="false">
      <span class="slice-title">Obsidian Dragon</span>
      <span class="slice-cap">
        <strong>Obsidian Dragon</strong>
        <span>Obsidian and lava over a burning valley. The render my avatar was cut from.</span>
        <span class="slice-hint">Tap again to come back</span>
      </span>
    </button>
  </div>

  <p class="flow-hint">Tap a world to step inside &middot; tap again to come back</p>

  <section>
    <p class="section-note">More worlds arrive as I make them.</p>
  </section>"""
latent_js = """<script>
(function () {
  var band = document.getElementById('latent-band');
  if (!band) return;
  var slices = Array.prototype.slice.call(band.querySelectorAll('.slice'));
  var openIdx = -1;
  document.documentElement.classList.add('latent-live');
  // The opened band starts below the top bar; CSS needs the bar's real
  // height so the image is sized to the space under it, fully in view.
  var header = document.querySelector('.site-header');
  function setBar() {
    if (!header) return;
    var h = header.offsetHeight;
    document.documentElement.style.setProperty('--bar-h', h + 'px');
    document.documentElement.style.setProperty('--bar-half', (h / 2) + 'px');
  }
  window.addEventListener('resize', function () { if (openIdx >= 0) setBar(); });
  function toggle(idx) {
    if (openIdx === idx) {
      openIdx = -1;
      band.classList.remove('open');
      slices.forEach(function (s) { s.classList.remove('active'); s.setAttribute('aria-expanded', 'false'); });
      document.documentElement.removeAttribute('data-world');
      document.documentElement.classList.remove('world-lock');
      document.documentElement.style.removeProperty('--bar-h');
      document.documentElement.style.removeProperty('--bar-half');
    } else {
      setBar();
      openIdx = idx;
      band.classList.add('open');
      slices.forEach(function (s, i) {
        s.classList.toggle('active', i === idx);
        s.setAttribute('aria-expanded', i === idx ? 'true' : 'false');
      });
      document.documentElement.setAttribute('data-world', slices[idx].getAttribute('data-world'));
      document.documentElement.classList.add('world-lock');
    }
  }
  slices.forEach(function (s, i) { s.addEventListener('click', function () { toggle(i); }); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && openIdx >= 0) toggle(openIdx); });
})();
</script>
"""
page("dreams.html", "Dreamscape — Adam Laloge",
     "AI artwork directed by Adam Laloge. Images sit in two-image splits. Open one and it fills the screen while the page takes on its colors.",
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
     "b": "Grimdark with dragons, and the one that asks the least homework up front. Current front-runner.",
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
    {"t": "Gardens of the Moon", "a": "Steven Erikson", "s": "Up next",
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


def latent_map_data():
    items = []
    group_angle = {"sunsets": -90, "shoreline": 0, "landscapes": 90, "details": 180}
    photos_block = re.search(r"var PHOTOS = \[(.*?)\];", gallery_js, re.S).group(1)
    for m in re.finditer(r"src: '(photos/[^']+)',\s+title: '([^']+)',\s+group: '([^']+)'", photos_block):
        src, title, group = m.groups()
        ang = math.radians(group_angle.get(group, 0) + _jitter(title, 26))
        rad = 0.052 + (zlib.crc32(title.encode()) % 100) / 100.0 * 0.075
        items.append({"kind": "photo", "title": title, "sub": group,
                      "rgb": _vibrant_color(os.path.join(SITE, src)), "size": 17,
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
                      "rgb": rgb, "size": 16, "dx": round(dx, 4), "dy": round(dy, 4),
                      "region": "bookshelf", "href": "bookshelf.html#book-" + _slug(b["t"])})
    for fname, title in [("golden-city.jpg", "The Golden City"), ("obsidian-dragon.jpg", "Obsidian Dragon")]:
        items.append({"kind": "world", "title": title, "sub": "Dreamscape",
                      "rgb": _vibrant_color(os.path.join(SITE, "art", fname)), "size": 30,
                      "dx": -0.045 if "golden" in fname else 0.045, "dy": 0.0,
                      "region": "worlds", "href": "dreams.html"})
    src_text = open(os.path.abspath(__file__)).read()
    for m in re.finditer(r'project\("(\w+)\.html", "([^"]+)", "([^"]+)"', src_text):
        slug, name, status = m.groups()
        h = zlib.crc32(name.encode())
        ang = math.radians(h % 360)
        items.append({"kind": "project", "title": name, "sub": status,
                      "rgb": _lighten([94, 234, 212], 0.1 + (h % 40) / 100.0), "size": 20,
                      "dx": round(math.cos(ang) * 0.07, 4), "dy": round(math.sin(ang) * 0.05, 4),
                      "region": "projects", "href": slug + ".html"})
    regions = {
        "photography": {"label": "PHOTOGRAPHY", "fx": 0.30, "fy": 0.44},
        "bookshelf": {"label": "BOOKSHELF", "fx": 0.76, "fy": 0.40},
        "worlds": {"label": "DREAMSCAPE", "fx": 0.24, "fy": 0.80},
        "projects": {"label": "PROJECTS", "fx": 0.74, "fy": 0.79},
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
  <div class="latent-glass-layer" aria-hidden="true" style="background: radial-gradient(60% 50% at 30% 44%, rgba(224, 170, 80, 0.17), rgba(224, 170, 80, 0) 70%), radial-gradient(55% 45% at 76% 40%, rgba(150, 110, 200, 0.15), rgba(150, 110, 200, 0) 70%), radial-gradient(60% 50% at 24% 80%, rgba(220, 90, 50, 0.16), rgba(220, 90, 50, 0) 70%), radial-gradient(55% 45% at 74% 79%, rgba(45, 190, 175, 0.15), rgba(45, 190, 175, 0) 70%), rgba(6, 8, 16, 0.55);"></div>
  <script>document.body.classList.add('sitemap-body');</script>
  <div class="sitemap-flow">
  <section class="latent-intro">
    <div class="latent-glass latent-phead">
      <p class="label">Sitemap</p>
      <h1>Atlas</h1>
      <p class="phead-note">Tap a point to select it &middot; tap again to open it &middot; scroll for the list &#8595;</p>
    </div>
    <div class="latent-scrollcue" aria-hidden="true">
      <span class="cue-word">Scroll</span>
      <span class="cue-arrow"><i></i><i></i></span>
    </div>
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
  var cueEl = document.querySelector('.latent-scrollcue');
  if (!canvas || !DATA) return;
  var ctx = canvas.getContext('2d');
  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var W = 0, H = 0, DPR = 1;

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
  function makeFog(rgb) {
    var c = document.createElement('canvas'); c.width = c.height = 256;
    var g = c.getContext('2d');
    g.globalCompositeOperation = 'lighter';
    var fs = 13579;
    function frnd() { fs = (fs * 1103515245 + 12345) & 0x7fffffff; return fs / 0x7fffffff; }
    for (var i = 0; i < 16; i++) {
      var bx = 128 + (frnd() - 0.5) * 130, by = 128 + (frnd() - 0.5) * 130;
      var br = 34 + frnd() * 62;
      var grad = g.createRadialGradient(bx, by, 0, bx, by, br);
      grad.addColorStop(0, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',' + (0.028 + frnd() * 0.055).toFixed(3) + ')');
      grad.addColorStop(1, 'rgba(' + rgb[0] + ',' + rgb[1] + ',' + rgb[2] + ',0)');
      g.fillStyle = grad;
      g.beginPath(); g.arc(bx, by, br, 0, Math.PI * 2); g.fill();
    }
    g.globalCompositeOperation = 'destination-in';
    var mask = g.createRadialGradient(128, 128, 40, 128, 128, 128);
    mask.addColorStop(0, 'rgba(0,0,0,1)');
    mask.addColorStop(0.7, 'rgba(0,0,0,0.75)');
    mask.addColorStop(1, 'rgba(0,0,0,0)');
    g.fillStyle = mask; g.fillRect(0, 0, 256, 256);
    // Smooth the cloud (downscale round trip), then bake in a whisper of
    // monochrome dither: together they keep the fog from lumping or
    // banding into stripes on 1x displays.
    var small = document.createElement('canvas'); small.width = small.height = 56;
    var sg = small.getContext('2d');
    sg.drawImage(c, 0, 0, 56, 56);
    g.globalCompositeOperation = 'source-over';
    g.clearRect(0, 0, 256, 256);
    g.drawImage(small, 0, 0, 256, 256);
    var imgData = g.getImageData(0, 0, 256, 256);
    var px = imgData.data;
    for (var q = 0; q < px.length; q += 4) {
      var nz = (Math.random() + Math.random() - 1) * 2.4;
      px[q] += nz; px[q + 1] += nz; px[q + 2] += nz;
    }
    g.putImageData(imgData, 0, 0);
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

  var regionKeys = Object.keys(DATA.regions);
  regionKeys.forEach(function (k, i) {
    var r = DATA.regions[k];
    r.key = k; r.seed = i * 1.73 + 0.6; r.cx = 0; r.cy = 0; r.rgb = [120, 120, 160];
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
    var list = items.filter(function (p) { return p.region === k; });
    if (!list.length) return;
    var r = [0, 0, 0];
    list.forEach(function (p) { r[0] += p.rgb[0]; r[1] += p.rgb[1]; r[2] += p.rgb[2]; });
    DATA.regions[k].rgb = [Math.round(r[0] / list.length), Math.round(r[1] / list.length), Math.round(r[2] / list.length)];
  });
  var fogs = [];
  regionKeys.forEach(function (k, i) {
    var spr = makeFog(DATA.regions[k].rgb);
    fogs.push({ sprite: spr, ph: i * 2.1 + 0.7, sp: 0.05 + i * 0.013, region: k, ox: -0.06, oy: 0.02, sc: 0.56 });
    fogs.push({ sprite: spr, ph: i * 2.1 + 2.6, sp: 0.041 + i * 0.011, region: k, ox: 0.07, oy: -0.03, sc: 0.4 });
  });

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
    var n = Math.round(Math.min(420, Math.max(180, W * H / 4500)));
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

  var probe = { x: 0, y: 0, tx: 0, ty: 0, active: false, last: 0 };
  var trail = [];
  var bursts = [];
  var comets = [];
  var nextComet = 4000, nextAuto = 5000, nextFixate = 8000;
  var fixate = null;
  var nearItem = null, nearItemD = 1e9;

  // The glass turn: scroll position drives a target; the render loop
  // eases toward it, fading the map's content while the DOM glass layer
  // rises over the still-living nebula.
  var glassTarget = 0, glassCur = 0, lastGlassWrite = -1;
  function onScroll() {
    var vh = window.innerHeight || 1;
    var y = window.scrollY || window.pageYOffset || 0;
    glassTarget = Math.max(0, Math.min(1, (y - vh * 0.42) / (vh * 0.55)));
  }
  window.addEventListener('scroll', onScroll, { passive: true });

  var lastRW = 0, lastRH = 0;
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
    regionKeys.forEach(function (k) { var r = DATA.regions[k]; r.x = r.fx * W; r.y = r.fy * H; });
    if (!filler.length) { buildFiller(); buildSparks(); buildStars(); }
    items.forEach(function (p) { if (!p.x) { var r = DATA.regions[p.region]; p.x = r.x + p.dx * W; p.y = r.y + p.dy * H; } });
    filler.forEach(function (p) { if (!p.x) { p.x = p.hx * W; p.y = p.hy * H; } });
    if (!probe.x) { probe.x = probe.tx = W * 0.5; probe.y = probe.ty = H * 0.45; }
    ctx.fillStyle = '#030209'; ctx.fillRect(0, 0, W, H);
    onScroll();
  }
  window.addEventListener('resize', resize);

  // The canvas itself takes no input at all (pointer-events: none in
  // the CSS), so the map listens at window level: the probe follows the
  // pointer anywhere on the page, and taps are read wherever they land.
  // Client coordinates are canvas coordinates — the canvas is fixed
  // and fills the viewport.
  window.addEventListener('pointermove', function (e) {
    probe.tx = e.clientX; probe.ty = e.clientY; probe.active = true; probe.last = performance.now();
  }, { passive: true });

  function sample(x, y) {
    bursts.push({ x: x, y: y, r: 6, a: 1 });
    if (bursts.length > 5) bursts.shift();
    items.concat(filler).forEach(function (p) {
      var dx = p.x - x, dy = p.y - y, d = Math.sqrt(dx * dx + dy * dy);
      if (d < 210) p.flash = Math.max(p.flash, 1 - d / 210);
    });
  }

  // Touch discipline: a touch never navigates by accident. The first
  // tap on a point selects it (nameplate + ring); a second tap on the
  // same point opens it. A mouse click opens directly. A drag is never
  // a tap, so exploring can't fire a link.
  var coarse = window.matchMedia('(pointer: coarse)').matches;
  var hitR = coarse ? 74 : 54;
  var selected = null, selectedAt = 0;
  var downPt = null, downAt = 0, downType = '';

  window.addEventListener('pointerdown', function (e) {
    probe.tx = e.clientX; probe.ty = e.clientY; probe.active = true; probe.last = performance.now();
    downPt = { x: e.clientX, y: e.clientY }; downAt = performance.now(); downType = e.pointerType || 'mouse';
  }, { passive: true });
  window.addEventListener('pointercancel', function () { downPt = null; probe.last = 0; }, { passive: true });
  window.addEventListener('contextmenu', function (e) {
    // No long-press menu over the map itself; links keep theirs.
    if (glassCur < 0.4 && !(e.target && e.target.closest && e.target.closest('a, button'))) e.preventDefault();
  });
  window.addEventListener('pointerup', function (e) {
    if (!downPt) return;
    // A tap on a link or button belongs to that element, not the map.
    if (e.target && e.target.closest && e.target.closest('a, button')) { downPt = null; return; }
    var moved = Math.abs(e.clientX - downPt.x) + Math.abs(e.clientY - downPt.y);
    var dt = performance.now() - downAt;
    var type = downType;
    downPt = null;
    if (moved > 16 || dt > 450) return; // a drag, not a tap
    if (glassCur > 0.4) return; // the map is glassed over; taps belong to the page
    var best = null, bestD = 1e9;
    items.forEach(function (p) {
      var dx = p.x - e.clientX, dy = p.y - e.clientY, d = dx * dx + dy * dy;
      if (d < bestD) { bestD = d; best = p; }
    });
    if (best && bestD < hitR * hitR) {
      if (type === 'mouse' || (selected === best && performance.now() - selectedAt < 3500)) {
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

  // Touch model: there are no zones. The page declares one gesture
  // contract (body { touch-action: pan-y }): vertical drags scroll
  // natively anywhere — margins, map, list — and the browser's own
  // arbitration (pointercancel when a scroll claims the gesture)
  // keeps the two apart. Sideways drags and taps reach the map
  // through the window listeners above.

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
    p.lit += (target - p.lit) * 0.13;
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
      // The scroll strip belongs to the map screen only: once the turn
      // begins it gets out of the way.
      if (cueEl) cueEl.classList.toggle('cue-gone', glassCur > 0.05);
      // (No touch handoff exists anymore — the canvas intercepts
      // nothing, so the page's touches were never taken from it.)
    }

    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(3, 2, 9, 0.24)';
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
    probe.x += (probe.tx - probe.x) * 0.06;
    probe.y += (probe.ty - probe.y) * 0.06;
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
    var si, st;
    for (si = 0; si < stars.length; si++) {
      st = stars[si];
      var sa = st.a * (0.72 + 0.28 * Math.sin(t * st.sp + st.ph));
      ctx.fillStyle = 'rgba(' + st.tint + ',' + sa.toFixed(3) + ')';
      ctx.fillRect(st.hx * W, st.hy * H, st.s, st.s);
    }
    fogs.forEach(function (w) {
      var r = DATA.regions[w.region];
      var wx = r.cx + w.ox * W + Math.sin(t * w.sp * 2 + w.ph) * W * 0.03;
      var wy = r.cy + w.oy * H + Math.cos(t * w.sp * 1.6 + w.ph) * H * 0.03;
      var ws = Math.max(W, H) * w.sc * (1 + 0.07 * Math.sin(t * 0.13 + w.ph));
      ctx.globalAlpha = 0.55;
      ctx.drawImage(w.sprite, wx - ws / 2, wy - ws / 2, ws, ws);
    });
    ctx.globalAlpha = 1;
    ctx.globalCompositeOperation = 'lighter';

    var i, p;
    for (i = 0; i < filler.length; i++) {
      p = filler[i];
      physics(p, p.hx * W + Math.sin(t * 0.4 + p.ph) * 10, p.hy * H + Math.cos(t * 0.34 + p.ph) * 9, t);
      var tw = 0.72 + 0.28 * Math.sin(t * 2.0 + p.ph);
      var size = p.s * tw * (0.75 + p.lit * 1.0 + p.flash * 0.7);
      ctx.globalAlpha = Math.min(1, 0.08 + p.lit * 0.6 + p.flash * 0.55);
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
        ctx.globalAlpha = Math.min(1, 0.5 + p.lit * 0.35 + p.flash * 0.35) * cf;
        ctx.drawImage(p.sprite, p.x - sz * 0.72, p.y - sz * 0.72, sz * 1.44, sz * 1.44);
        ctx.globalCompositeOperation = 'source-over';
        ctx.globalAlpha = Math.min(1, 0.55 + p.lit * 0.45 + p.flash * 0.4) * cf;
        ctx.fillStyle = p.css;
        ctx.beginPath(); ctx.arc(p.x, p.y, Math.max(1.6, sz * 0.16), 0, Math.PI * 2); ctx.fill();
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

      if (selected && now - selectedAt > 5000) selected = null;
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
      if (document.body.style.cursor !== wantCursor) document.body.style.cursor = wantCursor;
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

page("latent-sitemap.html", "Atlas — Adam Laloge",
     "A sitemap drawn as a latent space: every photo, book, artwork, and project on Adam Laloge's site as a point in one flowing map.",
     "latent-sitemap.html", sitemap_body, LATENT_MAP_JS)

print("done")
