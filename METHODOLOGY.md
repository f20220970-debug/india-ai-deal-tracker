# Methodology

How the database and radar are built, so a reader can judge how far to trust them.

## Funding database (`data/deals.csv`)

**Definition of an "Indian AI startup" used here:** a company listed in an Indian startup-funding tracker whose product is AI-native (models, agents, AI applications, AI infrastructure or developer tools) or physical AI (robotics, drones, AI sensors). Companies headquartered abroad with Indian founders or an Indian state listed (e.g. "California / Karnataka") are included, since this matches the thesis "Indian founders building globally".

**Inclusion rules**
- Rounds reported between Jul and Nov 2026 in StartupTalky's weekly Indian funding tables (39 dated rounds), plus AI companies from Inc42's "Top 20 Funded AI Startups in India 2026" list (7 rows, total funding rather than a dated round, marked as such in `source`).
- Excluded: space tech, 3D printing, advanced materials, quantum-only and generic SaaS without an AI product, even when listed next to AI rounds.

**Data handling**
- Every row cites its source. These are **secondary sources** (news trackers); rows have not been checked against company filings or primary announcements, which a fund would do before relying on a figure.
- Amounts are as reported (INR converted at the tracker's own USD figure). **Undisclosed amounts are left blank, not estimated**, and are excluded from medians.
- Duplicate announcements of the same round (e.g. Paar Autonomy listed in two weeks with different labels) are merged into one row.
- Layer and segment labels (application, agents, vertical AI, dev tools, infrastructure, foundation models, physical AI) are **my classification** from each company's stated product.
- Refresh: the funding table is updated by hand; the market map and summary statistics regenerate from it on every push.

**Spot-check against news reports (9 Nov 2026):** 4 rows checked against independent coverage.
| Row | Tracker said | Independent source | Result |
|---|---|---|---|
| Emergent | USD 130M Series C, lead Creaegis | Inc42, 15 Jul 2026 | Matches |
| RevRag AI | USD 2.5M Seed, Accion Ventures, Cedar Hill | StartupTalky news, 14 Oct 2026 | Matches; segment corrected to in-app agents for lenders and insurers |
| Simplismart | USD 14M Series B, Dallas Venture Capital | The SaaS News, 27 Oct 2026 | Matches |
| Sarvam AI | USD 75M Series B led by Activate | Inc42, 5 Aug 2026 (MCA filings) | **Corrected:** USD 74M *extension* of the USD 300M Series B; no named lead, NVIDIA the largest investor, Activate one participant |

One in four rows needed correcting, a reminder that secondary trackers compress rounds into one line. Checked rows are marked in the `source` column.

**Known limits:** two secondary sources only; small sample (39 dated rounds); investor fields often list only the lead; some company descriptions on trackers are thin.

## Builder radar (`src/radar.py`, every Monday)
1. **Search:** GitHub repositories with AI topics (llm, ai-agents, rag, mcp, speech, robotics, indic, etc.), created in the last 12 months, searched in star bands (25-99, 100-499, 500+) so large global repos don't crowd out smaller builders.
2. **Locate:** keep repos whose owner's GitHub profile location names India or an Indian city (word match, so "Indiana" is not India). Lookups are cached.
3. **Filter:** drop forks, archived repos, tutorials, courses, handbooks, guides, archives and awesome-lists (they attract stars without being products).
4. **Score:** star velocity: week-over-week star gain once a week of history exists; until then, stars per 30 days of age (age floored at 14 days).
5. **Flag:** an individual's repo gaining more than 2,000 stars a month is marked "check stars" (possible bought or bot stars) and listed after the ranking; teams already in the funding database are marked by exact name match.

**What the radar is and isn't:** a sourcing aid that surfaces builders to look at. Stars measure attention, not usage; any lead needs usage data (downloads, active users, revenue) and a founder conversation before it means anything.

## SDK release pace (`src/package_health.py`, every Monday)
Release history from PyPI and npm for tracker companies with public SDKs. Package ownership is checked via repository and author fields. Release counts need interpreting: auto-generated SDKs (e.g. Sarvam's) publish several versions a day, and an SDK can go quiet because the product no longer needs it (Keploy moved to eBPF).
