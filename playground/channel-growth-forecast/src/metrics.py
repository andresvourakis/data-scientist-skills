"""
Build the monthly per-channel metrics table that feeds the forecast notebook
and the exec dashboard.

Inputs (data/raw):
  - channel_stats_daily.csv     nightly API pull (views, subs, watch time)
  - studio_export_2026-05.csv   manual monthly export from YouTube Studio (revenue)
  - sponsorships.csv            the sponsorship tracking sheet

Output:
  - data/processed/monthly_channel_metrics.csv

Run this after the monthly Studio export lands, then rerun the forecast notebook.
"""
import os
import pandas as pd

RAW = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
PROC = os.path.join(os.path.dirname(__file__), "..", "data", "processed")


def load():
    daily = pd.read_csv(os.path.join(RAW, "channel_stats_daily.csv"), parse_dates=["date"])
    studio = pd.read_csv(os.path.join(RAW, "studio_export_2026-05.csv"))
    spon = pd.read_csv(os.path.join(RAW, "sponsorships.csv"))
    return daily, studio, spon


def monthly_channel_metrics():
    daily, studio, spon = load()

    daily["month"] = daily["date"].dt.to_period("M").astype(str)

    # roll the daily pull up to month x channel
    agg = (
        daily.groupby(["channel_id", "month"])
        .agg(
            monthly_views=("views", "sum"),
            subscribers=("subscribers", "sum"),
            minutes_watched=("estimated_minutes_watched", "sum"),
        )
        .reset_index()
    )

    # bring in ad revenue from the Studio export
    studio = studio.rename(columns={"estimated_partner_revenue_usd": "ad_revenue"})
    df = agg.merge(
        studio[["channel_id", "month", "ad_revenue"]],
        on=["channel_id", "month"],
        how="inner",
    )

    # revenue per mille — what the channel earns per 1k views
    df["rpm_usd"] = df["ad_revenue"] / df["monthly_views"] * 1000

    # add sponsorship money. the sheet is keyed by channel name, so map names -> ids.
    name_to_id = (
        studio.drop_duplicates("channel_id")
        .set_index("channel_title")["channel_id"]
        .to_dict()
    )
    spon = spon.copy()
    spon["channel"] = spon["channel"].str.strip()
    spon["channel_id"] = spon["channel"].map(name_to_id)
    spon["gross_amount_usd"] = pd.to_numeric(spon["gross_amount_usd"], errors="coerce")

    df = df.merge(
        spon[["channel_id", "month", "gross_amount_usd"]],
        on=["channel_id", "month"],
        how="left",
    )
    df["sponsor_revenue"] = df["gross_amount_usd"].fillna(0)
    df["total_revenue"] = df["ad_revenue"] + df["sponsor_revenue"]

    out = df[[
        "channel_id", "month", "monthly_views", "subscribers",
        "ad_revenue", "rpm_usd", "sponsor_revenue", "total_revenue",
    ]]
    return out


def main():
    out = monthly_channel_metrics()
    path = os.path.join(PROC, "monthly_channel_metrics.csv")
    out.to_csv(path, index=False)
    print(f"wrote {len(out)} rows -> {path}")
    print(f"company total revenue (all months): ${out['total_revenue'].sum():,.0f}")


if __name__ == "__main__":
    main()
