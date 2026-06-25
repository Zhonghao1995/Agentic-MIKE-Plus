---
name: mike-plot
version: 0.1.0
description: Produce publication-style figures from MIKE+ .res1d results via the mike-plus MCP server — a stacked rainfall-runoff hydrograph or a single time series, in the house style (Arial 12, ticks inward, SI units, no title). Use when an agent must render MIKE+ results as a PNG without opening the GUI. No license required.
---

# MIKE+ Plot

Renders MIKE+ results in the project house style. **No license / no MIKE+ install needed.**

## House style (do not change without being asked)
Arial 12 · ticks inward (`direction='in'`, both axes) · SI units · **no title** · inverted hyetograph · dpi 300. Rain `#4C78A8`, flow `#F58518`. Style lives in `mikeplus_mcp/contracts/plot_style.py` and is shared with the SWMM figures layer.

## Tools
- **`mike_plot_rain_flow`** — `{res1d, element, quantity?='Discharge', rain_dfs0?, out_png}` → stacked two-panel figure: **rainfall inverted on top, flow on the bottom**, shared time axis. `rain_dfs0` is optional (a `.dfs0`); without it only the flow panel is drawn.
- **`mike_plot_timeseries`** — `{res1d, quantity, element, out_png}` → single-panel series.
- **`mike_plot_network`** — `{res1d, out_png}` → network layout map (reaches as lines, nodes as points, equal aspect). Use for an overview / location figure of the whole model.

## Conventions
- Discover valid `element`/`quantity` with `mike_results_list` first; don't guess ids.
- Do not claim a figure exists unless the tool returned `{ok:true, png:...}` and the file was written.
- Keep units SI and the style fixed; expose only data choices (which element/quantity, which rainfall file) to the user.

## Orchestration
```
mike_results_list  -> pick element + quantity
mike_plot_rain_flow (or mike_plot_timeseries) -> out_png
```
