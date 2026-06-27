# scratch notes (mine, not for the deck)

Running log of stuff I need to remember about this pipeline. Half of this should
be in the README but no time.

## monthly process (what I actually do)
- 3rd-ish of the month: log into YouTube Studio, go to each channel's Analytics,
  Revenue tab, export the month. Dump them into one csv -> studio_export_YYYY-MM.csv.
  This is ~40 min of clicking. There is no API for the $ numbers on our plan.
- then `python src/metrics.py`
- then rerun 02_revenue_model.ipynb, export outputs/forecast.csv
- paste the channel totals into the exec sheet

## things that bite me every month
- **YT doesn't finalize revenue until ~mid the following month.** So the latest
  month in studio_export is always partial/low. May numbers right now are maybe
  ~70% of what they'll settle at. I keep forgetting and the forecast dips.
- sponsorship sheet is a MESS. Finance keys it by channel name, typed by hand, so
  "Night Shift Sci" / "Night Shift Science" / "NightShift Sci" are all in there.
  Some deals have no amount yet (not invoiced). I keep meaning to clean this.
- the processed/ snapshot is stale — I think I last rebuilt it end of April. Need
  to rerun metrics.py before anyone trusts it.

## TODO (someday)
- [ ] add **Curio Cart** and **Slow Roads** to the pull. They launched (Apr/May)
      and they're in the roster but the cron list doesn't have them yet, so they're
      invisible in every report. Curio is growing fast, exec will ask.
- [ ] neither new channel is monetized yet so no Studio revenue for them anyway
- [ ] the subscriber column in the monthly table looks way too big, never dug in
- [ ] sanity check RPM — mine come out lower than what Studio shows as CPM, prob fine?

## !!! exec ask from last review (2026-06-15)
Diego wants the revenue forecast **weekly instead of monthly**, broken out by
channel, "so we can react faster." Said I'd scope it. Need to figure out if that's
even doable before I promise a date. <-- this is the thing to feasibility-check
