---
name: mike-params
description: Read and modify MIKE+ model parameters via the mike-plus MCP server — inspect or change values in any model table (pipe Diameter/Manning in msm_Link, node levels in msm_Node, catchment properties in msm_Catchment, etc.). Use when an agent must identify a current parameter and change it before re-running. Requires MIKE+ + license; mutating tools must run on a copy.
---

# MIKE+ Parameters

Reads and edits values in the MIKE+ model database tables (via mikeplus). This is the "edit the model" capability that sits between `mike-model` (overview) and `mike-runner` (execute).

## Tools
- **`mike_get_values`** — `{sqlite, table, columns?, muids?}` → current values. Read-only. Use to **identify** a parameter before changing it.
- **`mike_set_values`** — `{sqlite, table, values, muids | all}` → applies the change and returns **before/after** for the affected rows. **Mutates** the database.

## Common tables / columns
- `msm_Link` — pipes/reaches: `Diameter`, `Width`, `Height`, `Manning` (Manning's M; higher = smoother), `MaterialID`, `TypeNo`.
- `msm_Node` — manholes/nodes: `GroundLevel`, `InvertLevel`, `Diameter`.
- `msm_Catchment` — catchments: area / imperviousness / runoff parameters.
- `msm_Project` — simulation setups (used by `mike_run`'s `simulation`).

## Conventions (safety)
- **Always operate on a COPY** — `mike_set_values` writes to the database and mikeplus has no undo.
- **Scope every edit.** Pass `muids` to target specific elements; only set `all=true` when you truly mean every row.
- Confirm with the returned `before`/`after` (or a follow-up `mike_get_values`) before re-running.
- After editing, re-run with `mike_run` and compare results to quantify the effect.

## Orchestration (identify -> change -> re-run -> compare)
```
mike_model_info / mike_get_values   -> identify current parameter
mike_set_values                     -> change it (on a copy)  -> before/after
mike_run                            -> new .res1d
mike_results_summary / read         -> compare against baseline
```
