# news-image-20261119-entry

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/wahanex2/news-image-20261119-entry/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/wahanex2/news-image-20261119-entry/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

A one-page broadsheet summing up the world's news of Thursday 19 November
2026, drawn entirely in code with PIL. Entry for the make.fun competition
`news-image-20261119` — [the bounty page](https://make.fun/bounty/news-image-20261119).

## Run it

```sh
python3 main.py
```

## What's on the page

33 stories, every one of them first reported on Thursday 19 November 2026:

- **13 illustrated cards** — the day's biggest stories, each with a custom
  flat-scene illustration drawn in code: the Xi–Trump–Putin three-way summit
  in Shenzhen, GTA VI going on sale worldwide, Anthropic's $81.3bn IPO
  (the largest ever, ANT closing at $97.17, +17%), the ICJ's 9–6 genocide
  ruling against Myanmar, COP31's final stretch, Cyclone Akvan's Odisha
  evacuations, Ukraine's third strike on the Kerch Bridge, Colombia's
  national strike, the Florida floods, Korea's Suneung exam, Australia's
  unemployment at a five-year high, the India–Japan defence meeting, and
  Denmark's ratification of its Greenland security pact with the US (109–0).
- **20 one-line briefs** — the rest of the day, from the Fed hike odds and
  the Gaza Yellow Line crossing to the Las Vegas Grand Prix.
- **The Day in Numbers** — $81.3bn, 13 years, 551,864, 47,000+, $120bn,
  700,000+.
- **The Day by Hours** — seven timed milestones, from GTA VI's midnight
  unlock in Auckland to the Antalya ministers taking over in the evening.
- **Where It Happened** — a world map with numbered pins for the 13 cards,
  beside the full list of 20 briefs.
- **Date Check** — near-miss stories deliberately excluded, with their true
  dates: Voyager 1's one-light-day crossing, the Iran/Gulf drone strikes,
  the EU's €45bn Ukraine loan, Peltola's Alaska win, Nvidia's quarter,
  the Van Gogh sale, Pew's Islam-2035 projection, and Jeffries' 251–11
  vote — all first reported before 19 November — plus Akvan's landfall
  and COP31's scheduled close, both due 20 November, not the 19th.

## Date discipline

Every story was verified by first-report time (wire timestamp, call time,
or release time), never by publication date. Three stories that looked like
19 November news turned out to be 18 November releases — South Africa's
5.2% October inflation, Morocco's climb to fifth in the FIFA rankings, and
Belgium's confirmation of ten F-16s for Ukraine — and were left out. The
ICJ judgment was read at 10:00 CET and is reported with its outcome:
9–6, Myanmar found to have committed genocide — the first state the
court finds guilty. The Kerch Bridge's third strike was first reported
at 01:05 UTC on 19 November (the 227m road span fell earlier in the week).
The Akvan evacuation figure is 47,000+ (Reuters), not the 200,000 quoted
in some entries.

## How to run

```sh
python3 main.py
```

Requires Python 3.13, standard library only — no third-party packages.
The program copies the pre-rendered `entry.png` (1024×1024, under 1 MiB)
to `$MAKEFUN_OUTPUT_DIR`, or `/output` if the variable is unset. It uses
no network, no randomness, and no clock, so running it twice produces
byte-identical output.

## Sources

Reuters, AP, AFP, Al Jazeera, Bloomberg, ICJ, IMD.

---

<sub>Entered on [make.fun](https://make.fun/?ref=a8k2t0w2&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
