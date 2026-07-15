---
name: dashboard-design
description: Use when changing the observatory dashboard's look — charts, theme.scss, page layout, new sections (chart, color, spacing, tooltip, table view). The design system's decisions and their rationale, so changes extend the language instead of fighting it.
---

# Observatory design language

Read the global `dataviz` skill before any chart work. This file adds what is
specific to this page.

## Identity

- **Ink is the signature.** Accent `#1a1a19` appears sparingly — the emphasized
  series, the lit dotgrid squares, rules. Restraint IS the identity; a colorful
  addition breaks the page.
- **Emphasis, not categorical**: one series in accent, the rest `BAR_GRAY`.
  Verdicts use an ordered one-hue ink ramp (darker = more restricted).
- The palette in `theme.py` is already validated — reuse it. A genuinely new
  color requires running the dataviz skill's validator first.
- Editorial, finding-first structure: claim → chart as proof → method last.
  The mission line under the kicker answers "what is this site?" above the
  fold; don't add explanatory preambles elsewhere.

## Conventions

- Chart builders live in `dashboard/charts.py`, one function per chart,
  wrapped in `theme.themed(...)`. Table builders sit next to them, sharing
  aggregation helpers (see `_block_agg`) — chart and table must show the same
  numbers.
- Every chart ships a Chart | Table tabset (accessibility) and tooltips with
  the counts behind any percentage. Tabset chrome is quieted in `theme.scss`
  (no content box, hairline only).
- Filters render as dropdown rows ABOVE the chart (`.vega-bindings` CSS).
- Sector slugs → reader-facing names via `charts.SECTOR_LABELS`.

## Spacing rhythm (hard-won values)

- Sections: `margin-top: 4.75rem + padding-top: 3rem` on `section.level2`
  (spacing on the wrapper, not the h2 — margin-collapse trap).
- The FIRST section break is `2.4rem` instead: it follows the dateline, which
  already spaces it from the hero chart.
- `.cell` rhythm is `2.4rem`; inside tabsets the tabset wrapper takes it over.
- The dateline is sticky (docks at top, hairline via `.is-stuck` set by a
  sentinel IntersectionObserver in `index.qmd`).

## Traps

- **Prose figures in `index.qmd` are hardcoded** and go stale on each new
  snapshot — see the `snapshot` skill for the list.
- Charts read the parquet already filtered to the latest snapshot (done at
  load in `index.qmd`); never aggregate across snapshots in a chart.
- Scroll animations must keep gating on `prefers-reduced-motion`.
