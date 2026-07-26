# kinetic-promo-video

An [Agent Skill](https://agentskills.io) that produces a **finished vertical
promo video** from a description of your product: kinetic typography, animated
UI mockups, motion-graphics polish. No editor, no stock footage, no timeline app,
no designer.

Give it a reference video and it matches that look. Give it nothing and it uses a
validated house style.

## Install

```bash
npx skills add ishmum123/kinetic-promo-video
```

## Use

> make me a promo video for this repo — 30 seconds, vertical

> make me a video like https://youtube.com/shorts/XXXX for my business

You get `promo.mp4` (1080×1920, 30 fps, H.264, silent by default), the
`scene.html` that generated it, a `render.py` that reproduces it, and a README
with the beat sheet and the constants to rebrand it.

## Why HTML instead of an editor

The video is authored as a **single HTML page driven by a paused master clock**.
`seek(t)` sets `currentTime` on every animation, so any frame is reproducible
from a timestamp alone. `render.py` serves the folder, seeks frame by frame with
Playwright, screenshots each frame, and pipes them into ffmpeg.

```
reference teardown ─┐
                    ├─► beat sheet ─► scene.html ─► contact-sheet loop ─► promo.mp4
   house style     ─┘                  (harness)      (look at frames)
```

Three things that buys you: every frame is deterministic, the whole video is a
diffable text file, and rebranding is three constants.

## Requirements

| Tool | Needed for |
|---|---|
| `ffmpeg` / `ffprobe` | encoding, contact sheets |
| `python3` + `playwright` (chromium) | frame rendering |
| `yt-dlp` | optional — only to tear down a reference video |

```bash
brew install ffmpeg yt-dlp
python3 -m venv .venv && .venv/bin/pip install playwright && .venv/bin/playwright install chromium
```

## What ships with it

```
SKILL.md                     the pipeline, the rules, the edge cases
references/teardown.md       reference video → a written spec you can build to
references/default-style.md  the house style, complete, plus three variants
references/beats.md          beat structure and copy rules
templates/scene-starter.html animation harness + seven example beats
templates/render.py          frame renderer / encoder
templates/fetch-fonts.sh     Poppins woff2 subsets, ~40 KB, for offline renders
```

## The rules it enforces

Each one is a failure this pipeline has already produced:

- **One animation per element, covering enter → hold → exit.** Two separate Web
  Animations with `fill: 'both'` fight — the exit clip applies its first keyframe
  from `t = 0` and pins the element visible for the entire video.
- **Consecutive text fully exits before the next enters.** Two legible lines
  mid-crossfade reads as a rendering bug, not a transition.
- **Never claim it looks good without looking.** The renderer will happily
  produce 1000 frames of a broken layout, so the loop is: contact sheet → read
  the image → fix → repeat.
- **Background stays atmosphere.** Narrow rotated gradient bars read as giant
  letter shapes across the frame; rays need width, heavy blur, low opacity.
- **Silent by default**, and every placeholder brand or invented metric is called
  out on delivery rather than quietly shipped as fact.

MIT.
