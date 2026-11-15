# Lab 12 · Did the Rollout Work? (Week 13)

Puente County phased in electronic case reporting (eCR), which sends case reports automatically from facilities' records, in place of faxed reports that staff entered by hand. Wave 1 facilities went live the week of June 30, 2025 (week 105). Wave 2 facilities had not started by the end of the series. The question for the county: expand eCR to Wave 2, pause, or stop?

`weekly.csv` is the registry's weekly monitoring series for each wave from the week of July 3, 2023 (week 1) through the week of June 22, 2026 (week 156): the main outcome, median days from diagnosis to report received, and three balancing measures. `timestamp_validation.csv` comes from a check done before go-live: for a sample of faxed reports from Wave 1 facilities in the 13 weeks before go-live, the time the fax arrived, taken from the fax server's log, and the time staff entered the report into the registry.

| File | One row is | Rows |
|---|---|---|
| `weekly.csv` | a wave and week | 312 |
| `timestamp_validation.csv` | a faxed report | 234 |

## Load

```python
import pandas as pd
weekly = pd.read_csv(COURSE_URL + "lab12/weekly.csv", parse_dates=["week_start"])
val = pd.read_csv(COURSE_URL + "lab12/timestamp_validation.csv", parse_dates=["fax_received_ts", "entered_ts"])
```

## Data dictionary

### `weekly.csv` (312 rows) · one row per wave and week

| Column | Type | Description |
|---|---|---|
| `wave` | integer | `1` (went live in week 105) or `2` (not yet live) |
| `week` | integer | 1 to 156 |
| `week_start` | date | Monday of the week |
| `month` | integer | Calendar month of `week_start` |
| `n_reports` | integer | Case reports received that week |
| `median_days` | decimal | Median days from diagnosis to report received, for that week's reports, as recorded by the registry |
| `pct_electronic` | decimal | Percent of the week's reports received through eCR |
| `duplicates_per_100_cases` | decimal | Duplicate reports per 100 cases |
| `queue_length` | integer | Reports waiting for an investigator at the end of the week |
| `occupation_complete_pct` | decimal | Percent of reports with the occupation field filled in |

### `timestamp_validation.csv` (234 rows) · one row per sampled faxed report

| Column | Type | Description |
|---|---|---|
| `report_id` | text | |
| `wave` | integer | Always `1` |
| `fax_received_ts` | timestamp | When the fax arrived, from the fax server's log |
| `entered_ts` | timestamp | When staff entered the report into the registry |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
