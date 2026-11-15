# Lab 9 · Build a Cohort Someone Else Could Rebuild (Week 10)

Puente County Health Services runs a Diabetes Care Management Program: a care manager, regular outreach, and help with medicines and appointments for adults with type 2 diabetes. It began as a pilot taking referrals from hospital discharges in September 2024 and opened to referrals from primary care on January 1, 2025.

The question: among adults with type 2 diabetes, does enrolling in the program reduce emergency department visits within 12 months?

`program_enrollment.csv` lists every enrollment in the PCHS records. Everything else comes from the Lab 3 EHR extract in `lab03/`; `patient_id` is the same in both folders. Record the data snapshot (`data/SNAPSHOT.txt`) with your cohort.

| File | One row is | Rows |
|---|---|---|
| `program_enrollment.csv` | an enrolled patient | 674 |

## Load

```python
import pandas as pd
prog = pd.read_csv(COURSE_URL + "lab09/program_enrollment.csv", parse_dates=["enroll_date"])
pt = pd.read_csv(COURSE_URL + "lab03/patients.csv", parse_dates=["birth_date", "first_seen", "last_seen"])
enc = pd.read_csv(COURSE_URL + "lab03/encounters.csv.gz", parse_dates=["encounter_date", "end_date"])
```

## Data dictionary

### `program_enrollment.csv` (674 rows) · one row per enrolled patient

| Column | Type | Description |
|---|---|---|
| `patient_id` | integer | Joins to `lab03/patients.csv` |
| `enroll_date` | date | Date of the first program contact |
| `referral_source` | text | `primary care` or `hospital discharge` |

For the other tables, see `lab03/README.md`. Emergency department visits are the `emergency` encounters in `lab03/encounters.csv.gz`; like everything in that extract, they cover PCHS's own hospital only.

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
