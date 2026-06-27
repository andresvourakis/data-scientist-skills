# Claude Code Skills for Data Scientists

Three Claude Code skills a senior data scientist uses to ship work with confidence. Each one closes a different confidence gap, before a stakeholder ever sees the work.

- **feasibility-check** : before you commit to building
- **analyst-peer-reviewer** : before you trust the numbers
- **present-analysis** : before a stakeholder sees it

## Install

Either one installs all three skills.

**As a plugin (supports updates):**

```text
/plugin marketplace add andresvourakis/data-scientist-skills
/plugin install data-scientist-skills@andres-vourakis
```

**Manual:**

```bash
git clone https://github.com/andresvourakis/data-scientist-skills
cp -R data-scientist-skills/skills/* ~/.claude/skills/
```

Then call any skill by its slash command, for example `/feasibility-check`. Claude also reaches for them on its own when the task fits.

## Where they fit

Most AI tooling lives in the middle of the analytics lifecycle, where you crunch the data. The judgment that decides whether work lands lives at the edges. These three sit there:

```
Stakeholder ask -> PLAN -> ANALYZE -> COMMUNICATE -> Decision
                    |         |            |
              feasibility   peer-       present-
                -check     reviewer     analysis
```

## The three skills

### feasibility-check

A stakeholder asks for a model, a forecast, a new feature, a more granular cut of a system you already run, and your gut says "sure, about a week." Before you commit, this pressure-tests the ask against the system it would plug into and tells you what is already there, what you would have to build, and the one unknown to resolve before you promise a date.

```
THE CALL
Verdict: Check first. Weekly views and subs are nearly free, but weekly revenue does
not exist in the system today, so there is no honest date to give yet.
The big unknown: can the API return revenue at day grain? If not, weekly revenue has to
be modeled, not measured. Check this before you promise anything.

THE BREAKDOWN
| Piece of the work               | Status    | Effort | Note                                    |
| Weekly views / subs per channel | ✓ have it | hrs    | daily pull, reaggregate to weekly       |
| Revenue at weekly grain         | ⚠ unknown | ?      | the big unknown: API may only give monthly |
| Replace the manual export       | ⛔ can't  | -      | no revenue API on this plan, hand-exported monthly |

NEXT
(1h) Pull revenue for one channel at day grain from the API. If it returns data, weekly
is days of work. If not, the honest answer is monthly, or a clearly labeled estimate.
```

### analyst-peer-reviewer

Your code runs, the numbers look clean, you are about to hit send. This is the senior colleague who stops you and asks the uncomfortable question: are you sure this answers what they actually asked? It catches the bug that survives a clean run, and the analysis that is technically correct but will walk a stakeholder straight to the wrong decision. A linter checks your syntax. This checks your judgment.

```
Bottom Line
Verdict: Think on it. The math checks out, but the story does not. The forecast
equal-weights every channel and leans on a month YouTube has not finalized, so it
reads healthier and steadier than reality.

What I'd Look At
1. [Framing gap] revenue_model.ipynb:84 averages per-channel growth equally, so two
   tiny channels swing the whole portfolio number. Leadership reads it as broad growth.
2. [Blind spot] the base month (May) is not finalized by YouTube yet, so the dip is a
   partial-data artifact, not a trend, and someone will react to it.

What's Solid
The daily-to-monthly aggregation and per-channel keys are correct. This is about
interpretation, not broken numbers.

One Question to Sit With
If the board asks whether growth is broad or driven by a few channels, does this
forecast answer that, or does equal-weighting quietly hide it?
```

### present-analysis

You did the work and it is right, but it lands as a wall of charts and the person who has to decide cannot find the answer. You give this the question the analysis answers, and it writes one report that works for three readers at once: the one who just wants the decision, the skeptic who wants the charts to back it, and the analyst who reads every line. It pulls the charts that support each takeaway, never invents a number that is not already in your work, and flags what you should fix before you share it.

```
# Objective
What is our revenue outlook for the next 12 months, and which channels drive it?

# Key Takeaways
- Revenue is on track to grow **about 22% over the next 12 months**.
- **Two channels drive most of it:** Wattage and Penny & Plan are ~60% of the gain.
- Growth flattens after month four, so the **second half is conservative**, not a ceiling.

# Recommendations
- Put incremental budget behind the two channels carrying the forecast.
- Treat the back-half numbers as a floor, and revisit once the forecast is refreshed.

# Analysis
For the full analysis, see the notebook.

## Two channels account for ~60% of projected revenue growth
![revenue by channel](charts/revenue_by_channel.png)
Observations
- The rest of the portfolio is roughly flat, so the upside is concentrated, not broad.
- The same two channels carry the highest revenue per view, which compounds the effect.
```

## Try them on the playground

`playground/channel-growth-forecast` is a realistic, deliberately flawed project: a media company forecasting revenue across its channels. It runs, and it is wrong in the ways real projects are wrong.

```bash
cd data-scientist-skills/playground/channel-growth-forecast

/feasibility-check Scope making the revenue forecast weekly instead of monthly, per channel.
/analyst-peer-reviewer src/metrics.py notebooks/02_revenue_model.ipynb
```

## Why these exist

Faster has a ceiling. Using AI to do the same work faster was the right first step. The next step is using it to do the work better: work that holds up, gets used, and earns trust. These skills put that judgment into the workflow.

## How skills work

A skill is a folder with a `SKILL.md` file: instructions Claude loads when you invoke it. Docs: https://code.claude.com/docs/en/skills

## License and credits

MIT, see [LICENSE](LICENSE). Use them, fork them, adapt them.

Built by [Andres Vourakis](https://github.com/andresvourakis).
