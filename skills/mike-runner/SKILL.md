---
name: mike-runner
description: Run MIKE+ simulations headless via the mike-plus MCP server and report result files + engine status. Use when an agent must execute a MIKE+ .sqlite model's active (or a named) simulation without opening the MIKE+ GUI, then hand the .res1d outputs to reading/plotting. Requires MIKE+ installed + a valid license. Always run on a copy.
---

# MIKE+ Runner

Executes a MIKE+ model headless through the `mike-plus` MCP server (engine: MIKE 1D).

## When to use
After a model is ready and you need to actually run it — the active simulation, or a named setup from `msm_Project`. Do **not** use this to read results (that's `mike-results`) or to plot (`mike-plot`).

## Tool
- **`mike_run`** — args: `sqlite` (path), `simulation` (optional setup id), `timeout_s` (optional). Returns `{ok, active_simulation, result_files[], elapsed_s}` plus `_log_tail` (engine console).

## Conventions (evidence boundaries)
- **License + install required.** `mike_run` loads the local MIKE 1D engine; it fails on a machine without MIKE+ + a valid license. (Reading/plotting do not.)
- **Always run on a COPY.** mikeplus has no undo — copy the model folder first and run the copy, never the user's original.
- **Gate on failure.** Treat the run as failed if `ok` is false. The engine prints `WARNING` and `N error(s)` per Load/Validate/Initialize/Prepare/Run phase to `_log_tail`; surface errors, don't bury them.
- Do not fabricate metrics. Pass the returned `result_files` to `mike-results` / `mike-plot`.

## Orchestration
```
mike_model_info  -> confirm the active simulation / pick one
mike_run         -> result_files (.res1d)
        -> mike-results (summary / read)  -> mike-plot
```
