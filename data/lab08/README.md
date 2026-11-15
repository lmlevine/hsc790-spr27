# Lab 8 · Break a "De-identified" Release, Then Repair It (Week 9)

`discharge_release.csv` is a file of 2025 hospital stays for residents of the Foothills (ZIP codes 95301 to 95305 and 95401), released with names, addresses, and record numbers removed. `voter_roster.csv` is a voter-style list for the same ZIP codes, of the kind anyone can request. Both, and every person in them, are synthetic: the point is to measure the risk of a release you might be responsible for, using people who do not exist.

Measure how identifiable the release is, link it to the roster, apply protections, and measure what the protections cost. `reference_rates.csv` is the utility benchmark: discharge rates by ZIP code and age group from the full, unprotected release. Compare it with the same rates from your protected version.

| File | One row is | Rows |
|---|---|---|
| `discharge_release.csv` | a hospital stay | 14,660 |
| `voter_roster.csv` | a registered voter | 55,682 |
| `population_by_zip_age_sex.csv` | a ZIP code, age group, and sex | 60 |
| `reference_rates.csv` | a ZIP code and age group | 30 |

## Load

```python
import pandas as pd
rel = pd.read_csv(COURSE_URL + "lab08/discharge_release.csv", dtype={"zip": str})
roster = pd.read_csv(COURSE_URL + "lab08/voter_roster.csv", dtype={"zip": str})
```

## Data dictionary

### `discharge_release.csv` (14,660 rows) · one row per stay

| Column | Type | Description |
|---|---|---|
| `record_id` | integer | Row number in the release |
| `zip` | text | Patient's five-digit ZIP code |
| `birth_date` | date | |
| `sex` | text | `F` or `M` |
| `race_ethnicity` | text | `Latino`, `White`, `Asian/Pacific Islander`, `Black`, or `Multiracial/other` |
| `admit_date` | date | |
| `discharge_date` | date | |
| `length_of_stay` | integer | Days |
| `principal_dx` | text | ICD-10-CM code of the principal diagnosis |
| `dx_description` | text | |
| `hospital_id` | integer | Same numbering as `commons/facilities.csv` |

### `voter_roster.csv` (55,682 rows) · one row per voter

| Column | Type | Description |
|---|---|---|
| `voter_id` | integer | |
| `last_name` | text | |
| `first_name` | text | |
| `middle_initial` | text | Blank if none |
| `street` | text | |
| `city` | text | |
| `zip` | text | |
| `birth_date` | date | |
| `sex` | text | `F` or `M` |
| `registration_date` | date | |

### `population_by_zip_age_sex.csv` (60 rows) · one row per ZIP code, age group, and sex

| Column | Type | Description |
|---|---|---|
| `zip` | text | |
| `age_group` | text | `0-4`, `5-17`, `18-44`, `45-64`, or `65+` |
| `sex` | text | `F` or `M` |
| `population` | integer | Residents |

### `reference_rates.csv` (30 rows) · one row per ZIP code and age group

| Column | Type | Description |
|---|---|---|
| `zip` | text | |
| `age_group` | text | Age on July 1, 2025 |
| `discharges` | integer | Stays in the full release |
| `population` | integer | Residents |
| `rate_per_1000` | decimal | `1000 × discharges / population` |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
