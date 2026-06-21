"""Read MIKE+ res1d results. Imports mikeio1d ONLY (+ pure contracts). No license.

stdin payload: {action: list|summary|read, res1d, ...}
"""
import json
import sys


def _ids(coll, n=25):
    """Best-effort (count, sample-ids) for a mikeio1d collection; never raises."""
    count = None
    try:
        count = int(len(coll))
    except Exception:
        pass
    sample = []
    try:
        names = getattr(coll, "names", None)
        if names is not None:
            sample = [str(x) for x in list(names)[:n]]
        else:
            for i, item in enumerate(coll):
                if i >= n:
                    break
                sample.append(str(getattr(item, "id", getattr(item, "name", item))))
    except Exception:
        sample = []
    return {"count": count, "sample": sample}


def main() -> None:
    payload = json.load(sys.stdin)
    out = payload["__out"]
    try:
        import mikeio1d
        from mikeplus_mcp.contracts import schema
        from mikeplus_mcp.contracts.units import unit_for

        action = payload.get("action", "list")
        res = mikeio1d.open(payload["res1d"])

        if action == "list":
            ti = res.time_index
            result = {
                "ok": True,
                "res1d": payload["res1d"],
                "quantities": list(res.quantities),
                "nodes": _ids(res.nodes),
                "reaches": _ids(res.reaches),
                "structures": _ids(res.structures),
                "catchments": _ids(res.catchments),
                "time": {
                    "start": str(res.start_time),
                    "end": str(res.end_time),
                    "n_steps": int(len(ti)),
                },
            }

        elif action == "summary":
            df = res.read()
            skip_hours = payload.get("skip_hours") or 0
            if skip_hours:
                import pandas as pd
                cutoff = df.index[0] + pd.Timedelta(hours=float(skip_hours))
                df = df.loc[df.index >= cutoff]
            result = {
                "ok": True,
                "res1d": payload["res1d"],
                "skip_hours": skip_hours,
                "summary": schema.summarize(df, payload.get("quantities")),
            }

        elif action == "read":
            quantity = payload["quantity"]
            element = payload["element"]
            df = res.read()
            base = f"{quantity}:{element}"
            # exact (node, no chainage) OR 'base:' prefix (reach w/ chainage); avoids
            # matching reach 'C14154801.2' when the node 'C14154801' was requested
            cols = [c for c in df.columns if str(c) == base or str(c).startswith(base + ":")]
            if not cols:
                raise ValueError(f"no series for quantity={quantity!r} element={element!r}")
            col = cols[0]
            s = df[col]
            max_pts = int(payload.get("max_points", 5000))
            step = max(1, len(s) // max_pts)
            s = s.iloc[::step]
            meta = schema.parse_column(col)
            result = {
                "ok": True,
                "res1d": payload["res1d"],
                "column": str(col),
                "quantity": quantity,
                "element_id": meta["element_id"],
                "chainage": meta["chainage"],
                "unit": unit_for(quantity),
                "n_points": int(len(s)),
                "times": [str(t) for t in s.index],
                "values": [float(v) for v in s.values],
            }
        else:
            raise ValueError(f"unknown action: {action!r}")
    except Exception as exc:
        result = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, default=str)
    sys.exit(0 if result.get("ok") else 1)


main()
