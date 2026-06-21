# Verification evidence

End-to-end evidence that the tools, skills, and the natural-language-driven loop
actually work, gathered on a real MIKE+ model. Reproduce with the pinned
environment (`requirements.lock`, Python 3.11 x64).

## Environment (pinned)

| Component | Version |
| --- | --- |
| Python | 3.11.9 (x64) |
| mcp | 1.28.0 |
| mikeplus | 2026.0.0 |
| mikeio | 3.1.0 |
| mikeio1d | 1.2.1 |
| pythonnet | 3.1.0 |
| pandas / numpy | 3.0.3 / 2.4.6 |
| matplotlib / shapely / scipy | 3.11.0 / 2.1.2 / 1.17.1 |
| MIKE+ (for run/edit only) | 2026 + valid DHI license |

## Tool discovery + smoke test

`python scripts/smoke_test.py` discovers all 10 tools and runs a live,
license-free read:

```
discovered tools: mike_get_values, mike_model_info, mike_plot_network,
  mike_plot_rain_flow, mike_plot_timeseries, mike_results_list,
  mike_results_read, mike_results_summary, mike_run, mike_set_values
mike_results_list OK on Rainfall_CDS_1yearHDBaseDefault_Network_HD.res1d:
  quantities=['WaterLevel','Discharge','FlowVelocity','ControlStrategyId',
  'CrestLevel','DischargeInStructure','GateLevel']
SMOKE OK
```

The whole MCP server was also exercised over the real stdio transport
(`initialize` -> `list_tools` -> `call_tool`), returning the same results.

## End-to-end on the Sirius_RTC example

Sirius_RTC is a collection-system (MIKE 1D) model bundled with MIKE+:
**568 nodes, 576 links, 863 catchments**, with real-time-control rules and a
1-year CDS design storm. (Model files are DHI's and are not redistributed here —
see [examples/sirius_rtc](../examples/sirius_rtc/README.md).)

- **Inspect** — `mike_model_info`: active simulation `Rainfall_CDS_1yearHD`,
  scenario `Base`, model `CS_MIKE1D`, units `MU_CS_SI`.
- **Run (headless)** — `mike_run`: the MIKE 1D engine ran in ~44-59 s and
  returned a fresh `.res1d`. No GUI was opened.
- **Read results** — `mike_results_summary`:
  - WaterLevel peak **23.5221 m** at node `C14154801` (t = 19:31).
  - Discharge peak **0.7989 m3/s** at reach `Link_29` (t = 00:05, warm-up).
    With `skip_hours=6` the storm peak is **0.7852 m3/s** at `Link_29` (t = 12:34) —
    the option added after the sub-agent flagged the warm-up artifact (below).
- **Edit a parameter** — `mike_get_values` read `Diameter = 0.8 m` on reach
  `C14154801.2`; `mike_set_values` changed it to `0.2 m` and the change was
  **verified to persist** by read-back (the tool errors loudly if an edit does
  not take effect).

### Network layout and a rainfall-runoff hydrograph

Produced by `mike_plot_network` and `mike_plot_rain_flow` (license-free), in the
house style (Arial 12, ticks inward, SI units, no title):

<p align="center">
  <img src="figs/sirius_rtc_network.png" alt="Sirius_RTC network layout" width="430" />
  <img src="figs/sirius_rtc_rain_flow.png" alt="Rainfall-runoff hydrograph for the busiest pipe" width="430" />
</p>

## Natural-language-driven validation

A general-purpose sub-agent was given only the tools, the `mike-results` and
`mike-plot` skills, and one sentence — *"tell me where the network is most
hydraulically stressed and plot the worst pipe."* With no hardcoded element ids,
it autonomously ran:

```
mike_results_list -> mike_results_summary -> mike_results_read -> mike_plot_rain_flow
```

found the worst reach (`Link_29`, 0.799 m3/s) and worst node (`C14154801`,
23.52 m), and produced the figure. It also reported a genuine issue — the global
discharge peak fell in the warm-up window (t = 00:05) rather than the storm — which
was folded back into `mike_results_summary` as the `skip_hours` option. This is
the build -> run -> critique -> improve loop working end to end.

## License boundary (honest)

`mike_run` and the parameter edits each work individually, but the local MIKE+
license is **single-seat / floating**: the engine feature is contended with the
GUI and effectively rate-limited (about one engine checkout before it needs to
recover). A back-to-back baseline+scenario run on a single seat is therefore not
reliable, so multi-run workflows (calibration, uncertainty) need a multi-seat or
dedicated engine/SDK license. Reading results and plotting need no license at
all. This is an environment/licensing constraint, not a limitation of the code.

## Reproduce

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.lock
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe scripts\smoke_test.py
# then point the mike_* tools at a MIKE+ model (a working copy of Sirius_RTC, etc.)
```
