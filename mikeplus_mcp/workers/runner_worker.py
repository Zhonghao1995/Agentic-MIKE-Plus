"""Run a MIKE+ model headless. Imports mikeplus ONLY.

stdin payload: {sqlite, simulation?, timeout_s, work_on_copy, __out}
result: {ok, active_simulation, result_files[], elapsed_s, qa{completed, errors, warnings, issues, status, log_file}}
"""
import json
import shutil
import sys
import tempfile
import time
from pathlib import Path


def main() -> None:
    payload = json.load(sys.stdin)
    out = payload["__out"]
    sqlite = payload["sqlite"]
    simulation = payload.get("simulation")
    timeout_s = payload.get("timeout_s", 1800)
    work_on_copy = payload.get("work_on_copy", False)

    run_dir = Path(sqlite).parent
    if work_on_copy:
        tmp_dir = Path(tempfile.mkdtemp(prefix="mike_run_copy_"))
        shutil.copytree(run_dir, tmp_dir / Path(sqlite).name, dirs_exist_ok=False)
        run_dir = tmp_dir / Path(sqlite).name
        sqlite_path = run_dir / Path(sqlite).name
    else:
        sqlite_path = Path(sqlite)

    try:
        import mikeplus as mp

        start = time.time()
        with mp.open(str(sqlite_path)) as db:
            if simulation:
                db.set_simulation(simulation)
            db.run()
        elapsed_s = round(time.time() - start, 2)

        result_files = [str(p) for p in run_dir.glob("*.res1d")]

        try:
            from mikeplus_mcp.runtime.engine_log import read_run_log
            qa = read_run_log(run_dir)
        except Exception:
            qa = {"completed": None, "errors": None, "warnings": None, "issues": None, "status": "unknown", "log_file": None}

        result = {
            "ok": True,
            "active_simulation": simulation or str(db.active_simulation),
            "result_files": result_files,
            "elapsed_s": elapsed_s,
            "work_on_copy": work_on_copy,
            "copy_path": str(run_dir) if work_on_copy else None,
            "qa": qa,
        }
    except Exception as exc:
        result = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}
    finally:
        if work_on_copy and "tmp_dir" in locals():
            try:
                shutil.rmtree(tmp_dir, ignore_errors=True)
            except OSError:
                pass

    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, default=str)
    sys.exit(0 if result.get("ok") else 1)


main()
