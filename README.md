# India AI deal tracker, market map and investment memo

[![tests](https://github.com/f20220970-debug/india-ai-deal-tracker/actions/workflows/tests.yml/badge.svg)](https://github.com/f20220970-debug/india-ai-deal-tracker/actions/workflows/tests.yml)

Built to StemAI India's technical analyst brief: map India's AI builder ecosystem, keep a structured deal database, and write a memo with a simple unit-economics model.

- **`data/deals.csv`:** 46 Indian AI funding rounds (Jul–Nov 2026 weekly tables + top-funded list), each with layer (application, agents, vertical AI, dev tools, infrastructure, foundation models, physical AI), segment, stage, amount, lead investor, state and **source**.
- **`docs/market_map.md`:** companies by layer and segment, generated from the data.
- **[Investment memo (PDF)](docs/Investment_Memo_Voice_Agents.pdf):** thesis on Indian sales/support voice agents, the most crowded agent segment in the tracker.
- **`src/unit_economics.py`:** gross margin, CAC payback and LTV/CAC with a price × model-cost sensitivity grid. **Inputs are illustrative assumptions.**

## Findings (from the tracker)
| | |
|---|---|
| Pre-seed/seed/angel share of dated rounds | **61.5%** |
| Median seed / pre-seed | **USD 2.35M / 1.5M** |
| Rounds listing Karnataka | **51%** |
| Agent rounds in sales or support | **5 of 7** |
| Most active layer at seed | **Physical AI** (6 of 7 rounds) |

Unit economics (illustrative): a price cut from ₹6 to ₹4 per minute takes gross margin from 41.7% to 12.5%: per-minute pricing in a crowded market is the main risk.

## Run
```
pip install pandas pytest
python src/analyse.py && python src/unit_economics.py && pytest -q
```
<sub>Sources: StartupTalky "Indian Startups Funding and Investors Data 2026"; Inc42 "Top 20 Funded AI Startups in India 2026". Layer classification is mine; amounts as reported.</sub>
