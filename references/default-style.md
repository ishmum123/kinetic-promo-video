# House style — "deep field"

Use this verbatim when the user gives no reference video. It is a complete spec,
already validated end to end, in the visual language of modern SaaS launch
shorts: dark, blue, typographic, weightless. It reads as premium at phone size
and costs nothing but CSS.

Tell the user in one line that you're using it and that naming a reference video
would change it. Then build — don't wait for approval.

## Canvas

1080 × 1920, 30 fps, 30–35 s.

## Palette

| Role | Value |
|---|---|
| Base | `#01040d` under `radial-gradient(120% 70% at 50% 0%, #061029, #030916 45%, #01050f)` |
| Accent | `#3b82ff` |
| Accent (type) | `#6aa1ff` |
| Accent (bright) | `#9dbcff` |
| Ink | `#eaf1ff` |
| Muted | `#94a9cf` |
| Positive | `#5fe0a4` |
| Negative | `#ff8b9c` |
| Glow | `rgba(38,102,255,.55)` |

Nothing is pure white except the horizon line's core and the logo mark's gradient
stop. Nothing is pure black except letterbox.

## Type

Poppins — geometric, round, even color. 300 for questions and body, 500 for
emphasis and feature verbs, 600 for the wordmark. Tracking `-0.5px`, line-height
`1.12`.

Sizes: `xl 104` (brand beat) · `lg 88` (primary lines) · `md 66` (secondary) ·
`sm 46` (taglines) · `xs 34` (fine print). Inside device mockups, 14–30 px.

One accented word per line, colored `#6aa1ff`, on the word carrying the meaning —
the noun or the verb, not the article. **Never italic**: geometric sans have no
true italic and the browser's synthesized oblique looks broken.

## Atmosphere (build once, runs the whole video)

- 4 blurred radial blobs, 620–1020 px, `blur(90px)`, opacity 0.24–0.40, slowly
  drifting and scaling across the full duration.
- 4 light rays: 340–560 px wide, 2400 px tall, `blur(130px)`, `mix-blend-mode:
  screen`, gradient to transparent by 78%, rotated ±16°. **Wide and soft, or they
  read as giant letter shapes.**
- 64 drifting specks, 1.6–4.4 px, soft box-shadow glow, rising and twinkling on
  staggered 7–15 s loops.
- Radial vignette to `rgba(0,0,0,.55)` at the corners.

## Motion vocabulary

| Move | Use | Timing |
|---|---|---|
| **Blur-in** — `opacity 0→1`, `blur(22px)→0`, `translateY(34px)→0`, `scale(.965)→1` | every text line | in 0.5 s, out 0.38 s |
| **Word swap** — enter `translateX(46px) skewX(-9deg) blur(16px)`, exit mirrored | rapid word cycling | in 0.22 s, out 0.18 s, one word every 0.46 s |
| **Bloom** — `scale(.25)→1` on a blurred ring + a sharp ring | brand reveal, outro | 0.75 s |
| **Rise** — `translateY(80px) scale(.94) blur(18px)` → rest | mockups, cards | 0.55–0.7 s |
| **3D slab** — `perspective(900px) rotateX(24°→12°)` rising off a glowing line | proof cards | 0.6 s |
| **Draw-on** — `stroke-dashoffset` L→0 | hand-drawn underline swooshes, arrows, ticks | 0.25–0.55 s |
| **Bar grow** — `scaleY(0)→1`, `transform-origin: 50% 100%`, staggered 45 ms | chart builds | 0.5 s |

Easing: `cubic-bezier(.16,.84,.28,1)` for entrances, `cubic-bezier(.6,.02,.9,.3)`
for exits. Entrances overshoot slightly; exits accelerate away.

## Signature shots

- **Brand reveal** — the word "Meet" stacked three times (two ghosted at 16% and
  10% opacity), which blows out as an 820 px glowing ring blooms open and the
  wordmark resolves at its center.
- **Glowing horizon** — a 1500 px white-cored line with a 60 px blue bloom, with
  translucent slabs rising behind it and a copy card standing in front.
- **Product mockups** — a dark dashboard card (KPI tiles with delta chips, a
  12-bar chart with a highlighted final bar, an annotation flag, findings rows),
  a laptop frame, a phone. All plain DOM and inline SVG.

## Structure

See `beats.md`. The default 34 s arrangement:

`hook ×3 (0–4) · brand reveal (4–7.6) · claim cycle (7.6–10.9) · verb 1 (10.9–13.7) ·
verb 2 (13.7–17.2) · verb 3 (17.2–21) · deliverable (21–24.2) · proof ×4 (24.2–29) ·
audience (29–30.6) · closer (30.6–32.6) · logo (32.6–34)`

## Variants

Same harness, different skin — swap palette and type, keep the motion:

- **Warm editorial** — `#0d0a08` base, `#ff8a3d` accent, serif display
  (Playfair, Fraunces) for lines and geometric sans for UI.
- **Clinical light** — `#f6f7fb` base, `#111` ink, single `#2f6bff` accent, no
  glow, heavier reliance on layout and whitespace. Best for enterprise/regulated.
- **Terminal** — near-black, `#00e5a0` accent, monospace, scanline overlay,
  type-on rather than blur-in. Best for developer tools.
