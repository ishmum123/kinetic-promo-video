# Beat sheet and copy

A 30-second promo is nine or ten beats. The structure below is the one nearly
every good SaaS launch short uses, because it works: name the pain, name
yourself, make one claim, prove it three ways, show the artifact, close.

## The structure

| # | Beat | Length | Job |
|---|---|---|---|
| 1 | Hook | 3–4 s | 2–3 rhetorical questions naming a pain the viewer feels *today* |
| 2 | Brand reveal | 3–3.5 s | "Meet X" + tagline. The one moment allowed to be theatrical |
| 3 | Claim | 2.5–3.5 s | Word cycle landing on the single strongest adjective + noun |
| 4–6 | Feature verbs | 2.5–3.5 s each | Three verbs — *Connect / Analyse / Decide* — each over a real mockup |
| 7 | The deliverable | 3 s | What the user actually receives. Devices. Make it tangible |
| 8 | Proof | 4–5 s | 3–4 cards, one differentiator each — the objection-handling beat |
| 9 | Audience | 1.5 s | Who it's for. Makes the viewer self-select |
| 10 | Closer | 2 s | One human line. Warmth, a little humor |
| 11 | Logo | 1.5 s | Mark, tagline, URL. Hold to the last frame |

Scale to the target runtime by cutting beats, not by speeding everything up:
20 s drops the audience beat and one feature verb; 45 s earns a second mockup
beat and a fourth verb.

## Copy rules

**Hooks name a symptom, not a category.** "Dashboards that answer nothing?" beats
"Struggling with analytics?" — the first is a Tuesday, the second is a brochure.

**Two lines, four to six words each.** One accented word per line, on the word
carrying the meaning.

**The claim beat is a cycle.** Three throwaway adjectives at ~0.46 s each, then
the one that sticks, then the noun phrase resolving underneath. The rhythm does
the work; the last word carries the argument.

**Feature verbs are imperatives.** *Connect. Analyse. Decide.* One word, big,
with a hand-drawn underline or arrow. Every verb needs a mockup under it —
verbs over empty space read as a pitch deck.

**Proof cards handle objections.** Each is a headline plus one sentence with a
concrete mechanism: *"A second model re-derives each headline number before it
ships."* Not *"Accurate and reliable."* If a card could appear in a competitor's
video unchanged, it is not proof.

**The closer is human.** One line with warmth or a small joke. It's the last
thing they remember, and it separates a real product from a template.

**Numbers must be specific or absent.** `−39%`, `2.4×`, `r = 0.81` read as real.
`+50%`, `10x`, `best-in-class` read as filler.

## Mockups

The middle third has to show software, or it's a poster with animation. Build in
DOM and CSS:

- **Dashboard card** — header with an "auto-generated" pill, 3 KPI tiles with
  delta chips, a 12-bar chart with the last bar highlighted, an annotation flag
  pointing at the anomaly, 3 findings rows with values.
- **Laptop** — 900 × 570 screen, 12 px bezel, base slab. Mini dashboard inside:
  4 KPI tiles, an area chart drawn on, a checklist.
- **Phone** — 330 × 680, 44 px radius, 10 px bezel, tilted −4°, a feed of stat
  cards. Overlap it with the laptop for depth.
- **Chips** — pill-shaped rows of integrations/sources with small stroke icons.

Numbers in mockups are illustrative. **Say so on delivery**, and swap them for
real anonymised figures before anything is published.

## Honesty

Never imply capabilities the product does not have. Never show a competitor's
brand, a real customer's name, or a fabricated testimonial, review, or press
logo. A synthetic dashboard illustrating your own product is fine; a fake
Bloomberg screenshot is not, whatever the intent. If the user asks for one, say
plainly that you'll build the mockup as clearly-their-own-product instead.
