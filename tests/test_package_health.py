import datetime as dt
from src.package_health import health, release_dates

def test_health_counts_recent_releases():
    ds = [dt.date(2025, 1, 1), dt.date(2026, 9, 1), dt.date(2026, 10, 1), dt.date(2026, 11, 1)]
    h = health(ds, dt.date(2026, 11, 9))
    assert h["releases_total"] == 4 and h["releases_last_90d"] == 3 and h["days_since_last"] == 8
    assert h["median_days_between_releases_12m"] == 30.5

def test_npm_parser_skips_meta_keys():
    fake = lambda u: {"time": {"created": "2024-01-01T00:00:00Z", "modified": "2026-11-01T00:00:00Z",
                               "1.0.0": "2025-05-01T10:00:00Z", "1.1.0": "2026-02-01T10:00:00Z"}}
    assert release_dates("npm", "@x/y", fake) == [dt.date(2025, 5, 1), dt.date(2026, 2, 1)]
