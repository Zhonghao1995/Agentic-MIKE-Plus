# Agentic MIKE+

**A headless, natural-language-driven, automated modelling workflow for MIKE+.**
State a goal in plain language; an agent inspects the model, changes parameters, runs simulations, reads results, and plots — end to end, without ever opening the MIKE+ GUI.

<p>
  <a href="https://github.com/Zhonghao1995/Agentic-MIKE-Plus/actions/workflows/ci.yml"><img src="https://github.com/Zhonghao1995/Agentic-MIKE-Plus/actions/workflows/ci.yml/badge.svg" alt="CI" /></a>
  <img src="https://img.shields.io/badge/python-3.11_x64-3776AB" alt="Python 3.11 x64" />
  <img src="https://img.shields.io/badge/MIKE%2B-2026-0a7d8c" alt="MIKE+ 2026" />
  <img src="https://img.shields.io/badge/MCP-1.28-7C3AED" alt="MCP 1.28" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT license" />
  <img src="https://img.shields.io/badge/status-experimental-orange" alt="experimental" />
</p>

> Experimental / pre-release. One MCP server + skills wrapping DHI's Python stack (`mikeplus` / `mikeio` / `mikeio1d`). Verified end to end on the MIKE+ 2026 `Sirius_RTC` example. Sibling of [agentic-swmm-workflow](https://github.com/Zhonghao1995/agentic-swmm-workflow).

## Install: just tell your agent

It is the AI era — you don't wire this up by hand. Paste this to your AI coding agent (Claude Code, Codex, …):

```text
Set up Agentic MIKE+ for me — an MCP server + skills that drive MIKE+ headless.

1. Clone https://github.com/Zhonghao1995/Agentic-MIKE-Plus and read its README.
2. Make a Python 3.11 (x64) venv in the repo and install it:
   pip install -r requirements.lock   then   pip install -e .
3. Register the MCP server with me (Claude Code):
   claude mcp add mike-plus -- "<repo>/.venv/Scripts/python.exe" -m mikeplus_mcp.server
4. Copy the skills/mike-* folders into ~/.claude/skills/ so you know how to drive the tools.
5. Run scripts/smoke_test.py to confirm the 10 tools load.
6. Tell me what's available and which tools need a MIKE+ license
   (running or editing a model does; reading results and plotting do not).
```

On Windows the agent can do steps 2–5 in one shot: after cloning, `powershell -ExecutionPolicy Bypass -File scripts\install.ps1`.

Needs **Python 3.11 (x64)**; *run/edit* also needs a licensed **MIKE+ 2026**. Exact versions are pinned in [`requirements.lock`](requirements.lock); other MCP clients can use `config/mcp.sample.json`.

## Why it matters

- **Natural-language-driven.** Describe the task in plain words; the agent plans and runs it — no scripting, no GUI clicking. (A sub-agent did this autonomously.)
- **Fully headless.** Runs with no GUI — on a workstation, a server, in CI, or under an agent. Built for batch and scenario automation.
- **MCP-native and portable.** One server speaks the Model Context Protocol; connect Claude Desktop or Codex with a single config line, and install with pip.
- **Low barrier to share.** Reading results and plotting need no MIKE+ license — only running or editing does. Teammates analyse model output with nothing but `pip install`.
- **Reproducible.** Deterministic tools, structured-JSON output, a pinned lockfile, verified on a real model — not a chat-to-model black box.
- **Engine-agnostic and extensible.** Results use a common schema (ready to sit beside SWMM and LSTM); add a tool or skill by dropping in a file.

<p align="center">
  <img src="docs/figs/overview.png" alt="Agentic MIKE+ overview — agentic-workflow advantages, core functionality and tools, and which capabilities need a MIKE+ license" width="900" />
</p>

## How it works

Skills (markdown playbooks) tell the agent *when and how*; the agent calls **MCP tools**; each tool runs in an isolated **worker subprocess** that imports only `mikeplus` *or* `mikeio*` — the two cannot share a process. The server itself imports neither.

```
agent  ->  reads skills/*.md  ->  calls MCP tools  ->  workers (mikeplus / mikeio1d)
```

<p align="center">
  <img src="docs/figs/workflow.png" alt="From one plain-language sentence to a finished MIKE+ run, automatically and without the GUI" width="900" />
</p>

## Tools (one server, `mike-plus`)

| Tool | Does | License |
|---|---|---|
| `mike_model_info` | model overview: simulations, scenarios, element counts | yes |
| `mike_get_values` / `mike_set_values` | read / change parameters (e.g. pipe diameter) | yes |
| `mike_run` | run a simulation headless, return `.res1d` | yes |
| `mike_results_list` / `summary` / `read` | list contents / peaks / one time series | no |
| `mike_plot_rain_flow` / `timeseries` / `network` | stacked hydrograph / series / network map | no |

Five skills (`mike-model`, `mike-params`, `mike-runner`, `mike-results`, `mike-plot`) orchestrate them.

## Demo — `Sirius_RTC` (MIKE 1D, 568 nodes, 576 links)

<p align="center">
  <img src="docs/figs/sirius_rtc_network.png" alt="Sirius_RTC network layout" width="900" />
</p>
<p align="center">
  <img src="docs/figs/sirius_rtc_rain_flow.png" alt="Rainfall-runoff hydrograph for the busiest pipe" width="900" />
</p>

Full evidence — commands, outputs, and the honest license boundary — is in **[docs/verification.md](docs/verification.md)**.

## License

MIT © 2026 Zhonghao Zhang, University of Victoria. Built on DHI's `mikeplus` / `mikeio` / `mikeio1d` and the Model Context Protocol. MIKE+ is a product of DHI; running models requires a valid DHI license.
