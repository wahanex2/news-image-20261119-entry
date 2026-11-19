# The World in One Day — Thursday 19 November 2026

A one-page broadsheet summing up the world's news of Thursday 19 November
2026, drawn entirely in code with PIL. Entry for the make.fun competition
`news-image-20261119`.

## What's on the page

38 stories, every one of them first reported on Thursday 19 November 2026:

- **13 illustrated cards** — the day's biggest stories, each with a custom
  flat-scene illustration drawn in code: the Xi–Trump–Putin three-way summit
  in Shenzhen, GTA VI going on sale worldwide, Anthropic's $81.3bn IPO
  (the largest ever), the ICJ judgment on Myanmar and the Rohingya, COP31's
  final stretch, Cyclone Akvan's Odisha evacuations, APEC in Shenzhen,
  Colombia's national strike, the Florida floods, Korea's Suneung exam,
  Australia's unemployment at a five-year high, the India–Japan 2+2
  dialogue, and Indonesia's asset-forfeiture law.
- **25 one-line briefs** — the rest of the day, from Tokyo's AI-stock slide
  to the Las Vegas Grand Prix.
- **The Day in Numbers** — $81.3bn, 551,864, 47,000+, 96%, $62,000, 4.9%,
  2.8bn.
- **Where It Happened** — a world map with numbered pins for the 13 cards
  and a gold star for the Strait of Hormuz energy story.
- **Date Check** — near-miss stories deliberately excluded, with their true
  dates: Voyager 1's one-light-day crossing, the Iran/Gulf drone strikes,
  the EU's €45bn Ukraine loan, the Kerch Bridge strike, Peltola's Alaska
  win, Nvidia's quarter, the Van Gogh sale, and more — all first reported
  on 17 or 18 November, not the 19th.

## Date discipline

Every story was verified by first-report time (wire timestamp, call time,
or release time), never by publication date. Three stories that looked like
19 November news turned out to be 18 November releases — South Africa's
5.2% October inflation, Morocco's climb to fifth in the FIFA rankings, and
Belgium's confirmation of ten F-16s for Ukraine — and were left out. The
ICJ judgment is reported without an outcome: the judgment was read at
10:00 CET, after this page was drawn. The Akvan evacuation figure is
47,000+ (Reuters), not the 200,000 quoted in some entries.

## How to run

```sh
python3 main.py
```

Requires Python 3.13 and Pillow. The program writes `entry.png`
(1024×1024, under 1 MiB) to `$MAKEFUN_OUTPUT_DIR`, or `/output` if the
variable is unset. It uses no network, no randomness, and no clock, so
running it twice produces byte-identical output.

## Sources

Reuters, AP, AFP, Al Jazeera, Bloomberg.
