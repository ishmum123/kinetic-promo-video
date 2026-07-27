# Audio — voice-led promos

**Narration is on by default.** Read this whenever you are building a promo,
unless the user asked for a silent piece. Music is the thing that stays off
unless explicitly requested.

The important idea: **when there is a voice, the voice owns the timeline.** Do not
write a beat sheet in round numbers and then try to fit speech into it. Generate
the speech first, measure it, and derive every beat time from the measurements.

## The pipeline

```
script -> TTS per line -> measure durations -> schedule with gaps
       -> cues.js -> scene.html reads it -> render -> mux
```

One line per file, never one long clip: you need per-line durations to place
beats, and a single clip cannot be re-timed.

### 1. Write the script as discrete lines

Short lines. Each line is one beat's worth of copy. Keep the on-screen text and
the spoken text related but not identical — reading along with a narrator is
tiring, and many viewers watch muted, so the key phrase must be on screen.

### 2. Synthesize and measure

```bash
edge-tts --voice en-US-AndrewNeural --text "..." --write-media 01.mp3
ffprobe -v error -show_entries format=duration -of default=nw=1:nk=1 01.mp3
```

### 3. Schedule

Lay the lines out with explicit gaps. Gaps are real silence and real screen time
— they are where a beat lands, not dead air. 0.3 s inside a section, 0.5 s at a
section boundary is a reasonable start. Add a lead-in (~1 s) and a tail (~1.5 s).

Total duration is then a *result*, not a target. Do not compress a script to hit
30 s; ask the user first, since a voiced promo commonly runs 45–60 s.

### 4. Emit `cues.js`, and have the scene read it

```js
window.__DUR  = 50.15;
window.__CUES = { "01": {t:1.00, d:4.51, end:5.51, text:"..."}, ... };
```

In `scene.html`:

```js
const C = window.__CUES, DUR = window.__DUR;
const IN = k => C[k].t, OUT = k => C[k].end;
/* then: benefit({k:'05', ...}) uses IN('05') / OUT('05'), never a literal */
```

This is the whole point. With hardcoded timestamps, changing the speaking rate
means hand-editing every beat. With `cues.js`, you regenerate and re-render.

### 5. Mux, after the video encode has fully finished

The standard shape: render the video to a **silent master** and mux into a
separate file, keeping the master.

```bash
python render.py --out promo_silent.mp4
ffmpeg -y -i promo_silent.mp4 -i voice.wav -c:v copy -c:a aac -b:a 192k promo.mp4
```

A bad mux, a voice re-take, or a tempo change then costs seconds, never a
re-render — cheaper and simpler than `--keep-frames`.

## Traps

1. **Regenerating the voice means regenerating BOTH `voice.wav` and `cues.js`.**
   Muxing a stale voice bed against a new video, or vice versa, is the single
   easiest way to lose a render.

2. **`-shortest` silently truncates to whichever stream is shorter.** A stale
   45 s voice bed against a 50 s video yields a 45 s file with the ending gone,
   and ffmpeg reports success. Omit `-shortest` unless you want that, and always
   verify:

   ```bash
   ffprobe -v error -show_entries format=duration \
           -show_entries stream=codec_type,nb_frames -of default=nw=1 promo.mp4
   ```

   `nb_frames` must equal `fps × DUR`. Check it before you believe the output.

3. **Do not mux over your only copy.** `render.py` cleans up its frame directory
   when it finishes, so a bad mux over the encode cannot be fixed by re-encoding
   — it costs a full re-render. The silent-master shape above makes this
   impossible; use it rather than `--keep-frames`.

4. **Wait for the encoder to exit.** The mp4 exists on disk long before it is
   finished; muxing early gives `moov atom not found`. Poll for the render
   process to exit, not for the file to appear.

## Engines

### English — edge-tts (Microsoft neural voices)

Simplest good option. No API key, no account.

```bash
pip install edge-tts
edge-tts --list-voices | grep en-US
edge-tts --voice en-US-AndrewNeural --rate=-8% \
         --text "..." --write-media 01.mp3
```

`en-US-AndrewNeural` (warm, confident, conversational) is a solid default for a
promo read. `en-US-AriaNeural` and `en-US-BrianNeural` are reasonable
alternatives; the `*MultilingualNeural` variants handle mixed-language copy.

It has native `--rate`, `--pitch` and `--volume`, so pace the read at synthesis
time rather than time-stretching afterwards.

### Other languages / local models

A local model may be the only option for some languages. Two things to check
before building a timeline on one:

- **Pace.** Local TTS is often slow and flat. If there is no rate parameter,
  time-stretch with pitch-preserving `atempo` — `ffmpeg -af atempo=1.10`. Stay
  under about 1.25x; beyond that it audibly chipmunks. Check for leading and
  trailing silence with `silencedetect` before assuming a clip is slow: padding
  and slow delivery need different fixes.
- **Output format.** Confirm what you actually get rather than trusting the
  declared content type — `file` and `ffprobe` on the first clip. An endpoint
  documented as returning JSON may return raw WAV bytes.

For any engine: write URLs and Latin brand names phonetically in the script's
own language ("acme dot com" spelled out in the script's own alphabet, not
`acme.com`) — otherwise TTS spells them out letter by letter.

## Music

Off unless explicitly asked for — this is the one part of the audio default that
stays negative. You cannot supply licensed music: either the user provides the
file, or the piece stays voice-only. Never fetch audio from a streaming site.

Voice-only is not a compromise. A narrated promo with clean silence between lines
reads as deliberate; the gaps are where beats land.
