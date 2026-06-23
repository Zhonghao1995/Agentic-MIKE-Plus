"""Render MIKE+ result plots in the house style.

Imports mikeio1d / mikeio / matplotlib (NOT mikeplus). No license needed.
Actions: rain_flow | timeseries | network
"""
import json
import sys


def main() -> None:
    payload = json.load(sys.stdin)
    out = payload["__out"]
    try:
        import mikeio1d
        from mikeplus_mcp.contracts import plot_style, schema
        from mikeplus_mcp.contracts.units import unit_for

        action = payload.get("action", "rain_flow")
        res = mikeio1d.open(payload["res1d"])
        out_png = payload["out_png"]

        if action == "network":
            reach_lines = []
            for name in res.reaches.names:
                try:
                    reach_lines.append(list(res.reaches[name].geometry.to_shapely().coords))
                except Exception:
                    pass
            node_xy = []
            for name in res.nodes.names:
                try:
                    nd = res.nodes[name]
                    node_xy.append((float(nd.xcoord), float(nd.ycoord)))
                except Exception:
                    pass
            plot_style.network_map(reach_lines, node_xy, out_png)
            result = {"ok": True, "png": out_png,
                      "n_reaches": len(reach_lines), "n_nodes": len(node_xy)}
        else:
            df = res.read()

            def series_for(quantity, element):
                cols = schema.match_columns(df.columns, quantity, element)
                if not cols:
                    raise ValueError(f"no series for {quantity}:{element}")
                return df[cols[0]], str(cols[0])

            if action == "rain_flow":
                quantity = payload.get("quantity", "Discharge")
                flow, col = series_for(quantity, payload["element"])
                rain = None
                if payload.get("rain_dfs0"):
                    import mikeio
                    rain = mikeio.read(payload["rain_dfs0"]).to_dataframe().iloc[:, 0]
                plot_style.rain_flow_stacked(
                    flow, out_png, rain=rain,
                    flow_label=quantity, flow_unit=unit_for(quantity) or "",
                )
                result = {"ok": True, "png": out_png, "series": col, "with_rain": rain is not None}

            elif action == "timeseries":
                quantity = payload.get("quantity", "WaterLevel")
                s, col = series_for(quantity, payload["element"])
                plot_style.timeseries(s, out_png, ylabel=f"{quantity} ({unit_for(quantity) or ''})")
                result = {"ok": True, "png": out_png, "series": col}
            else:
                raise ValueError(f"unknown action: {action!r}")
    except Exception as exc:
        result = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    with open(out, "w", encoding="utf-8") as fh:
        json.dump(result, fh, default=str)
    sys.exit(0 if result.get("ok") else 1)


main()
