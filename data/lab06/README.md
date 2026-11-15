# Lab 6 · Build a Detector and Measure How Often It Cries Wolf (Week 7)

A year (2025) of emergency department visits from the five Puente County hospitals that send data to the Department of Public Health's syndromic surveillance system, as the system received them: one row per visit, with the chief complaint as recorded at triage. Sagebrush Community Hospital (6) is not connected and has no rows.

`labeled_sample.csv` is a random sample of 4,000 of these visits, from every hospital and month, each labeled by a trained reviewer who read the chief complaint. Score your classifiers against it. The reviewers are careful but not perfect.

`outbreaks_2025.csv` lists the events the department investigated or declared in 2025, with the ZIP codes or regions affected and their dates. Score detection against it, and keep some events out of any threshold tuning so you can test on events you did not tune on.

| File | One row is | Rows |
|---|---|---|
| `ed_visits_2025.csv.gz` | an emergency department visit | 295,381 |
| `labeled_sample.csv` | a labeled visit | 4,000 |
| `outbreaks_2025.csv` | a known event | 8 |
| `daily_tmax_2025.csv` | a day | 365 |
| `hospitals.csv` | a hospital | 6 |

## Load

```python
import pandas as pd
ed = pd.read_csv(COURSE_URL + "lab06/ed_visits_2025.csv.gz", dtype={"zip": str}, parse_dates=["visit_ts"])
labeled = pd.read_csv(COURSE_URL + "lab06/labeled_sample.csv", parse_dates=["visit_ts"])
events = pd.read_csv(COURSE_URL + "lab06/outbreaks_2025.csv", parse_dates=["start_date", "end_date"])
```

## Data dictionary

### `ed_visits_2025.csv.gz` (295,381 rows) · one row per visit

| Column | Type | Description |
|---|---|---|
| `visit_id` | integer | |
| `hospital_id` | integer | Joins to `hospitals.csv` |
| `visit_ts` | timestamp | Arrival time |
| `age_group` | text | `0-4`, `5-17`, `18-44`, `45-64`, or `65+` |
| `sex` | text | `F` or `M` |
| `zip` | text | Patient's ZIP code |
| `cc` | text | Chief complaint |

### `labeled_sample.csv` (4,000 rows) · one row per labeled visit

| Column | Type | Description |
|---|---|---|
| `visit_id` | integer | Joins to `ed_visits_2025.csv.gz` |
| `hospital_id` | integer | |
| `visit_ts` | timestamp | |
| `cc` | text | Chief complaint, as in the visit file |
| `syndrome` | text | Reviewer's label: `ili` (influenza-like illness), `gi` (gastrointestinal illness), `heat` (heat-related illness), or `none` |

### `outbreaks_2025.csv` (8 rows) · one row per known event

| Column | Type | Description |
|---|---|---|
| `outbreak_id` | text | |
| `syndrome` | text | `ili`, `gi`, or `heat` |
| `zip_codes` | text | ZIP codes affected, separated by `;`; region names for a regional event; `all` for the whole county |
| `start_date` | date | First day of the event |
| `end_date` | date | Last day of the event |
| `scope` | text | `local`, `regional`, or `county` |
| `description` | text | |

### `daily_tmax_2025.csv` (365 rows) · one row per day

| Column | Type | Description |
|---|---|---|
| `date` | date | |
| `tmax_basin_f` | integer | Daily high temperature in the Basin, °F |
| `tmax_corridor_f` | integer | Daily high in the Corridor, °F |
| `tmax_foothills_f` | integer | Daily high in the Foothills, °F |

### `hospitals.csv` (6 rows) · one row per hospital

| Column | Type | Description |
|---|---|---|
| `hospital_id` | integer | Same numbering as `commons/facilities.csv` |
| `facility_name` | text | |
| `system` | text | |
| `zip` | text | |
| `city` | text | |
| `syndromic_connected` | boolean | Sends data to syndromic surveillance |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
