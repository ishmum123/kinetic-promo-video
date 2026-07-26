# Tearing down a reference video

The goal is a written spec you can build against — not a vibe. Twenty minutes
here saves an hour of rendering things that don't look like the target.

## 1. Get the file

```bash
yt-dlp -f "bv*+ba/b" -o ref.%\(ext\)s "<url>"
```

Works for YouTube (including `/shorts/`), TikTok, Reels, Vimeo. If it fails
(private, region-locked, DRM), ask the user for a local file or a few
screenshots. Do not proceed on the strength of a title or description — page
metadata tells you nothing about motion design.

## 2. Probe it

```bash
ffprobe -v error -show_entries stream=width,height,r_frame_rate,codec_type \
        -show_entries format=duration -of default=noprint_wrappers=1 ref.webm
```

Record: canvas size, fps, duration. Match the canvas exactly. Match the duration
only in spirit — copy the *pacing*, not the runtime.

## 3. Look at it

```bash
ffmpeg -y -v error -i ref.webm -vf "fps=1,scale=270:480,tile=8x2" -frames:v 2 sheet%d.png
```

One frame per second, tiled. **Read the sheets with the Read tool.** For a
30-second video this is two images and it shows you the entire structure at once.

Go finer on any beat you can't read:

```bash
ffmpeg -y -v error -ss 12 -t 4 -i ref.webm -vf "fps=6,scale=270:480,tile=6x4" -frames:v 1 beat.png
```

## 4. Write the spec

Answer all seven, in writing, before touching code:

1. **Canvas** — dimensions, fps, total duration.
2. **Palette** — background gradient, accent color, text colors. Pull real hexes
   off the frames rather than guessing; the difference between `#3b82ff` and
   "blue" is the difference between matching and not.
3. **Type** — one family or two? Weights? Geometric (Poppins, Circular, Futura)
   or humanist (Avenir, Inter)? Tight or loose tracking? Which words get the
   accent color, and is the accent on the noun or the verb?
4. **Beat structure** — a table of t-range → what's on screen. This is the most
   valuable output. Most SaaS promos run: hook question(s) → brand reveal →
   claim → feature verbs → product mockups → proof points → audience → closer →
   logo lockup.
5. **Motion vocabulary** — the specific moves, and how long each takes.
   Blur-in? Directional word swaps with motion blur? Scale-and-bloom? 3D card
   rises? Draw-on stroke doodles? Note durations: 0.4–0.6 s entrances and
   0.2–0.4 s exits are typical.
6. **Depth** — how is atmosphere built? Blurred color blobs, volumetric rays,
   drifting particles, vignette, glow ring, glowing horizon line.
7. **Signature shot** — the one frame someone would remember. Reproduce it.

## 5. Translate, don't clone

Match the *system* — palette, type, motion vocabulary, pacing — and write new
copy and new mockups for the user's product. Copying a competitor's exact script
or logo is not the assignment and is not defensible.

Note anything you deliberately dropped and why (a 3D product render you can't
reproduce in CSS, licensed footage, a specific licensed typeface). Tell the user
in one line rather than silently shipping something thinner than the reference.
