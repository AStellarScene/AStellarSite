---
title: The Liquid Seam
date: 2026-10-28
description: The Dreamscape's worlds melt into each other along living seams. This is the full technical story — the concept, the dead ends, two silent shader deaths, and the bisection that hunted a one-pixel line.
---

<div class="seefirst">
<div class="seefirst-k">See it first</div>
<div class="seefirst-t">This post is about a visual effect, and words are the wrong medium for one. Before the story of how it was built — go watch the seams move.</div>
<a class="seefirst-a" href="dreams.html">Open the Dreamscape &rarr;</a>
</div>

The Dreamscape page on this site is a gallery of AI-generated worlds — The Golden City, the Obsidian Dragon, The Drowned Bells, The Far Shore. They are not presented as thumbnails in a grid. They share one continuous surface, and every border between them is a living seam: a slow, refracting melt that sways like the surface of a liquid, bends the artwork on both sides, and carries light along its crest. Tap a world and it opens; the seams around it rearrange and keep moving.

This post is the complete technical record of building that effect: what the idea actually was, the approaches that failed and why, the bugs that hid, and what the final engine looks like. It took four architectures and one very instructive day of failures to get a border to behave like water.

<div class="statband">
<div class="stat"><b>4</b><span>Architectures</span></div>
<div class="stat"><b>7</b><span>Bisection renders</span></div>
<div class="stat"><b>2</b><span>Silent shader deaths</span></div>
<div class="stat"><b>1 px</b><span>The last streak</span></div>
</div>

## It started with two pictures

The Golden City and the Obsidian Dragon: two AI-generated images, side by side, and a question that would not leave — *can the border between them melt?* The first version of this effect was not a grid, a quilt, or a system. It was one seam between two pictures, built to find out whether a boundary could behave like the surface of a liquid instead of a line. Everything in this post — four architectures, two silent shader deaths, a one-pixel line hunted through seven renders — grew out of that single seam.

A grid of images is a contact sheet. The pictures sit in their cells, laminated, aware of nothing. But the Dreamscape's premise — stated on the page itself — is "worlds imagined by computers." Worlds are places. Places touch each other. I wanted the boundary between two worlds to stop being a border and become a *place itself*: a membrane of liquid that both worlds press into, where the geography of one bends into the other.

Concretely, the concept had four properties that all had to hold at once:

- **The seam is shared.** There is exactly one boundary line between two worlds, computed identically from both sides. If each image computes its own edge, the two edges disagree and the seam tears.
- **The seam refracts.** Artwork doesn't just fade across the boundary — it *bends*, the way objects bend at a waterline. Alpha tricks (masks, clip paths) can carve a wavy silhouette; they cannot move pixels.
- **The seam is alive but calm.** A three-sine wave with incommensurate periods, so the motion never visibly loops; per-world drift at different rates, so the surface feels like it has depth; light coupled to the wave's slope, so it reads as a dimensional surface rather than a distortion filter.
- **The grid grows.** Worlds arrive in pairs over time. Adding a world has to be adding data — a new cell in the grid — not new machinery. Every interior edge, horizontal and vertical, including the four-way cross where four worlds meet, runs the same liquid.

I looked for an existing implementation before building one, twice — once before the first version, once with a dedicated research pass when I considered rebuilding it in pure CSS. Distortion *transitions* exist (image sliders that ripple as they swap one picture for another), and single-image displacement demos exist. A persistent, ambient grid of worlds joined by living refracting seams — doubling as the page's navigation, since tapping a world opens it — did not. As far as I can determine, this effect has never been done before. So it had to be invented, and invention leaves a paper trail. Here is the trail.

<figure>
<div class="figbox">
<svg viewBox="0 0 680 300" role="img" aria-label="Diagram of the liquid seam between two worlds">
  <rect x="10" y="10" width="660" height="280" rx="10" fill="rgba(148,163,184,0.04)" stroke="rgba(148,163,184,0.25)"/>
  <rect x="30" y="30" width="310" height="240" fill="rgba(240,163,94,0.10)"/>
  <rect x="340" y="30" width="310" height="240" fill="rgba(45,212,191,0.08)"/>
  <line x1="340" y1="30" x2="340" y2="270" stroke="#8fa8bf" stroke-width="1.5" stroke-dasharray="4 6"/>
  <path d="M 340 30 C 300 80, 382 120, 340 170 C 312 208, 372 238, 340 270" fill="none" stroke="rgba(45,212,191,0.20)" stroke-width="30"/>
  <path d="M 352 30 C 312 80, 394 120, 352 170 C 324 208, 384 238, 352 270" fill="none" stroke="#0b0f16" stroke-width="4" opacity="0.55"/>
  <path d="M 340 30 C 300 80, 382 120, 340 170 C 312 208, 372 238, 340 270" fill="none" stroke="#e8f4f1" stroke-width="2"/>
  <text x="48" y="58" fill="#f0c894" font-family="var(--mono)" font-size="13" letter-spacing="2">WORLD A</text>
  <text x="560" y="58" fill="#7de8d8" font-family="var(--mono)" font-size="13" letter-spacing="2">WORLD B</text>
  <text x="48" y="252" fill="#9fb4c8" font-family="var(--mono)" font-size="11.5">nominal grid boundary (dashed)</text>
  <text x="392" y="96" fill="#e8f4f1" font-family="var(--mono)" font-size="11.5">the melt line — one boundary,</text>
  <text x="392" y="112" fill="#e8f4f1" font-family="var(--mono)" font-size="11.5">computed identically by both cells</text>
  <text x="392" y="196" fill="#9fb4c8" font-family="var(--mono)" font-size="11.5">blend band: each world is sampled</text>
  <text x="392" y="212" fill="#9fb4c8" font-family="var(--mono)" font-size="11.5">through the other's refraction field</text>
  <text x="392" y="252" fill="#f0a35e" font-family="var(--mono)" font-size="11.5">offset crease (“groove”) — removed in v6.2</text>
</svg>
</div>
<figcaption>FIG. 1 — ANATOMY OF THE SEAM. THE WAVE DISPLACES THE BOUNDARY; ARTWORK BENDS ACROSS IT (REFRACTION) AND BLENDS INSIDE A NARROW BAND. EVERY TERM IN THIS DIAGRAM GETS ITS OWN SECTION BELOW — INCLUDING THE ONE THAT HAD TO BE REMOVED.</figcaption>
</figure>

## What "done" meant

Before the attempts, the acceptance bar, because several failures below are failures against a specific line of it:

1. **True refraction** — pixels displace, in both worlds, driven by the wave's slope.
2. **One line, two computations** — the boundary must be a single function both cells agree on, or it tears.
3. **Corners agree** — displacement tapers to zero at segment ends, so the four-way cross can't develop a ledge.
4. **Safari on a phone is a first-class target** — not a stretch goal. Any technique that is Chrome-only is a dead end by definition here.
5. **Zero dependencies** — this site's standing rule. The engine is hand-written shader code generated by the site's generator; nothing is imported.
6. **A real fallback** — if WebGL is unavailable, the page still works as a CSS gallery. (This rule later saved the page's appearance more than once — and, once, hid a corpse. See below.)

## Dead end one: pure CSS

The most attractive idea is always the one with no shader in it, so CSS got a full research pass — a dedicated deep-dive into every mechanism that could plausibly share a moving edge between two images. The findings were not close:

| Technique | Moves pixels? | One shared edge? | Safari | Verdict |
|---|---|---|---|---|
| `clip-path` / `shape()` with shared custom properties | No — carves alpha only | Yes, geometrically | Yes | A wavy silhouette, not a melt |
| CSS masks (animated SVG path) | No — alpha only | Yes | Yes | Same ceiling as clip paths |
| SVG filters (`feTurbulence` + displacement) | Yes | No — filters are per-element | Buggy; drops filters | Can't share an edge; crawls on mobile |
| Houdini Paint API | Yes, in principle | Yes | Not supported | Dead platform support |
| View Transitions | N/A | N/A | Partial | Fine for tap-to-expand; not an ambient effect |
| Seam-band crossfade (the strongest CSS design) | No — fades a pre-baked band | Approximated | Yes | A ghost-dissolve impersonation |

The strongest pure-CSS construction — static tiles with narrow seam bands, complementary animated clips, and a crossfade — still fails the first requirement on the list. A mask can decide *whether* a pixel shows. It can never decide *which* pixel shows, and refraction is entirely about which pixel shows. Working examples were built from the research; they did not look anything like the original effect. CSS remains on the page exactly where it belongs: as the fallback gallery when WebGL is unavailable.

**Lesson 1: know which requirement a technique class cannot meet, and stop early.** Every CSS mechanism failed the same single requirement — displacement — for a structural reason, not a tuning reason. No amount of polish moves a technique across a category boundary.

## First working version: one engine per pair (v3–v4)

The research that killed CSS named the winner: a hand-written WebGL fragment shader. The first working build (October 26) gave the original pair its own engine — one canvas, painting both artworks cover-fit, with the seam computed in the fragment shader:

- The boundary is a sum of three sines (swell, chop, detail) at incommensurate frequencies, parameterised along the seam.
- Inside a narrow band around the boundary, each world is sampled with an offset proportional to the wave's *slope* — that is the refraction. Steep slope, strong bend.
- Light is coupled to the same slope: a highlight on one face of the wave, shadow on the other, a specular line at the crest. This is what makes it read as a surface instead of a warp.
- The two worlds drift at different rates (roughly 1 : 0.6), which sells depth — the seam feels like a surface *between* two spaces, not a crack in one picture.

It worked, and it worked on Safari, because a fragment shader doesn't care which browser hosts it. But the architecture had a ceiling, and the ceiling was the scope: one engine per pair. The seams existed only *within* a pair, never between pairs, and every new pair meant new machinery. Against the growth property of the concept, that was a prototype wearing a production costume.

The seam's vocabulary, for the chapters ahead:

| Term | What it does |
|---|---|
| Swell, chop, detail | The three sines whose sum is the wave — a slow heave, a mid ripple, a fine shimmer |
| Refraction | The sampling offset, proportional to the wave's slope — what bends the artwork |
| Slope light | Highlight and shadow coupled to the slope, so the seam reads as a surface |
| Crest glow | A soft specular line riding the wave's crest |
| Groove | A dark crease offset inside the seam, meant as contact shadow — remember this one |
| Drift | Each world slides slowly beneath the seam at its own rate; the difference sells depth |
| Breathe | A slow global swell that scales the whole seam field |

## The scope expands: the quilt and the atlas (v5)

Then the second pair arrived — The Drowned Bells and The Far Shore — and one seam became a scope problem. Two pairs could have meant two engines, forever: every new pair another canvas, another copy of the machinery, and no seam at all where the pairs met. Or the scope could change underneath the effect: stop thinking in pairs entirely, and quilt everything into one surface.

The fix was to stop thinking in pairs. One engine renders the entire page as a single grid — the *quilt* — up to twelve cells. Each cell knows its neighbours; every interior edge runs the same seam math, horizontally and vertically, including the centre cross where four worlds meet. Adding worlds became adding cells: data, not code. The whole page is one canvas, one shader, one draw.

<figure>
<div class="figbox">
<svg viewBox="0 0 680 250" role="img" aria-label="Diagram of the scope change from one pair to the quilt">
  <rect x="10" y="10" width="660" height="230" rx="10" fill="rgba(148,163,184,0.04)" stroke="rgba(148,163,184,0.25)"/>
  <rect x="30" y="30" width="92" height="140" fill="rgba(240,163,94,0.12)"/>
  <rect x="128" y="30" width="92" height="140" fill="rgba(45,212,191,0.10)"/>
  <path d="M 125 30 C 112 65, 140 100, 125 135 C 118 152, 132 160, 125 170" fill="none" stroke="#e8f4f1" stroke-width="2"/>
  <text x="30" y="196" fill="#e8f4f1" font-family="var(--mono)" font-size="12" letter-spacing="2">ONE PAIR</text>
  <text x="30" y="214" fill="#9fb4c8" font-family="var(--mono)" font-size="11">one seam · v3</text>
  <rect x="250" y="30" width="200" height="140" fill="none" stroke="rgba(148,163,184,0.4)" stroke-width="1.2" stroke-dasharray="5 5"/>
  <rect x="262" y="42" width="82" height="52" fill="rgba(240,163,94,0.12)"/>
  <rect x="348" y="42" width="82" height="52" fill="rgba(45,212,191,0.10)"/>
  <rect x="262" y="106" width="82" height="52" fill="rgba(96,165,250,0.12)"/>
  <rect x="348" y="106" width="82" height="52" fill="rgba(74,222,128,0.10)"/>
  <text x="262" y="102" fill="#f0a35e" font-family="var(--mono)" font-size="10">no seam between pairs</text>
  <text x="250" y="196" fill="#e8f4f1" font-family="var(--mono)" font-size="12" letter-spacing="2">TWO PAIRS</text>
  <text x="250" y="214" fill="#9fb4c8" font-family="var(--mono)" font-size="11">two engines · v4</text>
  <rect x="480" y="30" width="82" height="66" fill="rgba(240,163,94,0.12)"/>
  <rect x="568" y="30" width="82" height="66" fill="rgba(45,212,191,0.10)"/>
  <rect x="480" y="102" width="82" height="68" fill="rgba(96,165,250,0.12)"/>
  <rect x="568" y="102" width="82" height="68" fill="rgba(74,222,128,0.10)"/>
  <path d="M 565 30 C 552 65, 580 100, 565 135 C 558 152, 572 162, 565 170" fill="none" stroke="#e8f4f1" stroke-width="2"/>
  <path d="M 480 99 C 515 88, 550 112, 585 99 C 610 90, 632 106, 650 99" fill="none" stroke="#e8f4f1" stroke-width="2"/>
  <circle cx="565" cy="99" r="3.5" fill="#e8f4f1"/>
  <text x="480" y="196" fill="#e8f4f1" font-family="var(--mono)" font-size="12" letter-spacing="2">THE QUILT</text>
  <text x="480" y="214" fill="#9fb4c8" font-family="var(--mono)" font-size="11">one engine, every edge · v5</text>
</svg>
</div>
<figcaption>FIG. 2 — THE SCOPE CHANGE. THE EFFECT STARTED AS ONE SEAM BETWEEN TWO IMAGES (LEFT). A SECOND PAIR WOULD HAVE MEANT A SECOND ENGINE AND NO SEAMS BETWEEN PAIRS (CENTRE). THE QUILT (RIGHT) MADE EVERY EDGE — INCLUDING THE FOUR-WAY CROSS — THE SAME LIQUID.</figcaption>
</figure>

Two problems surfaced immediately:

### The cross ledged

With the wave parameterised globally, the four edges arrived at the centre point carrying four different displacement values — so the boundary visibly *jumped* at the cross, a ledge in the melt. The fix is structural: parameterise the wave *per segment* (each edge computes its own 0-to-1 coordinate) and taper displacement to zero at both ends. If every edge is exactly at its nominal position at the corners, all four agree at the cross *by construction* — no tuning, no special case. Neighbours sharing an edge compute the identical segment coordinate, so the line still cannot tear mid-edge.

### The atlas taxed growth

One shader needs the artworks in GPU memory, and the v5 way was a single texture atlas: all worlds packed into one 4096² texture. That is a fixed budget divided by the number of worlds — each world got a 2048² cell at four worlds, and the share halves with every doubling. I shipped it; the person who caught the flaw was the one reading over my shoulder, in one sentence: *"adding more images will over time reduce quality."* Correct, and it's an asymptote, not a bug — the architecture itself expires as the collection grows. A tablet also exposed a related failure: the atlas path could fall back to a half-resolution mosaic when the packed texture pressed against device limits. The atlas had to go.

<figure>
<div class="figbox">
<svg viewBox="0 0 680 245" role="img" aria-label="Bar chart of atlas cell width per world as the collection grows">
  <rect x="10" y="10" width="660" height="225" rx="10" fill="rgba(148,163,184,0.04)" stroke="rgba(148,163,184,0.25)"/>
  <text x="30" y="48" fill="#9fb4c8" font-family="var(--mono)" font-size="11.5">4 WORLDS (2×2)</text>
  <rect x="185" y="34" width="400" height="20" fill="rgba(45,212,191,0.35)"/>
  <text x="595" y="48" fill="#e8f4f1" font-family="var(--mono)" font-size="11.5">2048 px</text>
  <text x="30" y="90" fill="#9fb4c8" font-family="var(--mono)" font-size="11.5">9 WORLDS (3×3)</text>
  <rect x="185" y="76" width="267" height="20" fill="rgba(45,212,191,0.28)"/>
  <text x="462" y="90" fill="#e8f4f1" font-family="var(--mono)" font-size="11.5">1365 px</text>
  <text x="30" y="132" fill="#9fb4c8" font-family="var(--mono)" font-size="11.5">12 WORLDS (4×3)</text>
  <rect x="185" y="118" width="200" height="20" fill="rgba(45,212,191,0.20)"/>
  <text x="395" y="132" fill="#e8f4f1" font-family="var(--mono)" font-size="11.5">1024 px</text>
  <text x="30" y="182" fill="#f0c894" font-family="var(--mono)" font-size="11.5">PER-WORLD TEXTURES</text>
  <rect x="185" y="168" width="400" height="20" fill="none" stroke="#d9b36a" stroke-width="1.5" stroke-dasharray="6 4"/>
  <text x="595" y="182" fill="#f0c894" font-family="var(--mono)" font-size="11.5">always native</text>
  <text x="30" y="216" fill="#9fb4c8" font-family="var(--mono)" font-size="11">ATLAS CELL WIDTH PER WORLD, FROM ONE FIXED 4096² TEXTURE</text>
</svg>
</div>
<figcaption>FIG. 3 — THE ATLAS BUDGET. EVERY WORLD ADDED TO A FIXED ATLAS SHRINKS THE WORLDS ALREADY THERE. PER-WORLD TEXTURES (GOLD) NEVER DIVIDE.</figcaption>
</figure>

**Lesson 2: prefer the design whose cost doesn't scale against the collection.** Per-world textures cost the same per world forever. The atlas cost less today and more every day after.

## The day the shader died twice

The WebGL2 rebuild (v6) replaced the atlas with one texture per world at native resolution, moved the seam blends into linear space (blending in gamma space was mathematically darkening every seam midpoint — the mix of two values was landing darker than either), and switched to explicit-gradient sampling so mip selection stays correct under refraction. It shipped, was verified live byte-for-byte, and rendered — on the checking browser — as a page of static zigzag-edged images. That is the CSS fallback. The shader was dead. It had, in fact, been dead for hours *before* the rebuild, and the investigation that followed found two separate corpses.

### Death one: a name, mangled by a string replace

The shader is generated code: the generator stamps out four near-identical blocks of GLSL, one per side of a cell, by substituting a placeholder letter. The substitution was a blind split on the character `S` — and a variable introduced that morning was named `cellSize`. The stamper ate the `S` inside it and emitted `cell0ize`, an undeclared identifier. The fragment shader failed to compile, the engine bailed silently, and the fallback — which *imitates* the melt with zigzag clip-paths — took over so convincingly that my own render check certified the page as working. Screenshots were taken, comparisons were made, an architecture debate was held — about a fallback.

> A still image cannot distinguish the engine from its fallback, especially when the fallback is designed to look like the engine. The only honest liveness check for an animated effect is witnessing motion.

### Death two: the spec is not the terrain

The v6 shader indexed its texture array with a loop variable — legal GLSL ES 3.00. It compiled nowhere that matters: ANGLE, the translation layer inside both Chrome's and Safari's WebGL stacks, rejects it outright:

```
ERROR: 0:32: '[' : array index for samplers must be constant integral expressions
```

That error was not found in a console I couldn't read (the checking browser can't evaluate JavaScript or show console output). It was found by building a throwaway page that compiles the exact production shaders and prints the compiler's verdicts as page text. One round trip ended hours of screenshot arguments. The fix — branching on literal texture indices — was verified against ANGLE *before* it shipped, and the engine grew a **degradation ladder** so no single rejected construct can ever dark the quilt again:

| Rung | Path | When |
|---|---|---|
| 1 | WebGL2, GLSL ES 3.00, per-world sRGB textures | Any modern browser |
| 2 | WebGL2 context, ES 1.00 dialect, texture atlas | ES 3.00 program rejected by the driver |
| 3 | WebGL1, ES 1.00, texture atlas | No WebGL2 |
| 4 | CSS gallery (zigzag splits, drifting images) | No WebGL at all |

The page carries a `data-gl` attribute naming the rung that engaged. Nothing about the fallback is silent anymore — that was the actual bug in both deaths: not that shaders failed, but that failure had no voice.

**Lesson 3: a fallback that mimics success is the most dangerous failure mode a system can have.** It converts errors into confident wrong answers. Every silent path in a system should be made to announce itself.

**Lesson 4: generated code needs collision-proof generation.** A placeholder token must be a pattern that can only mean the placeholder — a word-final marker with a boundary rule — never a bare common letter. And after any edit to generated output, verify the *rendered result*, not the strings around the edit.

**Lesson 5: the vendor translator is the contract, not the specification.** Test against the real compiler your users run. When you can't see the console, make the page print its own verdicts.

## The line

With v6.1 live, the melt finally ran everywhere — and a thin, straight, black line appeared, riding exactly along both grid boundaries underneath the moving wave. It was not the fallback (the wave flowed over it), not a gap between cells (the grid has none), and not dirt in the artwork (it crossed four different images at the same coordinate). It was found the way the ANGLE error should have been: not by staring, but by **bisection** — rendering the same seam with exactly one term changed at a time and letting the renders vote.

| Variant | Change | Centre line | Seam character |
|---|---|---|---|
| A | As shipped | **Present, bold** | Dimensional |
| B | Neighbour refraction ×1.6 → ×1.0 | Present | Dimensional |
| C | All seam shading off | **Gone** | Flat |
| D | Groove off only | **Gone** | Dimensional |
| E | Glow off only | Present | Dimensional, less halo |
| F | Slope light off only | Present | Flat |
| G | All three softened (groove at 0.02) | Faint trace | Dimensional, softer |

The culprit was the **groove**: a deliberate dark crease, offset 4.5 device pixels inside the seam, meant to read as contact shadow. Its depth constant (0.05) had been tuned in the gamma-space era. In the linear pipeline the same number lands up to twice as hard in dark tones — the crease printed as a hard line that the eye reads straight even though it technically follows the wave.

Variant G is the instructive one: softening everything *almost* worked, but the trace remained because the groove survived at 0.02. Half-measures kept the culprit alive; removing it (v6.2) killed the bold line outright while the slope light and glow kept the seam's dimension. The heavy dark band visible along the seams on iPhone Safari was the same term.

**Lesson 6: when an artifact has multiple plausible parents, bisect by rendering variants — one variable per render.** Guessing would have "fixed" the refraction first (it was the most suspicious-looking term) and changed nothing, twice.

## The last streak

One remnant survived v6.2: a one-pixel grey streak at the exact centre of the bottom row, visible only where The Far Shore's bright sky and grass gave it contrast, in the stretches where the wave bulges far from the boundary. This one was not a shading term at all — it was in the *sampled field*. A world is sampled through two code paths: as the cell that owns a pixel (with its accumulated refraction), and as the *neighbour* of the cell that owns the pixel across the boundary (with that side's refraction, amplified ×1.6). Two different refraction values for the same world means the world's image steps sideways where the paths hand over — which is, precisely, the straight boundary.

Busy artwork hides a few texels of sideways step. A smooth sky gradient cannot.

The fix (v6.3) is a principle rather than a patch: **a world's sampled image must be a single function of position.** The neighbour sample recomputes the neighbour's *own* refraction field at that point — its four side terms, its rect, its tables — so both paths evaluate the identical function. Continuity across the boundary stops being tuned and becomes true by construction.

And then v6.3 was rolled back, the same day, on my call — which is also part of the record. It compiled cleanly, it rendered identically, and on a real phone it *stuttered*: recomputing four side terms for every neighbour sample roughly tripled the fragment cost inside the seam band, and the band is exactly where the eye lives. The streak it removed was visible at capture resolution, to a checker zoomed into the brightest sky on the page. It was not visible to me, on my devices, looking at the thing I built. I had already called v6.2 perfect once, in passing, and the rollback made it official: **v6.2 is the final engine.** The unified field stays in the version history as the correct answer to a question that turned out not to need asking at that price.

**Lesson 7: if the same quantity is computed two ways, the seam between the two ways will eventually become visible.** Unify the function; don't tune the discrepancy. **Corollary: a fix is priced per frame.** An artifact nobody can see does not get to tax every pixel, forever, to erase itself.

## The record

Nine engine versions in three days. The pace is part of the record, not a footnote to it: every version below was live, on real devices, within hours of the one before it, and most of what the later versions know was taught by a screenshot of the earlier one failing.

| Version | Date | Architecture | Fate |
|---|---|---|---|
| v1–v2 | Oct 25–26 | CSS bands, membrane seams | Superseded — no displacement possible |
| v3–v4 | Oct 26 | WebGL1, one engine per pair | Worked; couldn't grow |
| v5 | Oct 28 | One quilt engine, texture atlas | Cross ledge fixed; atlas scaling flaw |
| — | Oct 28 | (Ledge fix) | Killed the shader via codegen for hours, unnoticed |
| v6.0 | Oct 28 | WebGL2, per-world textures, linear blends | Never started — ANGLE rejected the shader |
| v6.1 | Oct 28 | Literal-index sampling + degradation ladder | The melt runs everywhere; a line appears |
| v6.2 | Oct 28 | Groove removed | The bold line dies; a faint streak remains |
| v6.3 | Oct 28 | Unified refraction field | Correct, and rolled back — tripled seam-band cost; v6.2 stands |

And the final state of the engine, for the record:

| Property | Value |
|---|---|
| Textures | One per world, native resolution, sRGB |
| Blending | Linear space; single gamma encode at output |
| Grid capacity | 12 worlds (uniform arrays); adding one is data only |
| Dependencies | None — one generated shader, vanilla JS |
| Fallbacks | 4 rungs, each announced via `data-gl` |
| Interaction | Tap a world to open it; seams follow the layout animation |
| Motion ethics | `prefers-reduced-motion` gets a still frame; DPR governor protects frame rate |

## Why any of this matters

Strip the specifics away and the day's lessons are not really about shaders:

1. **Know the category limit of your tools** (CSS could not displace; no tuning changes that).
2. **Choose the scaling law you can live with** (the atlas was cheaper today and worse forever).
3. **Make failures loud** (a mimicking fallback turned two dead shaders into hours of confident wrong conclusions).
4. **Generate code defensively** (a one-letter placeholder ate a variable name and a morning).
5. **Test against the real translator, not the spec** (ANGLE is the contract).
6. **Bisect, don't guess** (seven renders convicted one term; two plausible alternatives were innocent).
7. **Unify duplicate computations of the same quantity** (the last streak was two code paths disagreeing about one number) — and price the unification per frame before shipping it (v6.3's corollary).

The effect itself is the site's thesis in miniature: AI imagined the worlds, but the machinery that joins them is hand-built, dependency-free, and — as this post documents at probably excessive length — debugged the slow way, in the open, until the border between two imagined places behaved like the surface of the same water.

*Drafted with an AI's help and edited by me — the same way most of this site gets built. The over-shoulder quality catch in the atlas section was mine; so was every screenshot that moved this along.*
