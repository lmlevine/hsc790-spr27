# Lab 3 · Write a Phenotype, Then Find Out How Wrong It Is (Week 4)

An extract from the Puente County Health Services (PCHS) electronic health record for a random sample of 16,000 adult PCHS patients, January 1, 2024 through December 31, 2026, in a simplified Synthea-style layout: patients, encounters, conditions, observations, and medications. PCHS runs one hospital, Puente County Medical Center (facility 1), and 11 clinics (facilities 11 to 21) on this EHR, so the extract holds what happened at those sites only.

`reference_standard.csv` is a chart review of a random sample of 4,000 of these patients. A reviewer read each chart and recorded `truth = True` when type 2 diabetes was documented by December 31, 2026, either as a diagnosis or as a hemoglobin A1c of 6.5% or higher on any test; patients with type 1 diabetes are `False`. Treat it as a reference standard: careful, not infallible.

Lab 9 (Week 10) uses these same tables with `lab09/program_enrollment.csv`.

| File | One row is | Rows |
|---|---|---|
| `patients.csv` | a patient | 16,000 |
| `encounters.csv.gz` | a clinic visit, emergency visit, or hospital stay | 74,077 |
| `conditions.csv.gz` | a diagnosis recorded at an encounter | 88,929 |
| `observations.csv.gz` | a measurement or test result recorded at an encounter | 56,590 |
| `medications.csv.gz` | a prescription or renewal | 102,425 |
| `facilities.csv` | a PCHS site | 12 |
| `reference_standard.csv` | a chart-review label | 4,000 |

## Load

```python
import pandas as pd
T = {t: pd.read_csv(COURSE_URL + f"lab03/{t}", dtype={"zip": str})
     for t in ["patients.csv", "encounters.csv.gz", "conditions.csv.gz", "observations.csv.gz",
               "medications.csv.gz", "facilities.csv", "reference_standard.csv"]}
```

## Data dictionary

### `patients.csv` (16,000 rows) · one row per patient

| Column | Type | Description |
|---|---|---|
| `patient_id` | integer | Identifier in this extract (and in Lab 9) |
| `birth_date` | date | |
| `sex` | text | `F` or `M` |
| `race` | text | One or more races, separated by `;` |
| `ethnicity` | text | `Hispanic or Latino` or `Not Hispanic or Latino` |
| `language` | text | Preferred language |
| `zip` | text | |
| `clinic_id` | integer | The PCHS clinic where the patient is assigned for primary care; joins to `facilities.csv` |
| `insurance` | text | `Commercial`, `Medi-Cal`, `Medicare`, `Medicare-Medi-Cal`, or `Uninsured` |
| `first_seen` | date | Start of the patient's time as an active PCHS patient within the extract (January 1, 2024 if already a patient) |
| `last_seen` | date | End of that time (December 31, 2026 if still a patient) |

### `encounters.csv.gz` (74,077 rows) · one row per encounter

| Column | Type | Description |
|---|---|---|
| `encounter_id` | integer | |
| `patient_id` | integer | |
| `facility_id` | integer | Joins to `facilities.csv` |
| `encounter_date` | date | |
| `end_date` | date | Same as `encounter_date` except for inpatient stays |
| `encounter_class` | text | `ambulatory` (clinic visit), `emergency`, or `inpatient` |

### `conditions.csv.gz` (88,929 rows) · one row per diagnosis recorded at an encounter

| Column | Type | Description |
|---|---|---|
| `patient_id` | integer | |
| `encounter_id` | integer | Encounter at which the diagnosis was recorded |
| `onset_date` | date | Date it was recorded (the encounter date) |
| `code` | text | Diagnosis code |
| `system` | text | Code system |
| `description` | text | |

### `observations.csv.gz` (56,590 rows) · one row per observation

| Column | Type | Description |
|---|---|---|
| `patient_id` | integer | |
| `encounter_id` | integer | Encounter at which it was recorded |
| `obs_date` | date | |
| `code` | text | Observation code |
| `system` | text | Code system of `code`, as recorded by the EHR |
| `description` | text | |
| `value` | decimal | |
| `units` | text | |

### `medications.csv.gz` (102,425 rows) · one row per prescription or renewal

| Column | Type | Description |
|---|---|---|
| `patient_id` | integer | |
| `encounter_id` | integer | Most recent clinic visit on or before `start_date`; blank if none in the extract |
| `start_date` | date | |
| `stop_date` | date | End of the supply prescribed |
| `code` | text | Medication code |
| `system` | text | Code system |
| `description` | text | Medication name |

### `facilities.csv` (12 rows) · one row per PCHS site

| Column | Type | Description |
|---|---|---|
| `facility_id` | integer | Same numbering as `commons/facilities.csv` |
| `facility_name` | text | |
| `facility_type` | text | `hospital` or `clinic` |
| `zip` | text | |
| `city` | text | |

### `reference_standard.csv` (4,000 rows) · one row per reviewed patient

| Column | Type | Description |
|---|---|---|
| `patient_id` | integer | Joins to `patients.csv` |
| `clinic_id` | integer | The patient's assigned clinic |
| `truth` | boolean | Chart review found type 2 diabetes (see above) |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
