import csv, datetime as dt, json, shutil
from pathlib import Path
import src.radar as radar

def repo(name, owner, stars, created="2026-06-01", desc="", topics=(), fork=False, otype="Organization"):
    return dict(full_name=f"{owner}/{name}", name=name, html_url=f"https://github.com/{owner}/{name}", description=desc,
                topics=list(topics), fork=fork, archived=False, stargazers_count=stars, created_at=created + "T00:00:00Z",
                language="Python", owner=dict(login=owner, type=otype))

REPOS = [repo("voice-agent", "acme-blr", 900, desc="Hinglish voice agent for sales calls", topics=["ai-agents"]),
         repo("awesome-llm", "lister", 5000, desc="Awesome curated list"),                      # list: drop
         repo("gpu-serve", "sfco", 3000, desc="LLM inference server"),                          # not India: drop
         repo("robo-arm", "pune-robotics", 120, desc="ROS2 manipulation", otype="User"),
         repo("composio", "composiohq", 400, desc="agent toolkits"),                            # in funding tracker
         repo("forked", "acme-blr", 999, fork=True)]                                            # fork: drop
USERS = {"acme-blr": "Bengaluru, India", "lister": "Delhi", "sfco": "San Francisco", "pune-robotics": "Pune",
         "composiohq": "Bangalore", "indianapolis-dev": "Indianapolis"}

def fake_fetch(url):
    if "search/repositories" in url:
        return {"items": REPOS} if "topic:llm+" in url else {"items": []}
    login = url.rsplit("/", 1)[1]
    return {"location": USERS.get(login, ""), "type": "Organization"}

def setup(tmp_path, monkeypatch):
    root = tmp_path / "r"; (root / "data").mkdir(parents=True); (root / "docs").mkdir()
    shutil.copy(Path(radar.ROOT) / "data" / "deals.csv", root / "data" / "deals.csv")
    monkeypatch.setattr(radar, "ROOT", root); monkeypatch.setattr(radar.time, "sleep", lambda s: None)
    return root

def test_india_filter_and_product_filter(tmp_path, monkeypatch):
    root = setup(tmp_path, monkeypatch)
    radar.main(today=dt.date(2026, 11, 9), fetch=fake_fetch)
    rows = list(csv.DictReader(open(root / "data" / "radar_latest.csv")))
    names = {r["full_name"] for r in rows}
    assert names == {"acme-blr/voice-agent", "pune-robotics/robo-arm", "composiohq/composio"}
    layers = {r["full_name"]: r["layer"] for r in rows}
    assert layers["acme-blr/voice-agent"] == "Voice & speech" and layers["pune-robotics/robo-arm"] == "Physical AI"
    assert {r["full_name"]: r["in_funding_tracker"] for r in rows}["composiohq/composio"] == "True"
    assert "Bengaluru" not in radar.INDIA.sub("", "Bengaluru") and not radar.INDIA.search("Indianapolis, Indiana")

def test_weekly_gain_and_one_snapshot_per_day(tmp_path, monkeypatch):
    root = setup(tmp_path, monkeypatch)
    radar.main(today=dt.date(2026, 11, 2), fetch=fake_fetch)
    REPOS[0]["stargazers_count"] = 1000                                   # +100 in a week
    radar.main(today=dt.date(2026, 11, 9), fetch=fake_fetch)
    radar.main(today=dt.date(2026, 11, 9), fetch=fake_fetch)              # re-run same day: no duplicate rows
    rows = list(csv.DictReader(open(root / "data" / "radar_latest.csv")))
    assert rows[0]["full_name"] == "acme-blr/voice-agent" and rows[0]["weekly_star_gain"] == "100"
    hist = list(csv.DictReader(open(root / "data" / "radar_history.csv")))
    assert len([h for h in hist if h["date"] == "2026-11-09"]) == 3
    assert json.load(open(root / "docs" / "radar_summary.json"))["ranking"] == "weekly star gain"
    REPOS[0]["stargazers_count"] = 900
