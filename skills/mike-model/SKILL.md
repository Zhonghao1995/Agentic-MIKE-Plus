---
name: mike-model
description: Inspect a MIKE+ .sqlite model via the mike-plus MCP server — active simulation/scenario/model, unit system, the list of simulation setups and scenarios, and element counts. Use when an agent needs to understand a MIKE+ model before running or editing it. Requires MIKE+ installed + a license.
---

# MIKE+ Model

Opens a MIKE+ `.sqlite` and reports its high-level structure (via mikeplus).

## When to use
First step on any unfamiliar model: find the active simulation (what `mike_run` would run), the available simulation setups and scenarios, and the network size. Read-only.

## Tool
- **`mike_model_info`** — `{sqlite}` → `{active_simulation, active_scenario, active_model, unit_system, simulations[], scenarios[], counts{nodes,links,catchments}}`.

## Conventions
- Requires MIKE+ + license (it opens the model through mikeplus).
- Read-only, but still prefer a copy when a run/edit will follow.
- The `simulations` list are `msm_Project` setup ids — pass one as `mike_run`'s `simulation` to run a non-active setup.

## Orchestration
```
mike_model_info  -> choose simulation  -> mike_run  -> mike-results / mike-plot
```
