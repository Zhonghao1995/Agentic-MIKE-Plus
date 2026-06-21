"""Run a MIKE+ simulation headless. Imports mikeplus ONLY (needs a MIKE+ license).

stdin payload: {sqlite, simulation?, __out}
result (to __out): {ok, sqlite, active_simulation, result_files, elapsed_s}
The MIKE 1D engine log goes to stdout and is captured by the caller as _log_tail.
"""
import json
import sys
import time


def main() -> None:
    payload = json.load(sys.stdin)
    out = payload["__out"]
    try:
        import mikeplus as mp

        sqlite = payload["sqlite"]
        sim = payload.get("simulation")
        t0 = time.time()
        with mp.open(sqlite) as db:
            if sim:
                try:
                    db.active_simulation = sim
                except Exception as exc:  # best-effort; fall back to active sim
                    print(f"[run] could not set active_simulation={sim!r}: {exc}", file=sys.stderr)
            active = str(db.active_simulation)
            files = db.run()
        result = {
            "ok": True,
            "sqlite": sqlite,
            "active_simulation": active,
            "result_files": [str(f) for f in (files or [])],
            "elapsed_s": round(time.time() - t0, 1),
        }
    except Exception as exc:
        result = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, default=str)
    sys.exit(0 if result.get("ok") else 1)


main()
