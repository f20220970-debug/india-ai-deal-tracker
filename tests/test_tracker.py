import pandas as pd, subprocess, json, sys
def test_every_row_has_source_and_layer():
    d = pd.read_csv("data/deals.csv"); assert d.source.notna().all() and d.layer.notna().all()
    assert not d.company.duplicated().any()
def test_unit_economics_margin_falls_with_price():
    subprocess.run([sys.executable, "src/unit_economics.py"], check=True, capture_output=True)
    g = json.load(open("docs/unit_economics.json"))["sensitivity"]
    m = {(r["price_per_min_inr"], r["llm_inr"]): r["gross_margin_pct"] for r in g}
    assert m[(6.0, 0.8)] > m[(5.0, 0.8)] > m[(4.0, 0.8)]
