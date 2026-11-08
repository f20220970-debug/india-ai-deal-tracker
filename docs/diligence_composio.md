---
title: "Technical diligence note: Composio (tool integrations for AI agents)"
subtitle: "Practice note from public sources · Pavitra Seth · 8 Nov 2026"
geometry: margin=1.8cm
fontsize: 10pt
---

**Why this company.** Composio fits an India-focused AI fund's thesis: Indian founders building globally, in agent infrastructure. It is past seed, so this is a case study in *how* I would run technical diligence, not a recommendation. Registry figures were pulled by `src/package_health.py` on 8 Nov 2026; everything else is cited at the end.

## 1. Snapshot
- **What it does:** lets AI agents take actions in 1,000+ apps (Slack, GitHub, Salesforce, HubSpot, Gmail and more), with managed authentication (OAuth, API keys), tool search, context management and a sandboxed workbench.
- **Team:** founded 2022 by Soham Ganatra (CEO, IIT Bombay) and Karan Vaidya; HQ San Francisco. Inc42 lists the founding year as 2023, so check this.
- **Funding:** USD 25M Series A led by Lightspeed (USD 29M total). Existing investors: Elevation Capital and Together Fund. Angels include Guillermo Rauch (Vercel) and Dharmesh Shah (HubSpot).
- **Traction (company-reported):** 100,000+ developers and 200+ customers, including Glean.

## 2. What the public code and registries show
**Architecture: the open-source SDK is a thin client.** The Python `composio` package depends on a generated API client (`composio-client`), pydantic and JSON-schema tools. The npm package `@composio/core` depends on `@composio/client`. The value (auth, toolkits, execution) sits in the **hosted platform**, while the MIT-licensed SDK is distribution. So the moat is toolkit breadth, managed auth and reliability, not code anyone can copy. The org also publishes Helm charts, consistent with self-hosting for enterprise.

**Shipping pace: fast, and recently re-platformed.**

| Package | Releases (total) | Last 90 days | Median days between releases (12m) |
|---|---|---|---|
| PyPI `composio` (new SDK, first release Dec 2024) | 86 | 16 | 6 |
| npm `@composio/core` | 156 | 16 | 4 |
| PyPI `composio-core` (old SDK, since Apr 2024) | 223 | ~0 | n/a (largely quiet since mid-2025) |

The move from `composio-core` to `composio` looks like a v3 rewrite. **Diligence question:** what did the migration cost existing customers, and how are breaking changes handled?

**Dependencies worth asking about.** The core SDK lists the **OpenAI client** as a required dependency in both Python and JavaScript, even though the docs cover Gemini, LangChain/LangGraph, the Vercel AI SDK and others. Real-time triggers run over **Pusher** (`pysher`, `pusher-js`), a third-party service: what happens to triggers if it degrades, and what does it cost at scale?

**Attention is not usage.** The product repo has ~30K GitHub stars, but the same org's curated list *awesome-claude-skills* has ~73K, more than the product. Composio is clearly good at distribution, but stars can't show usage. Usage needs active API keys, tool calls per account, paid conversion and net revenue retention.

## 3. Market and risks (my analysis)
- **Crowded layer:** agent integrations are also offered by Merge (Agent Handler), Zapier MCP, Pipedream MCP and Toolhouse.
- **Commoditisation:** MCP standardises how agents call tools, and model labs ship native connectors. Composio's defence has to be what's hard to copy: auth at enterprise scale, 1,000+ maintained toolkits, reliability, and the "learning" layer it is raising for.
- **Pricing:** four tiers metered on tool calls, premium tool calls and connected accounts. This comes from a competitor's blog, so I haven't verified the prices.

## 4. Questions I would ask the founders
1. **Reliability:** tool-call success rate and p95 latency per toolkit; how they detect an upstream API change before customers do.
2. **Maintenance cost:** share of toolkits generated automatically vs maintained by hand; engineers per 100 toolkits.
3. **Security:** how OAuth tokens are stored and scoped; audit logs; which certifications are complete.
4. **Unit economics:** gross margin per tool call; revenue concentration in the top 10 customers; net revenue retention by cohort.
5. **Dependencies:** why OpenAI is a hard dependency; plan if Pusher or a model provider changes terms.
6. **The learning layer:** what metric proves agents get better with use?

## 5. Read-out
**Strong signals:** a team with global distribution, very fast shipping, and a hosted moat behind an open SDK. **Key risks:** commoditisation by MCP and model-lab connectors, and the fact that the real moat (reliability at scale) can't be seen in public data. **What would change my view:** per-toolkit reliability metrics and retention cohorts.

<small>**Sources:** YourStory, "Composio raises $25M led by Lightspeed"; Inc42, "Top 20 Funded AI Startups in India 2026"; GitHub org page github.com/ComposioHQ (stars as of the page fetched 8 Nov 2026); OSS Insight (ComposioHQ/composio); everydev.ai (Composio profile); Merge blog, "Composio pricing" (competitor-written); PyPI JSON API (`composio`, `composio-core`); npm registry (`@composio/core`); Composio docs (framework guides).</small>
