---
title: "Investment thesis memo: Indian voice agents for sales and support"
subtitle: "Pre-seed / seed lens · India AI deal tracker · Pavitra Seth · Nov 2026"
geometry: margin=2cm
fontsize: 10pt
---

**What this is.** A practice memo written the way an early-stage AI fund analyst would, built on a tracker of 46 Indian AI funding rounds from public sources (StartupTalky weekly funding tables, Jul–Nov 2026; Inc42 top-funded AI list). The unit-economics numbers are **illustrative assumptions**, not any company's figures.

## 1. What the deal flow says
- **Early stage dominates:** 61.5% of the 39 dated rounds (Jul–Nov 2026) were angel, pre-seed or seed. Median seed: **USD 2.35M**; median pre-seed: **USD 1.5M**.
- **Bengaluru is the centre:** 51% of dated rounds list Karnataka.
- **The application layer leads:** application (10), agents (7), vertical AI (7) and physical AI (7) rounds, against 4 infrastructure and 1 foundation-model round. Physical AI is the most active at seed (6 of its 7 rounds), mostly robotics and drones.
- **Agents cluster in one workflow:** 5 of 7 agent rounds are sales or customer-service agents (Karta AI, RevRag AI, Desible.ai, Superleap, Revspot). This is the most crowded segment in the tracker.

## 2. The thesis
Indian businesses run on phone calls in many languages: lead follow-up, collections, support, hiring. Voice agents that handle these calls are useful and sell fast. But the segment is crowded and the core inputs (speech-to-text, LLM, text-to-speech, telephony) are rented, so **the winners will be the ones that own something the others rent**: Indic speech quality, a workflow integration that is painful to rip out (CRM, loan system, ATS), or outcome-based pricing.

## 3. Unit economics: where margin lives (illustrative)
Base case: customer pays ₹6 per handled minute; cost ₹3.5/min (speech ₹1.2, LLM ₹0.8, telephony ₹0.9, infra and support ₹0.6); 40,000 minutes per customer per month; CAC ₹2.5 lakh; 3% monthly churn.

| Price/min | LLM cost/min | Gross margin | CAC payback | LTV/CAC |
|---|---|---|---|---|
| ₹6 | ₹0.8 | 41.7% | 2.5 months | 13.3 |
| ₹5 | ₹0.8 | 30.0% | 4.2 months | 8.0 |
| ₹4 | ₹0.8 | 12.5% | 12.5 months | 2.7 |
| ₹4 | ₹1.6 | −7.5% | never | negative |

**Read:** a price war from ₹6 to ₹4 a minute cuts gross margin from 42% to 12.5%. Per-minute pricing in a crowded market is the main risk; cheaper models help, but price falls faster.

## 4. What I would diligence in a founder pitch
1. **Stack:** which parts are owned vs rented; word error rate on Indic and code-mixed (Hinglish) calls vs a commercial API baseline.
2. **Evals and guardrails:** how they test the agent before a change ships, what happens when the LLM fails, how compliance-sensitive calls (collections, insurance) are routed to a human.
3. **Pricing:** per minute vs per outcome (meeting booked, payment collected); gross margin by customer.
4. **Retention:** logo and minute retention by cohort; whether usage grows inside accounts.
5. **Founders:** domain access (lending, staffing, D2C) and whether they can sell to Indian enterprises *and* go global.

## 5. Red flags
Margin that depends on one model provider's price; demos on clean English calls only; no eval set; "AI" revenue that is mostly human-in-the-loop services.

## 6. Limits of this memo
Public funding tables are incomplete (undisclosed amounts, missing investors) and classifications into layers are mine. A real memo would add founder calls, customer references and product trials.
