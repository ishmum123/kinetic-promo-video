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
- `$duration` — optional. Default 30–35 s silent, 45–60 s narrated (the voice sets
  the length — see `references/audio.md`). Keep under 60 s for Shorts/Reels/TikTok.
- `$audio` — **default: narrated, no music.** Write a voice-over and build the
  timeline around it unless the user asks for a silent piece. Music is the one
  thing that stays off unless explicitly requested.

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

#### 2b. No reference → derive the subject's own language first

Do **not** open `default-style.md` yet. Spend two minutes answering four
questions about the actual subject:

1. **What are the objects?** Books, jars, invoices, faces, a dashboard. These are
   what should move.
2. **What light do they live in?** Reading lamp, showroom, moonlight, screen
   glow, daylight through a window.
3. **How do they physically move?** Things with mass settle. Paper turns and
   creases. Liquids spread. Data snaps.
4. **What is the spine?** The one recurring element carrying the argument — a
   countdown, a clock crossing a night, a receipt growing, a route filling in.
   Ideally it *is* the claim, not decoration.

If those four answers give you a coherent look, build that. A skincare promo
about overnight repair gets night palette, serif type, slow settling motion and a
dial running 10pm→7am — not glowing rings.

**Fall back to the house style** when the subject genuinely suggests nothing
specific (most B2B software, abstract services). Then read
`references/default-style.md` and use it as-is: it is a complete, validated spec
(dark navy + blue glow, geometric sans, blur-in kinetic type, glowing horizon,
ring outro). Tell the user which style you're using in one line and that they can
swap it by naming a reference video — then keep going. Do not stall for approval.

**Honesty check before you build.** If your beat timings land within ~0.5 s of
the template's and the signature shots survived — the echoed word stack, the ring
bloom, the horizon-plus-slab card, blur-in as the only text move — you reskinned
the template rather than designing for the subject. That is fine when you chose
the fallback deliberately, and a defect when you didn't.

**Success criteria**: a short written spec — canvas size, fps, duration, palette
hexes, font, and the motion moves you will use — that you can point back to while
building. If you derived a subject-native language, it also names the spine and
the moves you are deliberately *not* using.

### 3. Write the beat sheet

**Read `references/audio.md` and write the voice track first** — it is on by
default. The voice owns the timeline: generate the lines, measure them, and
derive beat times from the measurements rather than fitting speech into round
numbers. Only skip this when the user asked for a silent piece.

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

A hard cut is a legitimate move: two `win()` layers sharing an exact time
boundary, entered with `steps(1,end)`, give a deliberate single-frame cut — the
right tool for a tonal snap such as story-world → flat brand color. Everything
else eases; the cut lands *because* it is the only one.

Real multicolour logos are often illegible on both dark scenes and flat brand
grounds — put the asset on a small white plate rather than recoloring it.

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

**The two views answer different questions.** The contact sheet is for structure:
timing, overlaps, dead frames, beat order. It is 270×480 per frame and it
systematically *under-reads* dark or low-contrast work — a piece that looks muddy
and broken on the sheet is often clean at full size. Judge contrast, palette and
legibility only from `--at` frames, and pull at least one per beat whenever the
palette is dark, plus one per pictogram or illustration — recognizability cannot
be judged at tile size (see Rule 12). Do not raise brightness to fix something
the sheet exaggerated.

What to hunt for on every pass:
- two pieces of text legible at once mid-transition
- anything visible before its cue (the classic `fill: 'both'` bug — see Rules)
- background elements that read as recognizable shapes instead of atmosphere
- stacked translucent blobs — overlapping alpha layers composite into visible
  intersection arcs and read as discs; use one element with a rim that dissolves
  inside its own box, sized larger than the frame
- dead frames — any moment with nothing on screen
- text or mockups crowded against the frame edges, or too small for a phone screen

**Human checkpoint**: none required, but if the user is present, show them the
contact sheet before the full render — pacing and copy notes are cheapest now.

**Success criteria**: you have viewed a contact sheet in which every frame reads
cleanly and no defect above is present.

### 7. Render and verify

```bash
python render.py                    # -> promo.mp4, ~1 screenshot per frame
# narrated pieces: mux only after the encoder process has EXITED
ffmpeg -y -i promo.mp4 -i vo/voice.wav -c:v copy -c:a aac -b:a 192k promo_av.mp4
ffprobe -v error -show_entries format=duration \
        -show_entries stream=codec_type,codec_name,width,height,nb_frames \
        -of default=noprint_wrappers=1 promo_av.mp4
ffmpeg -y -v error -i promo_av.mp4 -vf "fps=1/1.2,scale=180:320,tile=10x3" -frames:v 1 verify.png
```

**Run the full render in the background.** It is ~1 screenshot per frame — a 50 s
video is ~1500 frames and comfortably exceeds a 600 s command timeout. Poll for
the render *process* to exit, not for the mp4 to appear: the file exists on disk
long before it is finished, and muxing early gives `moov atom not found`.

Read `verify.png` — verifying the **encoded output**, not the browser, is the
point. Then delete the scratch sheets and frame directory.

**Success criteria**: ffprobe reports the expected duration, 1080×1920, and
`nb_frames == fps × duration`; for narrated pieces an audio stream is present and
the duration matches the voice bed; `verify.png` matches the beat sheet end to
end. A short file with a missing ending usually means `-shortest` met a stale
voice track — see `references/audio.md`.

### 8. Hand it over

Write a README next to the video with: the beat sheet, the rebrand constants,
the render commands, and the two harness gotchas. Then report to the user:

- where the file is and its exact specs (size, duration, fps, and whether it is
  narrated or silent — plus the TTS voice used, so it can be regenerated)
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

1. **Narrated by default, never music.** Write a voice-over and let it own the
   timeline unless the user asked for a silent piece. Music and sound design stay
   off unless explicitly requested — you cannot supply licensed tracks, and never
   pull audio from a streaming site. When you do ship a silent piece, say
   "silent" when reporting so quiet playback isn't read as a bug.

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

9. **`__ready` must wait on images, not just fonts.** Any scene containing `<img>`
   will otherwise capture its first frames with empty cells — the render succeeds
   and the output is quietly wrong. The starter's ready gate already does this;
   keep it if you rewrite the driver.

10. **Animating an SVG path's `d` across keyframes is unreliable** in headless
    Chromium — it silently does nothing or snaps. Draw two paths and crossfade
    them instead.

11. **Set `transform-origin` explicitly on any SVG group you translate and scale
    together.** The default origin is the element's own center, so the scale
    component drags the object sideways mid-move. Same failure family as the
    path-`d` rule: it renders, it's just quietly wrong.

12. **Pictograms are judged at full resolution, never on the contact sheet.** At
    tile size a line-art goat read fine; at full res it read as a beetle. Any
    object the viewer must *recognize* gets its own `--at` check. And silhouette
    animals get no eyes — an eye dot tips a pictogram from icon to life-like,
    which reads wrong and has already drawn a client correction.

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
