"""Shipping-pace check for tracker companies with public SDKs (PyPI / npm release history).
A diligence signal: is the team still shipping, and how often? Re-run weekly with the radar."""
import datetime as dt, json, statistics, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACKAGES = [("Composio", "pypi", "composio"), ("Composio", "npm", "@composio/core"),
            ("Sarvam AI", "pypi", "sarvamai"), ("Sarvam AI", "npm", "sarvamai"),
            ("Keploy", "npm", "@keploy/sdk")]          # ownership checked via repository / author fields


def release_dates(registry, name, get=lambda u: json.load(urllib.request.urlopen(u, timeout=30))):
    if registry == "pypi":
        d = get(f"https://pypi.org/pypi/{name}/json")
        return sorted(dt.date.fromisoformat(f[0]["upload_time"][:10]) for f in d["releases"].values() if f)
    d = get(f"https://registry.npmjs.org/{name.replace('/', '%2F')}")
    return sorted(dt.date.fromisoformat(v[:10]) for k, v in d["time"].items() if k not in ("created", "modified"))


def health(dates, today):
    year = [d for d in dates if (today - d).days <= 365]
    gaps = [(b - a).days for a, b in zip(year, year[1:])]
    return dict(releases_total=len(dates), first_release=dates[0].isoformat(), last_release=dates[-1].isoformat(),
                days_since_last=(today - dates[-1]).days, releases_last_90d=sum((today - d).days <= 90 for d in dates),
                median_days_between_releases_12m=round(float(statistics.median(gaps)), 1) if gaps else None)


def main(today=None, fetch=None):
    today = today or dt.date.today()
    rows = []
    for company, reg, name in PACKAGES:
        try:
            ds = release_dates(reg, name, fetch) if fetch else release_dates(reg, name)
            rows.append(dict(company=company, registry=reg, package=name, **health(ds, today)))
        except Exception as e:                                    # one registry failing must not kill the run
            rows.append(dict(company=company, registry=reg, package=name, error=str(e)[:80]))
    json.dump(dict(date=today.isoformat(), packages=rows), open(ROOT / "docs" / "package_health.json", "w"), indent=1)
    lines = [f"# SDK shipping pace, {today}\n", "| Company | Package | Releases (total) | Last 90 days | Median days between releases (12m) | Last release |",
             "|---|---|---|---|---|---|"]
    lines += [f"| {r['company']} | {r['registry']}: `{r['package']}` | {r.get('releases_total','')} | {r.get('releases_last_90d','')} | "
              f"{r.get('median_days_between_releases_12m','')} | {r.get('last_release', r.get('error',''))} |" for r in rows]
    (ROOT / "docs" / "package_health.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
