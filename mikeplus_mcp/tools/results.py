"""Result-reading tools (no license needed)."""
from .._types import ToolDef
from ..runtime.worker import call_worker


def get_tools():
    return [
        ToolDef(
            name="mike_results_list",
            description=(
                "List what is inside a MIKE+ .res1d: quantities (WaterLevel/Discharge/...), "
                "element counts (nodes/reaches/structures/catchments) with sample ids, and the "
                "time range. No license needed."
            ),
            input_schema={
                "type": "object",
                "properties": {"res1d": {"type": "string", "description": "Path to a .res1d file."}},
                "required": ["res1d"],
            },
            handler=lambda a: call_worker("results_worker", {"action": "list", "res1d": a["res1d"]}, timeout=300),
        ),
        ToolDef(
            name="mike_results_summary",
            description=(
                "Per-quantity peak summary (peak value, element, chainage, time) from a MIKE+ "
                ".res1d. No license needed. NOTE: this is the GLOBAL max over the whole run, which "
                "can fall in the warm-up/initial-condition period (a base-flow value near t=0) "
                "rather than the storm peak — pass skip_hours to exclude an initial window and "
                "always check peak_time."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "res1d": {"type": "string"},
                    "quantities": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Optional subset, e.g. ['Discharge','WaterLevel'].",
                    },
                    "skip_hours": {
                        "type": "number",
                        "description": "Exclude the first N hours (warm-up) before finding peaks.",
                    },
                },
                "required": ["res1d"],
            },
            handler=lambda a: call_worker(
                "results_worker",
                {"action": "summary", "res1d": a["res1d"],
                 "quantities": a.get("quantities"), "skip_hours": a.get("skip_hours")},
                timeout=600,
            ),
        ),
        ToolDef(
            name="mike_results_read",
            description=(
                "Extract one time series (a quantity at an element) from a MIKE+ .res1d as "
                "times+values (downsampled to max_points). No license needed."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "res1d": {"type": "string"},
                    "quantity": {"type": "string", "description": "e.g. 'Discharge' or 'WaterLevel'."},
                    "element": {"type": "string", "description": "Element id (node id, or reach/link id, optionally with chainage)."},
                    "max_points": {"type": "integer", "description": "Cap on returned points (default 5000)."},
                },
                "required": ["res1d", "quantity", "element"],
            },
            handler=lambda a: call_worker(
                "results_worker",
                {
                    "action": "read",
                    "res1d": a["res1d"],
                    "quantity": a["quantity"],
                    "element": a["element"],
                    "max_points": a.get("max_points", 5000),
                },
                timeout=600,
            ),
        ),
    ]
