"""Plotting tools (house style: Arial 12, ticks inward, SI, no title). No license."""
from .._types import ToolDef
from ..runtime.worker import call_worker


def get_tools():
    return [
        ToolDef(
            name="mike_plot_rain_flow",
            description=(
                "Render a stacked two-panel rainfall-runoff figure (rain inverted on top, flow "
                "on bottom) in the house style. Flow comes from a .res1d element; rainfall "
                "optional from a .dfs0. No license needed."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "res1d": {"type": "string"},
                    "element": {"type": "string", "description": "Reach/link or node id for the flow series."},
                    "quantity": {"type": "string", "description": "Flow quantity (default 'Discharge')."},
                    "rain_dfs0": {"type": "string", "description": "Optional rainfall .dfs0 for the top panel."},
                    "out_png": {"type": "string", "description": "Output PNG path."},
                },
                "required": ["res1d", "element", "out_png"],
            },
            handler=lambda a: call_worker(
                "plot_worker",
                {
                    "action": "rain_flow",
                    "res1d": a["res1d"],
                    "element": a["element"],
                    "quantity": a.get("quantity", "Discharge"),
                    "rain_dfs0": a.get("rain_dfs0"),
                    "out_png": a["out_png"],
                },
                timeout=600,
            ),
        ),
        ToolDef(
            name="mike_plot_timeseries",
            description=(
                "Render a single-panel time-series plot (a quantity at an element) in the house "
                "style. No license needed."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "res1d": {"type": "string"},
                    "quantity": {"type": "string"},
                    "element": {"type": "string"},
                    "out_png": {"type": "string"},
                },
                "required": ["res1d", "quantity", "element", "out_png"],
            },
            handler=lambda a: call_worker(
                "plot_worker",
                {
                    "action": "timeseries",
                    "res1d": a["res1d"],
                    "quantity": a["quantity"],
                    "element": a["element"],
                    "out_png": a["out_png"],
                },
                timeout=600,
            ),
        ),
        ToolDef(
            name="mike_plot_network",
            description=(
                "Render a network layout map of a MIKE+ model from a .res1d — reaches/pipes as "
                "lines, nodes as points, equal-aspect, house style. Good for an overview figure. "
                "No license needed."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "res1d": {"type": "string"},
                    "out_png": {"type": "string"},
                },
                "required": ["res1d", "out_png"],
            },
            handler=lambda a: call_worker(
                "plot_worker",
                {"action": "network", "res1d": a["res1d"], "out_png": a["out_png"]},
                timeout=600,
            ),
        ),
    ]
