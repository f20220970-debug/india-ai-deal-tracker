"""Illustrative unit economics for an Indian sales/support voice-agent startup.
All inputs are ASSUMPTIONS for a diligence template, not any company's figures. Change them and re-run."""
import json, itertools
A = dict(price_per_min_inr=6.0,       # what the customer pays per handled minute
         stt_tts_inr=1.2, llm_inr=0.8, telephony_inr=0.9, infra_support_inr=0.6,   # cost per minute
         mins_per_customer_month=40000, cac_inr=250000, monthly_churn=0.03, sales_payback_target_m=12)
def model(a):
    cost = a["stt_tts_inr"] + a["llm_inr"] + a["telephony_inr"] + a["infra_support_inr"]
    gm = 1 - cost / a["price_per_min_inr"]
    gp_month = a["mins_per_customer_month"] * (a["price_per_min_inr"] - cost)
    return dict(gross_margin_pct=round(100*gm,1), gross_profit_per_customer_month_inr=round(gp_month),
                cac_payback_months=round(a["cac_inr"]/gp_month,1), ltv_to_cac=round(gp_month/a["monthly_churn"]/a["cac_inr"],1))
base = model(A)
grid = []
for price, llm in itertools.product([4.0, 5.0, 6.0], [0.4, 0.8, 1.6]):    # price war x model cost
    grid.append(dict(price_per_min_inr=price, llm_inr=llm, **model({**A, "price_per_min_inr": price, "llm_inr": llm})))
json.dump(dict(assumptions=A, base=base, sensitivity=grid), open("docs/unit_economics.json","w"), indent=1)
print(base); [print(g) for g in grid]
