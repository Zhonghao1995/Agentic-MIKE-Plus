"""Model run tool."""
from .._types import ToolDef
from ..runtime.worker import call_worker


def get_tools():
    return [
        ToolDef(
            name="mike_run",
            description=(
                "Run a MIKE+ simulation headless. Requires MIKE+ + license. "
                "By default runs on the provided sqlite path. Set work_on_copy=true to "
                "run on a scratch copy to protect the original model."
            ),
            input_schema={
                "type": "object",
                "properties": {
                    "sqlite": {"type": "string", "description": "Path to the MIKE+ .sqlite model database."},
                    "simulation": {"type": "string", "description": "Optional simulation setup id (msm_Project) to run. Defaults to active."},
                    "timeout_s": {"type": "integer", "description": "Optional timeout in seconds."},
                    "work_on_copy": {"type": "boolean", "description": "If true, copies the whole model folder to a scratch location and runs the copy, leaving the original untouched."},
                },
                "required": ["sqlite"],
            },
            handler=lambda a: call_worker(
                "runner_worker",
                {
                    "sqlite": a["sqlite"],
                    "simulation": a.get("simulation"),
                    "timeout_s": a.get("timeout_s", 1800),
                    "work_on_copy": a.get("work_on_copy", False),
                },
                timeout=a.get("timeout_s", 1800) + 60,
            ),
        )
    ]
