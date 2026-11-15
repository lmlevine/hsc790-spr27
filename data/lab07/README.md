# Lab 7 · Nowcast the Right Edge, Then Publish Safely (Week 8)

`covid_cases.csv` is the COVID-19 case registry as it stood at 11:59 PM on March 31, 2026: every report received by then for cases whose illness began on or after June 1, 2025. Reports keep arriving after a case's onset, so the most recent weeks are incomplete. Onset is unknown for some cases.

The population tables are the denominators for a small-area table by ZIP code and race and ethnicity. `suppression_checker.py` attacks a table you intend to publish the way a reader could, by subtracting from the published totals, and reports any suppressed cell it can recover or narrow down.

`wastewater.csv` is a synthetic wastewater series from the county's two monitored treatment plants, for an optional overlay. It is not real monitoring data.

| File | One row is | Rows |
|---|---|---|
| `covid_cases.csv` | a case | 7,280 |
| `population_by_zip_group.csv` | a ZIP code and group | 135 |
| `zip_codes.csv` | a ZIP code | 27 |
| `wastewater.csv` | a sample | 174 |
| `suppression_checker.py` | the checker | |

## Load

```python
import pandas as pd
cases = pd.read_csv(COURSE_URL + "lab07/covid_cases.csv", dtype={"zip": str},
                    parse_dates=["onset_date", "specimen_date", "report_date", "received_ts"])

import urllib.request
urllib.request.urlretrieve(COURSE_URL + "lab07/suppression_checker.py", "suppression_checker.py")
from suppression_checker import check
```

`check(table)` expects the table you intend to publish: one row per ZIP code, one column per group, a `Total` column, and a final `Total` row, with `*` in every suppressed cell. The first column holds the ZIP codes. It returns a dictionary: `passed`, `hidden_cells`, the cells it `recovered` exactly, the cells whose possible range is narrower than the threshold of 11 (`narrow_ranges`), and every range it found (`ranges`). The docstring at the top of the file has the details.

## Data dictionary

### `covid_cases.csv` (7,280 rows) · one row per case

| Column | Type | Description |
|---|---|---|
| `case_id` | integer | |
| `onset_date` | date | Date symptoms began; blank if unknown |
| `specimen_date` | date | Date the specimen was collected |
| `report_date` | date | Date on the report |
| `received_ts` | timestamp | When the registry received the report |
| `zip` | text | |
| `age_group` | text | `0-17`, `18-44`, `45-64`, or `65+` |
| `sex` | text | `F` or `M` |
| `race_ethnicity` | text | `Latino`, `White`, `Asian/Pacific Islander`, `Black`, or `Multiracial/other` |
| `reporting_facility_id` | integer | Who reported; same numbering as `commons/facilities.csv` |
| `case_status` | text | `confirmed` or `probable` |

### `population_by_zip_group.csv` (135 rows) · one row per ZIP code and group

| Column | Type | Description |
|---|---|---|
| `zip` | text | |
| `race_ethnicity` | text | Same groups as `covid_cases.csv` |
| `population` | integer | Residents |

### `zip_codes.csv` (27 rows) · one row per ZIP code

| Column | Type | Description |
|---|---|---|
| `zip` | text | |
| `city` | text | |
| `region` | text | `Basin`, `Corridor`, or `Foothills` |
| `population_2025` | integer | Residents |

### `wastewater.csv` (174 rows) · one row per sample (Mondays and Thursdays)

| Column | Type | Description |
|---|---|---|
| `sewershed` | text | Treatment plant: `BASIN` or `CORRIDOR` (see `commons/zip_codes.csv` for the ZIP codes each serves) |
| `sample_date` | date | |
| `population_served` | integer | Residents in the sewershed |
| `sars_cov2_gc_per_l` | decimal | SARS-CoV-2 RNA, gene copies per liter |
| `pmmov_gc_per_l` | decimal | Pepper mild mottle virus RNA, gene copies per liter, a marker of fecal strength used to normalize |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
