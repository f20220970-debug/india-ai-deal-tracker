"""AI builder radar: finds fast-rising AI repos by India-based builders, weekly.

How it works (runs on GitHub Actions with the built-in GITHUB_TOKEN):
  1. SEARCH   GitHub repo search by AI topics, recent repos only (created in the last 12 months, >= 25 stars)
  2. LOCATE   look up each owner's profile location (cached in data/owner_cache.json) and keep India-based owners
  3. FILTER   drop forks, archived repos, tutorials, courses and awesome-lists (they collect stars, not products)
  4. SCORE    star velocity: stars gained since last week's snapshot; on the first run, stars per 30 days of age
  5. FLAG     layer (agents, dev tools, infra, voice, physical AI, vertical, foundation models) and whether the
              team is already in the funding tracker
  6. PUBLISH  data/radar_latest.csv, data/radar_history.csv, docs/radar.md, docs/index.html
"""
import csv, datetime as dt, html, json, os, re, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOPICS = ["llm", "ai-agents", "agents", "generative-ai", "rag", "mcp", "llmops", "speech-recognition",
          "text-to-speech", "robotics", "computer-vision", "indic", "voice-assistant", "ai"]
INDIA = re.compile(r"\b(india|bharat|bengaluru|bangalore|mumbai|bombay|delhi|ncr|gurgaon|gurugram|noida|hyderabad|"
                   r"pune|chennai|kolkata|ahmedabad|jaipur|kochi|cochin|indore|chandigarh|bhubaneswar|coimbatore|"
                   r"lucknow|thiruvananthapuram|trivandrum|mysore|mysuru|visakhapatnam|vizag|surat|nagpur|goa|"
                   r"pilani|kanpur|kharagpur|roorkee|guwahati)\b", re.I)
NOT_PRODUCT = re.compile(r"awesome|tutorial|course|roadmap|interview|cheat.?sheet|\bnotes\b|\blearn|\bbook\b|"
                         r"list of|papers|100.?days|bootcamp|homework|assignment|resume|portfolio|curated|"
                         r"prompts? collection|examples?$", re.I)
LAYERS = [("Physical AI", r"robot|\bros2?\b|drone|uav|autonomous|embodied|slam|lidar"),
          ("Voice & speech", r"speech|voice|tts|asr|whisper|audio|text-to-speech"),
          ("Agents", r"agent|agentic|mcp|autonomous workflow|crew|multi-agent|browser.?use"),
          ("Infrastructure", r"inference|serving|gpu|vector|embedding|quantiz|llmops|observability|eval|gateway|cache"),
          ("Foundation models", r"indic|pretrain|fine.?tun|foundation model|tokenizer|\bslm\b"),
          ("Vertical AI", r"health|medical|legal|finance|fintech|education|edtech|agri|insurance|hr\b|recruit"),
          ("Dev tools", r"sdk|cli|framework|library|devtool|testing|code|ide|api")]


def http_json(url, token, tries=3):
    import urllib.request, urllib.error
    req = urllib.request.Request(url, headers={"Accept": "application/vnd.github+json", "User-Agent": "ai-builder-radar",
                                               **({"Authorization": f"Bearer {token}"} if token else {})})
    for i in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (403, 429) and i < tries - 1:       # rate limit: back off, then retry
                time.sleep(20 * (i + 1)); continue
            if e.code == 404:
                return None
            raise


def layer_of(repo):
    text = " ".join([repo.get("name") or "", repo.get("description") or "", " ".join(repo.get("topics") or [])])
    for name, pat in LAYERS:
        if re.search(pat, text, re.I):
            return name
    return "Application"


def is_product(repo):
    text = f"{repo.get('name','')} {repo.get('description') or ''}"
    return not (repo.get("fork") or repo.get("archived") or NOT_PRODUCT.search(text))


def search(fetch, today, min_stars=25, per_topic=100, pause=2.5):
    since = (today - dt.timedelta(days=365)).isoformat()
    seen = {}
    for t in TOPICS:
        q = f"topic:{t}+created:>{since}+stars:>={min_stars}"
        res = fetch(f"https://api.github.com/search/repositories?q={q}&sort=stars&order=desc&per_page={per_topic}")
        for r in (res or {}).get("items", []):
            seen.setdefault(r["full_name"], r)
        time.sleep(pause)
    return list(seen.values())


def locate(fetch, repos, cache, max_lookups=700):
    looked = 0
    for r in repos:
        login = r["owner"]["login"]
        if login not in cache and looked < max_lookups:
            u = fetch(f"https://api.github.com/users/{login}") or {}
            cache[login] = {"location": u.get("location") or "", "type": u.get("type") or r["owner"].get("type", "")}
            looked += 1
    return [r for r in repos if INDIA.search(cache.get(r["owner"]["login"], {}).get("location", ""))]


def score(repos, history, today, tracker_names):
    last = {}
    for row in history:                                     # most recent earlier snapshot per repo
        if row["date"] < today.isoformat():
            last[row["full_name"]] = int(row["stars"])
    out = []
    for r in repos:
        created = dt.date.fromisoformat(r["created_at"][:10])
        age = max((today - created).days, 14)
        prev = last.get(r["full_name"])
        out.append(dict(
            full_name=r["full_name"], url=r["html_url"], description=(r.get("description") or "")[:140],
            stars=r["stargazers_count"], created=created.isoformat(), language=r.get("language") or "",
            layer=layer_of(r), owner_type=r["owner"].get("type", ""),
            weekly_star_gain="" if prev is None else r["stargazers_count"] - prev,
            stars_per_30d=round(30 * r["stargazers_count"] / age, 1),
            in_funding_tracker=any(n and n in r["full_name"].lower().replace("-", "") for n in tracker_names)))
    has_history = any(o["weekly_star_gain"] != "" for o in out)
    key = (lambda o: o["weekly_star_gain"] if o["weekly_star_gain"] != "" else -1) if has_history else (lambda o: o["stars_per_30d"])
    return sorted(out, key=key, reverse=True)


def publish(rows, history, today, root=None, top=40):
    root = root or ROOT
    data, docs = root / "data", root / "docs"
    fields = list(rows[0].keys()) if rows else ["full_name"]
    with open(data / "radar_latest.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fields); w.writeheader(); w.writerows(rows)
    keep = [h for h in history if h["date"] != today.isoformat()]  # one snapshot per day
    keep += [dict(date=today.isoformat(), full_name=r["full_name"], stars=r["stars"]) for r in rows]
    with open(data / "radar_history.csv", "w", newline="") as f:
        w = csv.DictWriter(f, ["date", "full_name", "stars"]); w.writeheader(); w.writerows(keep)
    by_layer = {}
    for r in rows:
        by_layer[r["layer"]] = by_layer.get(r["layer"], 0) + 1
    summary = dict(date=today.isoformat(), builders=len(rows), by_layer=dict(sorted(by_layer.items(), key=lambda x: -x[1])),
                   orgs=sum(r["owner_type"] == "Organization" for r in rows),
                   already_in_funding_tracker=sum(r["in_funding_tracker"] for r in rows),
                   ranking="weekly star gain" if any(r["weekly_star_gain"] != "" for r in rows) else "stars per 30 days of age")
    json.dump(summary, open(docs / "radar_summary.json", "w"), indent=1)
    head = "| # | Repo | Layer | Stars | Gain this week | Stars/30d | Team | Funded? |\n|---|---|---|---|---|---|---|---|\n"
    body = "".join(f"| {i} | [{r['full_name']}]({r['url']}) | {r['layer']} | {r['stars']} | {r['weekly_star_gain']} | "
                   f"{r['stars_per_30d']} | {'org' if r['owner_type']=='Organization' else 'individual'} | "
                   f"{'in tracker' if r['in_funding_tracker'] else ''} |\n" for i, r in enumerate(rows[:top], 1))
    (docs / "radar.md").write_text(f"# AI builder radar, {today}\n\n{summary['builders']} India-based AI repos (created in the last "
                                   f"12 months, 25+ stars), ranked by {summary['ranking']}.\n\n" + head + body)
    rows_html = "".join(f"<tr><td>{i}</td><td><a href='{html.escape(r['url'])}'>{html.escape(r['full_name'])}</a><br><small>"
                        f"{html.escape(r['description'])}</small></td><td>{r['layer']}</td><td>{r['stars']}</td>"
                        f"<td>{r['weekly_star_gain']}</td><td>{r['stars_per_30d']}</td><td>{'org' if r['owner_type']=='Organization' else 'individual'}</td>"
                        f"<td>{'in tracker' if r['in_funding_tracker'] else ''}</td></tr>" for i, r in enumerate(rows[:top], 1))
    layers = " · ".join(f"{k}: {v}" for k, v in summary["by_layer"].items())
    (docs / "index.html").write_text(f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI Builder Radar</title><style>body{{font:15px/1.5 system-ui,sans-serif;max-width:1100px;margin:auto;padding:16px;color:#1d1d1f;background:#fff}}
table{{border-collapse:collapse;width:100%}}td,th{{border-bottom:1px solid #ddd;padding:6px;text-align:left;vertical-align:top}}small{{color:#555}}
.k{{display:inline-block;margin:4px 14px 4px 0}}.k b{{font-size:22px;display:block}}</style></head><body>
<h1>India AI builder radar</h1><p>Re-run every week on GitHub Actions. Finds AI repos by India-based builders (created in the last 12 months, 25+ stars),
drops tutorials and lists, and ranks by <b>{summary['ranking']}</b>. Last run: <b>{today}</b>. A sourcing aid, not an endorsement: stars measure attention, not usage.</p>
<div><span class="k"><b>{summary['builders']}</b>builders found</span><span class="k"><b>{summary['orgs']}</b>organisations</span>
<span class="k"><b>{summary['already_in_funding_tracker']}</b>already in funding tracker</span></div><p><small>{layers}</small></p>
<table><tr><th>#</th><th>Repo</th><th>Layer</th><th>Stars</th><th>Gain this week</th><th>Stars/30d</th><th>Team</th><th>Funded?</th></tr>{rows_html}</table>
<p><small>Code: <a href="https://github.com/f20220970-debug/india-ai-deal-tracker">india-ai-deal-tracker</a> · funding database, market map, memo and technical diligence in the same repo.</small></p></body></html>""")
    return summary


def main(today=None, fetch=None):
    today = today or dt.date.today()
    token = os.environ.get("GITHUB_TOKEN", "")
    fetch = fetch or (lambda u: http_json(u, token))
    cache_path = ROOT / "data" / "owner_cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    hist_path = ROOT / "data" / "radar_history.csv"
    history = list(csv.DictReader(open(hist_path))) if hist_path.exists() else []
    tracker = [re.sub(r"[^a-z0-9]", "", r["company"].lower().replace(" ai", "").replace(".ai", ""))
               for r in csv.DictReader(open(ROOT / "data" / "deals.csv"))]
    repos = [r for r in search(fetch, today) if is_product(r)]
    india = locate(fetch, repos, cache)
    cache_path.write_text(json.dumps(cache, indent=0, sort_keys=True))
    rows = score(india, history, today, [t for t in tracker if len(t) >= 4])
    summary = publish(rows, history, today)
    print(json.dumps(summary, indent=1))
    if not rows:
        sys.exit("radar found no builders: check the API token and rate limits")


if __name__ == "__main__":
    main()
