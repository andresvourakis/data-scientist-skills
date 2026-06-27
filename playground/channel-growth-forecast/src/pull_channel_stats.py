"""
Pull daily channel stats from the YouTube Analytics API and append to
data/raw/channel_stats_daily.csv.

Runs nightly on the analytics box (cron @ 03:15). If it dies, just rerun it the
next morning, it backfills from the last date in the csv.

NOTE: subscribers is the *cumulative* subscriber count as of that day (that's what
the API returns), not the daily gain.
"""
import csv
import os
import datetime as dt

# --- the channels we report on -------------------------------------------------
# Keep this list in sync with data/raw/channel_roster.csv
CHANNEL_IDS = [
    "UCq8Hk2bZpFv3nT0wYxA1bCa",  # Pixel Forge
    "UC2mLp9Qz7rVnK4sWxYa0bD1",  # Skillet & Spoon
    "UC7Hq2bQpL9rV8nT0wYxA1bC",  # Trailhead
    "UCx7Hk2bZpFv3nT0wYxA1bD2",  # Wattage
    "UCa1Pixel0Forge9rV8nT0wYx",  # The Lore Vault
    "UC9mZ2pLrV8nT0wYxA1bC3kQ9",  # Penny & Plan
    "UCkQ9mZ2pLrV8nT0wYxA1bC3k",  # Studio Hum
    "UCnT0wYxA1bC3kQ9mZ2pLrV8n",  # Grit & Gain
    "UCwYxA1bC3kQ9mZ2pLrV8nT0w",  # Paper Planes
    "UCbC3kQ9mZ2pLrV8nT0wYxA1b",  # Night Shift Sci
]

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT_FILE = os.path.join(RAW, "channel_stats_daily.csv")

METRICS = ["views", "estimatedMinutesWatched", "subscribersGained", "subscribers",
           "averageViewDuration"]


def get_service():
    """Build the authenticated Analytics API client (OAuth token cached on disk)."""
    from googleapiclient.discovery import build  # noqa: F401
    import google.oauth2.credentials  # noqa: F401
    # token.json is created by the one-time auth flow, see README
    raise NotImplementedError("wired up on the analytics box, not locally")


def last_pulled_date():
    if not os.path.exists(OUT_FILE):
        return dt.date(2026, 3, 1)
    last = None
    with open(OUT_FILE) as f:
        for row in csv.DictReader(f):
            d = dt.date.fromisoformat(row["date"])
            if last is None or d > last:
                last = d
    return last


def pull(service, channel_id, start, end):
    resp = service.reports().query(
        ids=f"channel=={channel_id}",
        startDate=start.isoformat(),
        endDate=end.isoformat(),
        metrics=",".join(METRICS),
        dimensions="day",
    ).execute()
    return resp.get("rows", [])


def main():
    service = get_service()
    start = last_pulled_date() + dt.timedelta(days=1)
    end = dt.date.today()
    for cid in CHANNEL_IDS:
        rows = pull(service, cid, start, end)
        with open(OUT_FILE, "a", newline="") as f:
            w = csv.writer(f)
            for r in rows:
                day, views, emw, gained, subs, avd = r
                w.writerow([day, cid, subs, views, emw, avd])
        print(f"pulled {len(rows)} days for {cid}")


if __name__ == "__main__":
    main()
