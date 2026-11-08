"""India AI deal tracker: market map + summary stats from data/deals.csv (public sources, per row)."""
import pandas as pd, json
d = pd.read_csv("data/deals.csv")
weekly = d[d.source == "StartupTalky"]                     # dated rounds, Jul-Nov 2026
early = weekly[weekly.stage.isin(["Angel", "Pre-Seed", "Seed"])]
out = {
 "rounds_tracked": len(d), "dated_rounds_jul_nov": len(weekly),
 "pre_seed_seed_share_pct": round(100 * len(early) / len(weekly), 1),
 "median_seed_usd_m": float(early[early.stage == "Seed"].amount_usd_m.median()),
 "median_pre_seed_usd_m": float(early[early.stage == "Pre-Seed"].amount_usd_m.median()),
 "karnataka_share_pct": round(100 * weekly.state.fillna("").str.contains("Karnataka").mean(), 1),
 "rounds_by_layer": weekly.layer.value_counts().to_dict(),
 "early_rounds_by_layer": early.layer.value_counts().to_dict(),
 "agents_segments": weekly[weekly.layer == "Agents"].segment.tolist(),
}
json.dump(out, open("docs/summary.json", "w"), indent=1); print(json.dumps(out, indent=1))
m = d.groupby(["layer", "segment"]).company.apply(lambda s: ", ".join(s)).reset_index()
with open("docs/market_map.md", "w") as f:
    f.write("# India AI market map (rounds Jul-Nov 2026, public sources)\n\n")
    for layer, g in m.groupby("layer"):
        f.write(f"## {layer}\n" + "".join(f"- **{r.segment}:** {r.company}\n" for r in g.itertuples()) + "\n")
