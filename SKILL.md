---
name: kinetic-promo-video
description: Produce a finished vertical promo video (mp4) for a product, service, or brand - kinetic typography, animated UI mockups, motion-graphics polish - by writing a deterministic HTML timeline and frame-rendering it with a headless browser and ffmpeg. Matches the look of a reference video when the user supplies one (YouTube/TikTok/Reels URL or local file), and falls back to a validated built-in house style when they do not. Use whenever the user asks for a promo, ad, explainer, launch, teaser, demo, or trailer video, a Short/Reel/TikTok, "a video like <link>", or an animated version of a landing page - even when they have no editor, no footage, and no designer.
---

# Kinetic Promo Video

Build a broadcast-looking vertical promo video from nothing but a description of
the business. The video is authored as a **single HTML page driven by a paused
master clock**, then rendered frame by frame and encoded. No editor, no stock
footage, no timeline app — and every frame is reproducible from a timestamp.

## Inputs

- `$brief` — what the thing is, who it's for, what makes it different. Required.
  Pull it from the conversation, the repo's README, or ask.
- `$reference` — optional. A video URL or local file whose look should be matched.
- `$brand` — optional. Name, tagline, URL, colors, logo. If absent, use a clearly
  flagged placeholder (never silently invent a brand and present it as final).
- `$duration` — optional. Default 30–35 s. Keep under 60 s for Shorts/Reels/TikTok.
- `$audio` — **default: silent.** Only add sound if the user explicitly asks.

## Goal

`promo.mp4` — 1080×1920, 30 fps, H.264, playable and correct on first watch —
plus the `scene.html` that generated it, a `render.py` that reproduces it, and a
README with the beat sheet and the constants to rebrand it. Success is not "a
file exists": it is **frames you have looked at** that read cleanly, with no
overlapping text, no elements visible before their cue, and no dead air.

## Steps

### 1. Check the toolchain

```bash
which ffmpeg ffprobe yt-dlp python3
python3 -m venv .venv && .venv/bin/pip install -q playwright && .venv/bin/playwright install chromium
```

`ffmpeg` and a Chromium for Playwright are hard requirements. `yt-dlp` is needed
only for reference teardown. Prefer a venv — the user's system Python may be
externally managed.

**Success criteria**: `ffmpeg -version` works and
`.venv/bin/python -c "from playwright.sync_api import sync_playwright; sync_playwright().start().chromium.executable_path"`
prints a path.

### 2. Establish the visual target

**Two paths — pick by whether `$reference` exists.**

#### 2a. Reference given → tear it down

Read `references/teardown.md` and follow it. In short: download it, probe it,
extract 1 fps contact sheets, **actually Read the sheet images**, and write down
dimensions, duration, palette, type treatment, beat structure, and motion
vocabulary before writing any code.

Never describe a reference you have not looked at frame by frame. A page's title
or description tells you nothing about its motion design.

#### 2b. No reference → use the house style

Read `references/default-style.md` and use it as-is. It is a complete,
opinionated spec (dark navy + blue glow, geometric sans, blur-in kinetic type,
glowing horizon, ring outro) that has already been validated end to end. Tell the
user which style you're using in one line and that they can swap it by naming a
reference video — then keep going. Do not stall for approval.

**Success criteria**: a short written spec — canvas size, fps, duration, palette
hexes, font, and the motion moves you will use — that you can point back to while
building.

### 3. Write the beat sheet

Read `references/beats.md` for the structure and copy rules, then map the user's
**actual** differentiators onto beats. The middle third is where the product is
sold: it must contain the specific reasons this thing is better, not adjectives.

Write the beat sheet out as a table (t-range → beat) before writing code. Getting
the pacing wrong is far more expensive to fix after the scenes are built.

**Artifacts**: beat table with explicit second ranges summing to `$duration`.

**Success criteria**: every beat traces to something real about the product, and
the ranges are contiguous with no gaps > 0.3 s.

### 4. Scaffold from the templates

`$SKILL` below is this skill's own directory — the one holding this SKILL.md.

```bash
mkdir -p video && cp "$SKILL/templates/render.py" video/
cp "$SKILL/templates/scene-starter.html" video/scene.html
bash "$SKILL/templates/fetch-fonts.sh" video/fonts     # Poppins subsets, ~40 KB
```

`scene-starter.html` already contains the animation harness (`seek`, `win`, `io`,
`pop`, `swap`, `draw`, seeded RNG, atmosphere) and seven example beats covering
every pattern worth copying. **Do not rewrite the harness** — it encodes the bugs
listed under Rules. Replace the example beats; keep everything above them.

**Success criteria**: `python render.py --contact` produces `contact.png` from the
untouched starter.

### 5. Build the scenes

One IIFE per beat, each creating its own `layer()` gated by `win(layer, tIn, tOut)`.
Inside, every animated element gets exactly one `io()` / `pop()` / `swap()` call.

Build UI mockups (dashboards, phones, laptops, cards, chips) as plain DOM + CSS
and animate them in — they carry the "real product" feel that pure type cannot.
Charts are divs and inline SVG; no chart library, no images, no external requests.

**Rules**: see the Rules section. They are not style preferences — each one is a
specific failure this skill has already hit.

**Success criteria**: `python render.py --contact` renders without errors.

### 6. Preview loop — look at every frame

```bash
python render.py --contact          # 24-frame overview, ~20 s
python render.py --at 6.2 12.0 19.5 # specific moments, full resolution
```

**Read the resulting PNGs with the Read tool and inspect them.** Then fix and
repeat. Iterate here until the sheet is clean — a full render is 10× slower, so
never use it as your feedback loop.

What to hunt for on every pass:
- two pieces of text legible at once mid-transition
- anything visible before its cue (the classic `fill: 'both'` bug — see Rules)
- background elements that read as recognizable shapes instead of atmosphere
- dead frames — any moment with nothing on screen
- text or mockups crowded against the frame edges, or too small for a phone screen

**Human checkpoint**: none required, but if the user is present, show them the
contact sheet before the full render — pacing and copy notes are cheapest now.

**Success criteria**: you have viewed a contact sheet in which every frame reads
cleanly and no defect above is present.

### 7. Render and verify

```bash
python render.py                    # -> promo.mp4, ~3 min for 34 s
ffprobe -v error -show_entries format=duration -show_entries stream=width,height,nb_frames \
        -of default=noprint_wrappers=1 promo.mp4
ffmpeg -y -v error -i promo.mp4 -vf "fps=1/1.2,scale=180:320,tile=10x3" -frames:v 1 verify.png
```

Read `verify.png` — verifying the **encoded output**, not the browser, is the
point. Then delete the scratch sheets and frame directory.

**Success criteria**: ffprobe reports the expected duration, 1080×1920, and
`fps × duration` frames; `verify.png` matches the beat sheet end to end.

### 8. Hand it over

Write a README next to the video with: the beat sheet, the rebrand constants,
the render commands, and the two harness gotchas. Then report to the user:

- where the file is and its exact specs (size, duration, fps, **silent**)
- the beat table
- **every placeholder and invented number, called out explicitly** — brand names,
  URLs, and any metric shown in a mockup. Say plainly that fabricated figures must
  be replaced before publishing if the claims need to be defensible.
- that there is **no shareable link** — it is a local file — unless the user asked
  for hosting

Offer to open it: `open promo.mp4`.

**Rules**: never commit or publish without explicit approval. Never upload the
video anywhere as a side effect of producing it.

**Success criteria**: the user knows the file path, what is placeholder, and how
to change it.

## Rules

Hard constraints. Each is a failure this pipeline has already produced.

1. **Silent by default.** No music, no sound design, unless explicitly requested.
   Say "silent" when reporting, so quiet playback isn't read as a bug.

2. **One animation per element, covering enter → hold → exit.** Two separate
   WAAPI animations with `fill: 'both'` fight: the exit clip applies its *first*
   keyframe from `t = 0`, pinning the element visible for the entire video. The
   `io()` helper exists solely to prevent this. Symptom: everything in a scene
   appears at once at the scene's start instead of animating in.

3. **Consecutive text must fully exit before the next enters.** Two legible lines
   on screen mid-crossfade reads as a rendering bug, not a transition. Schedule
   line N's exit to complete before line N+1's entrance begins.

4. **Determinism is non-negotiable.** Seed the RNG. Never call `Date.now()`,
   `Math.random()`, or `new Date()` at render time — the renderer seeks the same
   timeline thousands of times and any wall-clock input produces flicker.

5. **Background must stay atmosphere.** Light rays, blobs, and particles need
   large blur radii, wide extents, and low opacity. Narrow rotated gradient bars
   read as giant letter-shaped artifacts across the frame.

6. **Never claim it looks good without looking.** Read the contact sheet. The
   renderer will happily produce 1000 frames of a broken layout.

7. **Flag every fabrication.** Placeholder brand names and invented metrics are
   fine for a draft and dishonest if presented as final. List them on delivery.

8. **Vertical, 1080×1920, 30 fps, under 60 s** unless the user says otherwise.
   Type below ~30 px is unreadable on a phone; mockup body text should sit at
   16–24 px only inside a device frame, never as primary copy.

## Edge cases

- **`yt-dlp` fails or the reference is private** — ask for a local file or
  screenshots; if neither, fall back to `default-style.md` and say so.
- **No Chromium** — `playwright install chromium` needs network. Without it,
  there is no renderer; stop and tell the user rather than producing nothing.
- **Fonts unavailable offline** — `fetch-fonts.sh` needs network once. Fall back
  to a geometric system font (`Futura`, `Avenir Next`, `Century Gothic`) and note
  the substitution.
- **Emoji** render via the system emoji font; verify in a contact sheet, since
  they are a common cause of tofu boxes in headless Chromium on Linux.
- **Render is slow** — it is ~1 screenshot per frame. 34 s ≈ 1020 frames ≈ 3 min.
  Do not "optimize" by dropping to 24 fps without asking; the motion blur in the
  transitions is tuned for 30.
- **User wants a different aspect** — 16:9 or square: change the `#stage` size and
  the `W`/`H` constants in `render.py` together, then re-check every scene's
  absolute `top:` values, which are tuned for 1920 height.
