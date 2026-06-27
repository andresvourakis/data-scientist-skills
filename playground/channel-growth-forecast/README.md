# Channel Growth & Revenue Forecast

Internal analytics for **Milepost Media** — subscriber growth and revenue
forecasting across our portfolio of **12 channels**. Powers the monthly exec
revenue review.

## What it does

1. Pulls daily stats (views, subscribers, watch time) for **every channel** from
   the YouTube Analytics API.
2. Joins in ad revenue and sponsorship revenue.
3. Rolls everything up to a monthly per-channel table.
4. Projects subscribers and revenue **18 months** forward, per channel, with **no
   artificial caps** — growth is modeled straight off each channel's own trend.
5. Outputs a forecast feed for the exec dashboard, refreshed nightly.

## Pipeline

```
YouTube Analytics API ──(nightly cron)──▶ channel_stats_daily.csv ─┐
                                                                   ├─▶ metrics.py ─▶ monthly_channel_metrics.csv ─▶ revenue_model.ipynb ─▶ outputs/forecast.csv
YouTube Studio (revenue) ─────────────────▶ studio_export.csv ─────┤
sponsorship tracker ──────────────────────▶ sponsorships.csv ──────┘
```

## Setup

```bash
pip install -r requirements.txt
python src/pull_channel_stats.py     # one-time auth, then runs on cron
python src/metrics.py                # build the monthly table
jupyter lab notebooks/               # run 02_revenue_model.ipynb to refresh the forecast
```

## Layout

- `src/pull_channel_stats.py` — nightly API pull
- `src/metrics.py` — builds the monthly per-channel metrics table
- `notebooks/01_explore.ipynb` — scratch EDA
- `notebooks/02_revenue_model.ipynb` — the forecast (this is the one the exec deck uses)
- `data/raw/` — pulled + exported source data
- `data/processed/` — the monthly metrics table
- `outputs/` — forecast feed for the dashboard

## Owner

Maintained by the data team (currently just me). Ping me before the monthly
review if numbers look off.
