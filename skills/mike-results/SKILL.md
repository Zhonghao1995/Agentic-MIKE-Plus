---
name: mike-results
description: Read MIKE+ .res1d results via the mike-plus MCP server — list contents, summarize peaks, or extract a single time series. Use when an agent needs to inspect or pull numbers from MIKE+ network results (node water levels, link/reach discharge, velocities). No MIKE+ license or installation required.
---

# MIKE+ Results

Reads MIKE+ `.res1d` result files (via mikeio1d). **No license / no MIKE+ install needed** — fully portable.

## When to use
To find out what is in a result file, get peak values, or extract a series for analysis/plotting. Use after `mike_run`, or on any existing `.res1d`.

## Tools
- **`mike_results_list`** — `{res1d}` → quantities, element counts + sample ids (nodes/reaches/structures/catchments), time range. Start here to discover valid `quantity`/`element` values.
- **`mike_results_summary`** — `{res1d, quantities?}` → per-quantity peak (value, element, chainage, time), in the canonical schema.
- **`mike_results_read`** — `{res1d, quantity, element, max_points?}` → a single downsampled time series (`times`, `values`, `unit`).

## Conventions
- Column identity is `Quantity:ElementId[:chainage]` (e.g. `Discharge:Link_29:33.5333`). `element` matches the id prefix.
- Output follows the canonical, engine-agnostic schema (`{engine, quantity, element_id, chainage, unit, ...}`) so the same downstream skills work for SWMM/LSTM later. (`mike_results_summary` reports the peak's element as `peak_element` — same idea, named for the peak.)
- **Global-max caveat:** `mike_results_summary` returns the max over the WHOLE run, which can land in the warm-up / initial-condition period (e.g. a base-flow value near t=0), not the storm peak. Always check `peak_time`; when you want the event peak, pass `skip_hours` (e.g. `skip_hours: 6`) to drop the initial window.
- Report only what the file contains; if a `quantity`/`element` has no series, say so (the tool errors with a clear message) rather than guessing.

## Orchestration
```
mike_results_list     -> learn quantities + element ids
mike_results_summary  -> peaks for a quick read
mike_results_read     -> a series for a specific element  -> mike-plot
```
