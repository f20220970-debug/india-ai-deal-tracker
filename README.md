# India AI deal tracker, market map and investment memo

[![tests](https://github.com/f20220970-debug/india-ai-deal-tracker/actions/workflows/tests.yml/badge.svg)](https://github.com/f20220970-debug/india-ai-deal-tracker/actions/workflows/tests.yml) [![weekly-radar](https://github.com/f20220970-debug/india-ai-deal-tracker/actions/workflows/radar.yml/badge.svg)](https://github.com/f20220970-debug/india-ai-deal-tracker/actions/workflows/radar.yml)

**Live radar page:** `https://f20220970-debug.github.io/india-ai-deal-tracker/` (re-run every Monday on GitHub Actions)

Built to StemAI India's technical analyst brief: map India's AI builder ecosystem, keep a structured deal database, and write a memo with a simple unit-economics model.

- **`data/deals.csv`:** 46 Indian AI funding rounds (Jul–Nov 2026 weekly tables + top-funded list), each with layer (application, agents, vertical AI, dev tools, infrastructure, foundation models, physical AI), segment, stage, amount, lead investor, state and **source**.
- **`docs/market_map.md`:** companies by layer and segment, generated from the data.
- **[Investment memo (PDF)](docs/Investment_Memo_Voice_Agents.pdf):** thesis on Indian sales/support voice agents, the most crowded agent segment in the tracker.
- **AI builder radar (`src/radar.py`, weekly):** searches GitHub for AI repos created in the last 12 months by **India-based** owners, drops forks, tutorials and awesome-lists, ranks by **star velocity** (week-over-week gain once history exists) and flags layer and whether the team is already in the funding tracker. Owner lookups are cached; every run is snapshotted in `data/radar_history.csv`.
- **[Technical diligence: Composio (PDF)](docs/Technical_Diligence_Composio.pdf):** architecture, shipping pace, dependencies and risks from public code and package registries, plus founder questions.
- **SDK shipping pace (`src/package_health.py`, weekly):** release cadence from PyPI and npm for tracker companies with public SDKs (Composio, Sarvam AI, Keploy) → `docs/package_health.md`.
- **`src/unit_economics.py`:** gross margin, CAC payback and LTV/CAC with a price × model-cost sensitivity grid. **Inputs are illustrative assumptions.**

**How the data is built, its sources and its limits:** see [METHODOLOGY.md](METHODOLOGY.md).

## Findings (from the tracker)
| | |
|---|---|
| Pre-seed/seed/angel share of dated rounds | **61.5%** |
| Median seed / pre-seed | **USD 2.35M / 1.5M** |
| Rounds listing Karnataka | **51%** |
| Agent rounds in sales or support | **5 of 7** |
| Most seed-heavy layer | **Physical AI** (6 of its 7 rounds at seed or earlier) |

**Caveat the radar respects:** stars measure attention, not usage. Composio's product repo has ~30K stars, but its own awesome-list has ~73K. The radar is a sourcing aid; diligence needs usage data.

Unit economics (illustrative): a price cut from ₹6 to ₹4 per minute takes gross margin from 41.7% to 12.5%: per-minute pricing in a crowded market is the main risk.

## Run
```
pip install pandas pytest
python src/analyse.py && python src/unit_economics.py && python src/package_health.py && pytest -q
GITHUB_TOKEN=... python src/radar.py      # needs a GitHub token; runs weekly in Actions
```
<sub>Sources: StartupTalky "Indian Startups Funding and Investors Data 2026"; Inc42 "Top 20 Funded AI Startups in India 2026". Layer classification is mine; amounts as reported.</sub>
