---
title: The Living Map
date: 2026-10-28
description: The Atlas is this site's sitemap drawn as a latent space — alive, breathing, and spaced by an algorithm. The full technical story: the questions that started it, thirty iterations in three days, the fog wars, and the solver that places the pieces.
---

<div class="seefirst">
<div class="seefirst-k">See it first</div>
<div class="seefirst-t">The Atlas is a map you touch, not a diagram you look at. Spend a minute pushing the fog around and tapping points first — then come back for how it works.</div>
<a class="seefirst-a" href="latent-sitemap.html">Open the Atlas &rarr;</a>
</div>

Every website has a sitemap. Almost all of them are lists — a page of links, or a file machines read. This site's sitemap is a place: a dark field of drifting fog lit in five colours, where every page, photo, book, artwork, project, and post exists as a point of light, and moving your finger through it makes the nearby points lean toward you and connect. It is called the Atlas, and it began — as the Dreamscape article on this blog began — with a question I asked out loud: *what would it look like if my sitemap was a latent space?*

This is its technical record: the prompts that started it, the concept stages, the versions it burned through at a ridiculous pace, the long fight to make the fog match a look, the graphics architecture underneath, and — the part everything else was scaffolding for — the algorithm that spaces the pieces by itself.

<div class="statband">
<div class="stat"><b>5</b><span>Regions</span></div>
<div class="stat"><b>38</b><span>Points, this post included</span></div>
<div class="stat"><b>30+</b><span>Shipped iterations in 3 days</span></div>
<div class="stat"><b>0</b><span>Points placed by hand</span></div>
</div>

## It started with a question

The phrase arrived sideways. I was naming the AI-art page on this site and asked what "latent space" actually meant. The mechanism, briefly: a trained model compresses everything it knows into a high-dimensional space where *nearness means relatedness* — pictures of similar things land near each other, and the map of that space, projected flat, looks like an archipelago of glowing clusters. I'd seen those plots. Every personal site I'd ever visited had a list for a sitemap. The prompt I kept coming back to over the next day was simple: **build me a version of the latent space as my sitemap.**

The first proof of concept (October 26) was pure atmosphere: a standalone page with somewhere between 550 and 1,500 synthetic glowing points in six clusters named for my art worlds, flowing on a sine field, with a "prompt probe" that reported a fake z-vector and its nearest cluster as you moved the pointer. It looked the part. Then I asked the question that changed the project: *is it built on the website's content?* It wasn't — hand-seeded, synthetic, decorative. I asked whether it adapted as the site changed, and whether it should be "some sort of SSG." It should, and it was: the site's generator already *is* a hand-rolled static site generator, so the map became a build step inside it, deriving every point from the same data that builds the pages.

Then I pushed harder: *how is this a real latent space? Explain it.* The honest answer, which the shipped page still stands on: it is a **feature space in latent-space grammar**. Every item becomes a point computed from a small feature vector — its kind, its group or status, its *measured* colour (sampled from the actual photo or artwork file) — and proximity means similarity *by construction*, the way an embedding's proximity means similarity by training. It is not a learned embedding; the literal upgrade (CLIP embeddings at build time, UMAP projection) exists and was named, and I chose the honest version: a map *arranged from the site's content*, labelled as such. A sitemap doesn't need to pretend a model dreamed it. It needs to be true, current, and beautiful.

From there the direction was mine and it was specific: promote it from proof of concept to an art visualiser — more colour, more dynamic — and then ship it as a real page. The acceptance bar I set, and repeated until it stuck:

- **Living.** Nothing on it is static. If a layer can be frozen, it will be — so no layer may be.
- **Breathing.** The field itself moves: fog advects on a wander current, points are held by soft springs, homes orbit slowly.
- **Physics-spaced.** Positions come from forces and constraints, not from a table of coordinates I maintain.
- **Beautiful.** It has to look like a place, not a debug view — the fog carries the mood.
- **Multi-dimensional.** Every point encodes several features at once — kind, colour, size, region — the way a latent point encodes many features in its coordinates.

**Lesson 1: a map generated from the thing it maps cannot go stale.** The Atlas has no separate upkeep because there is nothing separate to keep up: add a photo, a book, a post, and the next build adds its point. The day this article publishes, it adds *itself*.

<figure>
<div class="figbox">
<svg viewBox="0 0 680 300" role="img" aria-label="Diagram of the Atlas as a latent space: five coloured regions of points, with a probe connecting to its nearest neighbours">
  <rect x="10" y="10" width="660" height="280" rx="10" fill="rgba(148,163,184,0.04)" stroke="rgba(148,163,184,0.25)"/>
  <ellipse cx="200" cy="105" rx="120" ry="62" fill="rgba(34,190,205,0.08)"/>
  <ellipse cx="480" cy="95" rx="110" ry="55" fill="rgba(216,96,158,0.07)"/>
  <ellipse cx="185" cy="235" rx="115" ry="48" fill="rgba(228,96,52,0.08)"/>
  <ellipse cx="480" cy="230" rx="120" ry="50" fill="rgba(226,182,92,0.07)"/>
  <ellipse cx="345" cy="165" rx="80" ry="40" fill="rgba(150,130,255,0.08)"/>
  <g fill="#7de8d8"><circle cx="150" cy="85" r="3.5"/><circle cx="205" cy="118" r="3"/><circle cx="245" cy="80" r="2.6"/><circle cx="180" cy="140" r="2.4"/></g>
  <g fill="#f2a7c8"><circle cx="445" cy="80" r="3.2"/><circle cx="505" cy="105" r="2.8"/><circle cx="480" cy="65" r="2.4"/></g>
  <g fill="#f5a183"><circle cx="140" cy="225" r="4"/><circle cx="215" cy="248" r="3.4"/><circle cx="185" cy="215" r="2.6"/></g>
  <g fill="#ecd29a"><circle cx="440" cy="220" r="3.4"/><circle cx="520" cy="240" r="3"/><circle cx="485" cy="255" r="2.5"/></g>
  <g fill="#c4b5fd"><circle cx="330" cy="158" r="3"/><circle cx="362" cy="175" r="2.6"/></g>
  <line x1="285" y1="185" x2="245" y2="80" stroke="rgba(232,244,241,0.45)" stroke-width="1" stroke-dasharray="3 4"/>
  <line x1="285" y1="185" x2="330" y2="158" stroke="rgba(232,244,241,0.45)" stroke-width="1" stroke-dasharray="3 4"/>
  <circle cx="285" cy="185" r="5" fill="none" stroke="#e8f4f1" stroke-width="1.6"/>
  <line x1="285" y1="174" x2="285" y2="196" stroke="#e8f4f1" stroke-width="1.2"/>
  <line x1="274" y1="185" x2="296" y2="185" stroke="#e8f4f1" stroke-width="1.2"/>
  <text x="130" y="42" fill="#7de8d8" font-family="var(--mono)" font-size="11.5" letter-spacing="2">PHOTOGRAPHY</text>
  <text x="425" y="36" fill="#f2a7c8" font-family="var(--mono)" font-size="11.5" letter-spacing="2">BOOKSHELF</text>
  <text x="120" y="282" fill="#f5a183" font-family="var(--mono)" font-size="11.5" letter-spacing="2">DREAMSCAPE</text>
  <text x="435" y="282" fill="#ecd29a" font-family="var(--mono)" font-size="11.5" letter-spacing="2">PROJECTS</text>
  <text x="300" y="128" fill="#c4b5fd" font-family="var(--mono)" font-size="11.5" letter-spacing="2">WRITING</text>
  <text x="300" y="205" fill="#9fb4c8" font-family="var(--mono)" font-size="11">the probe — near points lean in and connect</text>
</svg>
</div>
<figcaption>FIG. 1 — THE MAP AS A LATENT SPACE. FIVE REGIONS, ONE PER KIND OF THING THE SITE HOLDS. A POINT'S COLOUR IS MEASURED FROM THE THING ITSELF; ITS REGION IS ITS MEANING; THE PROBE MAKES PROXIMITY VISIBLE BY CONNECTING WHAT IS NEAR.</figcaption>
</figure>

## First light: Latent Sitemap

The page shipped the same day as the idea (October 26, stylesheet v30 — keep that number in mind; it becomes an odometer). Thirty-two points: 19 photos, 7 books, 2 artworks, 4 projects. A stage occupying most of the viewport, a frosted-glass panel carrying the title, and below the stage a plain grouped list of every item as real links — the functional sitemap and the no-JavaScript fallback, because a sitemap that only works as art fails its one job.

The first fights were embarrassingly physical. The title panel covered the visualisation, so it moved above the stage; then the stage felt boxed in, so the page was rebuilt to my full-page design: the nebula became a fixed, full-viewport background for the whole page, scrolling fades the map's points out while a full-screen frosted layer rises over the still-living fog, and the plain list sits on that glass. The map stopped being a box on a page and became the page's ground. The name changed the same day — Latent Sitemap became **Atlas** — though the URL, like several things on this site, kept its birth name: `latent-sitemap.html`.

The fog spent these rounds being fixed in ways that sound small and aren't. Its sprite edges quantised into visible grain on 1x displays (fixed by smoothing the sprite at build). Then I photographed horizontal contour stripes banding through the red fog on my monitor — 8-bit banding, the same family — fixed by baking a ±2.4 triangular micro-dither into every fog sprite. A nebula you generate is a nebula whose every artefact is also yours.

## The touch wars

The Atlas's hardest problem was never drawing. It was *touch* — because a full-screen interactive canvas on a phone is a claim on every gesture the page also needs for scrolling, and mobile browsers arbitrate that claim by rules that differ per platform and per element.

The interaction model settled early and never really changed: on touch, a tap on a point *selects* it (pulsing ring, pinned nameplate); a second tap opens it. Drags never count as taps. Browsing selects nothing — passing over a point is not a choice. What changed, round after round, was everything underneath that model:

- A restructure wrapped the canvas in a content layer that silently swallowed every pointer event over it — the animation ran beautifully on attract mode while mouse and touch were completely dead. The map looked alive and was a corpse. (The Dreamscape article's lesson about fallbacks that mimic success has a sibling: *wrappers that mimic interactivity*.)
- iOS intermittency: in the list region, most touches fell through to the touch-locked canvas and died, so scrolling only worked when a drag happened to start on a link. Safari, it turns out, reads `touch-action` from the exact element touched — it does not walk up to ancestors the way the spec's spirit suggests — so the gesture contract has to live on the surface itself, and eventually arbitration moved into raw touch events with a JavaScript direction lock: the first few pixels of a drag decide whether it belongs to the page or the map, with a hysteresis flip so the decision can't chatter.
- The end state is deliberately boring: the canvas is `pointer-events: none` — purely visual, incapable of intercepting anything, anywhere — and exactly one dedicated surface owns input, with one real scroll zone at the bottom of the first screen.

Magnetism went through the same demotion. Early builds let the probe *capture* points — a lock-on that felt possessive and wrong. The final form is a whisper: the probe light leans at most about seven pixels toward a nearby point, visual only, no capture, and selection happens when a drag *rests* near a point rather than when it passes. Restraint turned out to be the feature.

**Lesson 2: on touch platforms, the browser's gesture arbitration is part of your API surface.** It has platform-specific fine print, it will not be reasoned about from documentation alone, and the device that disagrees with you is the specification. Test on it.

## The fog: matching a look

Every visual system has a moment where it finds its face. For the Atlas fog, that moment was "v51": 256-pixel sprites, one sprite drawn at three scales, dithered, per-region palettes — Photography teal, Bookshelf rose, Dreamscape ember, Projects gold. It was settled, archived to its own branch, and declared done.

Then a demo explored a better recipe — call it *Improved*: instead of soft blobs, the fog's alpha comes from periodic fractal fields (fbm and ridge noise) cut by a density threshold, with filament sprites for structure and dust lanes carved *out* of the field with destination-out compositing, so the nebula has dark rivers running through it. The demo looked right. Porting it to the site produced a washed-out pastel haze within seconds of runtime. Twice.

The washout had a mechanism, and it generalises: the fog stamps are drawn with screen blending under a per-frame translucent fade. Screen blending only ever brightens, and a fade fill that never fully clears lets each frame's brightness *integrate* — the field climbs toward white like a long-exposure photograph. The fix was a full opaque repaint of the fog layer every frame. But even fixed, my port was a re-implementation written from notes about the demo, and it still didn't match. The recovery that worked was embarrassingly literal: lift the demo's implementation *verbatim* — its fields, its smoothstep(0.36, 0.80) density cutoff, its three-stop palettes, its home spring of 0.00015 — and transplant it whole. The look matched because it *was* the look. My verdict at the end of that round, and the fog has not been touched since: **the overall look is perfect.**

Two constraints framed the whole struggle. There is no nebula *image* on this site — a reference painting existed during development and I rejected shipping it; the fog is procedural or it is nothing. And the finished fog had to run on a phone: the final architecture renders all fog work (stamps, filaments, cores, dust lanes) to an offscreen canvas at 0.65× resolution and composites it in one blit per frame, with every look constant untouched.

**Lesson 3: porting means transplanting the actual code, not re-implementing a summary of it.** A description of a look is not the look. When a reference implementation exists, diff against it — never freehand the recipe.

## How it's built

The Atlas is two systems wearing one name: a build-time derivation and a runtime simulation.

| Half | Where | What it does |
|---|---|---|
| Derivation | The site's generator, at build time | Reads the site's own content and emits one JSON dataset: regions + items, each with a measured colour, a size, a link, and an in-cluster offset |
| Simulation | One fixed full-viewport canvas, in the browser | Fog weather, point physics, probe connections, labels, selection — repainted every frame |

What a point is made of, per kind:

| Kind | Source | Colour | Size |
|---|---|---|---|
| Photo | The gallery's photo list | Vibrant colour sampled from the image file itself | 19 |
| Book | The bookshelf data | Its cover colour, lightened | 18 |
| World | The Dreamscape artworks | Vibrant colour sampled from the artwork | 33 — the landmarks |
| Project | The project entries | Shades of the site's teal, varied by hash | 22 |
| Post | The blog's post files | Shades of violet, varied by hash | 18 |

Inside the simulation, the layering is strict. The fog lives on its own offscreen canvas (0.65×, one blit) because its repaint rules differ from everything else's. Points ride the same wander current the fog stamps use, held to their homes by springs weak enough to let border points stray into neighbouring hues — the regions are allowed to bleed at the edges, like the clusters in a real embedding plot. A persistent faint web threads each point to its two nearest same-region neighbours; the probe adds its own temporary threads to whatever is near *it*. Labels sit above their clusters, which matters more than it sounds — see the next chapter. The device pixel ratio is capped at 1.5, and iOS's habit of firing resize events as its URL bar collapses mid-scroll is ignored under 180 pixels of height jitter, because rebuilding the canvas then is a visible flash. Links are real: points carry deep links (a photo point lands on that photo, a book on that book), and the grouped list under the glass remains the plain, script-free sitemap.

## The algorithm that spaces the pieces

Everything above is prologue to this chapter, because the Atlas's most important property is the one you can't see: **nobody places it.** Not me, not a config file of coordinates. An algorithm does, on your device, every time the page loads — and the reason it exists is a crash.

When the blog launched, it added a fifth region — WRITING — to the map's data. The data was generated correctly. The page died anyway: the fog generator kept its per-region colour palettes in a hand-written table keyed by region name, WRITING wasn't in it, and the lookup threw during initialisation, taking the whole canvas down. The page's chrome rendered fine; the map was simply gone. A hand-keyed table had done exactly what hand-keyed tables do: it waited silently for the next addition and then broke everything at once.

My response, given twice that day until it became a standing rule for this site: **for layout, algorithmic changes beat manual quick fixes — the system should automatically develop as more pages and regions are added.** The fixes followed the rule, in both halves of the system:

**Style is derived, never keyed.** A region's fog palette is now computed from the region's own colour — a three-stop ramp (deep at 0.42×, the colour itself, pale pulled 72% toward white) — whenever no hand-tuned palette exists. A new region arrives styled. It cannot arrive broken.

**Position is solved, never assigned.** Each region keeps an *anchor* — a preferred spot, expressed as fractions of the viewport (Photography up-left, Bookshelf up-right, Dreamscape and Projects low, Writing high-centre). Anchors are preferences, and the runtime solver, `layoutRegions()`, treats them exactly that way:

1. **Measure the real chrome.** The solver reads the live DOM — the site header, the title-and-description card, the scroll zone — and marks each as a forbidden zone, padded by 44 pixels. Not estimated chrome: *this* device's, *this* load's.
2. **The card rule is absolute.** The title card's zone is grown by each cluster's own *reach* (its widest in-cluster offset, plus its largest point, plus margin), so no point of that cluster can slide underneath the card — not its centre, not its edge, not its label. Labels sit above their centres, so zones are extended upward by a label lift of 16% of the viewport height. Of everything the solver does, this is the one non-negotiable, in my words at the time: the most unacceptable outcome is any object under the title and description card.
3. **Project, don't push.** A centre caught inside a forbidden zone is moved to the zone's *nearest edge* — the least displacement that makes it legal. The composition survives as close to the anchors as the constraints allow.
4. **Separate the regions.** Any two centres closer than 30% of the smaller viewport dimension push each other apart, symmetrically.
5. **Relax.** Steps 2–4 iterate forty times, inside viewport margins of 7% horizontally and 6% vertically, and a final projection pass guarantees the constraints hold exactly, not approximately.

A packaged force-layout library (CoLa) was considered for this and declined — I wanted an original solver small enough to hold in my head, tuned to this page's actual priorities rather than a general graph's. The consequence is the property the whole article has been walking toward: **adding a region can no longer break the map.** It arrives with a derived palette, an anchor preference, and a solver that makes room. The map develops as the site develops, which was the point of making it a sitemap in the first place.

<figure>
<div class="figbox">
<svg viewBox="0 0 680 300" role="img" aria-label="Diagram of the layout solver: anchor positions as preferences, a forbidden card zone, and solved positions projected clear of it">
  <rect x="10" y="10" width="660" height="280" rx="10" fill="rgba(148,163,184,0.04)" stroke="rgba(148,163,184,0.25)"/>
  <rect x="255" y="34" width="170" height="58" fill="rgba(148,163,184,0.13)" stroke="rgba(148,163,184,0.45)"/>
  <text x="340" y="60" fill="#9fb4c8" font-family="var(--mono)" font-size="11" text-anchor="middle">TITLE + DESCRIPTION CARD</text>
  <text x="340" y="78" fill="#f0a35e" font-family="var(--mono)" font-size="10.5" text-anchor="middle">FORBIDDEN — grown by cluster reach</text>
  <circle cx="300" cy="120" r="7" fill="none" stroke="rgba(232,244,241,0.55)" stroke-width="1.4" stroke-dasharray="3 3"/>
  <circle cx="470" cy="70" r="7" fill="none" stroke="rgba(232,244,241,0.55)" stroke-width="1.4" stroke-dasharray="3 3"/>
  <circle cx="140" cy="200" r="7" fill="none" stroke="rgba(232,244,241,0.55)" stroke-width="1.4" stroke-dasharray="3 3"/>
  <circle cx="520" cy="215" r="7" fill="none" stroke="rgba(232,244,241,0.55)" stroke-width="1.4" stroke-dasharray="3 3"/>
  <line x1="306" y1="126" x2="238" y2="168" stroke="#5eead4" stroke-width="1.4"/>
  <line x1="464" y1="76" x2="520" y2="120" stroke="#5eead4" stroke-width="1.4"/>
  <circle cx="232" cy="174" r="7" fill="#5eead4"/>
  <circle cx="526" cy="126" r="7" fill="#f2a7c8"/>
  <circle cx="140" cy="200" r="7" fill="#f5a183"/>
  <circle cx="520" cy="215" r="7" fill="#ecd29a"/>
  <line x1="232" y1="238" x2="520" y2="238" stroke="rgba(148,163,184,0.5)" stroke-width="1" stroke-dasharray="3 4"/>
  <text x="376" y="254" fill="#9fb4c8" font-family="var(--mono)" font-size="10.5" text-anchor="middle">centres keep ≥ 30% of the smaller dimension apart</text>
  <text x="36" y="42" fill="#9fb4c8" font-family="var(--mono)" font-size="11">dashed = anchors (preferences)</text>
  <text x="36" y="60" fill="#5eead4" font-family="var(--mono)" font-size="11">solid = solved positions</text>
  <text x="180" y="152" fill="#9fb4c8" font-family="var(--mono)" font-size="10.5">projected to</text>
  <text x="180" y="166" fill="#9fb4c8" font-family="var(--mono)" font-size="10.5">nearest edge</text>
</svg>
</div>
<figcaption>FIG. 2 — THE SOLVER. ANCHORS SAY WHERE A REGION WOULD LIKE TO BE. THE SOLVER MEASURES THE REAL CHROME, FORBIDS THE CARD'S TERRITORY OUTRIGHT, PROJECTS CENTRES TO THE NEAREST LEGAL EDGE, AND ENFORCES SEPARATION — FORTY RELAXATION PASSES, ON THE DEVICE, AT LOAD.</figcaption>
</figure>

**Lesson 4: every hand-keyed table is a crash reserved for the next addition.** If a system grows by accretion, anything keyed by the list of current members is a debt instrument. Derive the value from the member itself, or default it — never require a human to remember a second list.

**Lesson 5: treat layout as a solver with priorities, not a list of coordinates.** Anchors as preferences, constraints as law, and one named outcome that outranks all others. A solver degrades gracefully on a screen nobody tested; a coordinate table just lies there, wrong.

## The record

| When | Milestone | Note |
|---|---|---|
| Oct 26 | Latent-space proof of concept | Synthetic points, prompt probe — atmosphere only |
| Oct 26 | Content-driven v2 | SSG build step; 32 real points; "how is this real?" answered in the open |
| Oct 26 | Latent Sitemap ships | Stylesheet v30; stage, glass panel, plain list below |
| Oct 26 | Full-page rebuild | Nebula becomes the page's fixed ground; list moves onto glass |
| Oct 26 | The touch wars | Styles v31–v51 in one day, most of them this page: tap model, gesture arbitration, scroll zone |
| Oct 26 | Fog v51 | Settled look #1 — sprites at 3 scales, ±2.4 dither; archived to its own branch |
| Oct 27 | The Improved fog | Demo recipe; washed-out port, full-repaint fix, verbatim transplant — "the overall look is perfect" |
| Oct 27 | Magnetism demoted | Capture becomes a ≤7px visual lean; rest-to-select |
| Oct 28 | WRITING arrives, page dies | The hand-keyed palette table meets a region it doesn't know |
| Oct 28 | derivePal + the solver | Style derived from colour; position solved per device; anchors demoted to preferences |

About the pace, since it's the part people ask about: the stylesheet version is this site's odometer, and the Atlas drove it from v30 to v51 *in a single day* — twenty-one versions, most of them rounds on this one page — with the fog generations and the solver still to come on the two days after. Thirty-plus shipped iterations in three days, every one of them live, on real devices, within hours of the last. That is not a methodology I would recommend for, say, medical software. For a personal site's living map, iteration *was* the design process: the touch model, the fog, and the solver are all things that only exist in their current form because a phone in my hand kept voting.

## Why it matters

A sitemap is supposed to be the most boring page on a site — a utility, an afterthought, a file for crawlers. This one is the site's thesis instead: that structure can be *felt* — that proximity, colour, and motion can say what a list of links says, slower and better — and that the machinery underneath can be honest about what it is. A feature space, not a fake embedding. A solver, not a coordinate table. A fog with no picture underneath it. The map is the site's content, derived fresh at every build, arranged by rules that will still work when there are sixty points and seven regions.

Including, as of this build, a point for this article — filed under WRITING, violet, size 18, placed by the solver somewhere the card isn't. I didn't choose where. That's rather the point.

*Drafted with an AI's help and edited by me — the same way most of this site gets built. The questions that started it, the standard it was held to, and every "that's not it" along the way were mine.*
