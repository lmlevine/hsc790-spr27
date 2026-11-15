# Data commons · Lab 0 and the semester project

A linked sample of Puente County residents and their records from January 1, 2024 through December 31, 2026: 45,436 people, a simple random sample of about 1 in 20 residents (sampling fraction 0.05). Every table here covers the same people, so `patient_id` joins across all of them.

Counts in these tables are about one-twentieth of county totals. Multiply by 20 to estimate a county count, or divide `zip_codes.population_2025` by 20 to get denominators that match the sample.

| File | One row is | Rows |
|---|---|---|
| `patients.csv` | a resident in the sample | 45,436 |
| `encounters.csv` | a clinic visit, emergency department visit, or hospital stay | 90,682 |
| `lab_results.csv` | a test result | 41,451 |
| `case_reports.csv` | a reportable-disease case report | 2,847 |
| `immunizations.csv` | a vaccine dose | 120,879 |
| `ed_visits.csv` | an emergency department visit sent to syndromic surveillance | 42,345 |
| `facilities.csv` | a hospital, clinic, laboratory, pharmacy, or other site | 47 |
| `zip_codes.csv` | a ZIP code | 27 |
| `conditions.csv` | a reportable condition | 17 |

## What each table covers

- **Encounters.** Clinic visits are PCHS and Lucero visits only; other doctors' offices are not in the commons. Emergency visits and hospital stays cover all six hospitals. An emergency visit that ends in admission appears twice: once as the emergency encounter and once as the inpatient stay that starts the same day.
- **ED visits.** The syndromic surveillance feed, which comes from the five connected hospitals (`facilities.syndromic_connected`). These are the same visits as the emergency encounters at those hospitals, under a different identifier, with the chief complaint added.
- **Lab results.** Not every test a resident had: hemoglobin A1c from PCHS and Lucero clinic visits; the positive results behind laboratory-confirmed case reports; negative results for COVID-19, chlamydia, hepatitis C, and pertussis tests; influenza A tests; and blood lead screening for young children on Medi-Cal.
- **Case reports.** Every report of a reportable condition, including COVID-19, received by the Department of Public Health.
- **Immunizations.** Doses recorded in the county immunization registry: childhood and adolescent series, seasonal influenza, COVID-19, and zoster.

## Load

```python
import duckdb
con = duckdb.connect()
for t in ["patients", "encounters", "lab_results", "case_reports", "immunizations", "ed_visits",
          "facilities", "zip_codes", "conditions"]:
    con.sql(f"CREATE TABLE {t} AS SELECT * FROM read_csv_auto('{COURSE_URL}commons/{t}.csv')")
```

In pandas, pass `dtype={"zip": str, "cvx_code": str}` where those columns appear.

## Data dictionary

### `patients.csv` (45,436 rows) · one row per resident in the sample

| Column | Type | Description |
|---|---|---|
| `patient_id` | integer | Identifier for the person in the commons |
| `first_name` | text | Given name, upper case |
| `middle_initial` | text | Blank if none |
| `last_name` | text | Family name, upper case; may hold two surnames |
| `birth_date` | date | |
| `sex` | text | `F` or `M` |
| `race` | text | One or more races, separated by `;`; blank if not recorded |
| `ethnicity` | text | `Hispanic or Latino` or `Not Hispanic or Latino`; blank if not recorded |
| `language` | text | Preferred language |
| `street` | text | Street address at the end of 2026 |
| `city` | text | |
| `zip` | text | Five-digit ZIP code; joins to `zip_codes.csv` |
| `phone` | text | Ten digits; blank if none on file |
| `insurance` | text | Main coverage: `Commercial`, `Medi-Cal`, `Medicare`, `Medicare-Medi-Cal`, or `Uninsured` |
| `pchs_patient` | boolean | Has a primary care home at Puente County Health Services |
| `lucero_patient` | boolean | Has a primary care home at Lucero Community Health Centers |

### `encounters.csv` (90,682 rows) · one row per visit or stay

| Column | Type | Description |
|---|---|---|
| `encounter_id` | integer | |
| `patient_id` | integer | Joins to `patients.csv` |
| `facility_id` | integer | Joins to `facilities.csv` |
| `encounter_type` | text | `outpatient` (PCHS or Lucero clinic visit), `emergency`, or `inpatient` |
| `start_date` | date | |
| `end_date` | date | Same as `start_date` except for inpatient stays |
| `primary_dx_code` | text | ICD-10-CM code of the main diagnosis |
| `primary_dx_description` | text | |

### `lab_results.csv` (41,451 rows) · one row per test result

| Column | Type | Description |
|---|---|---|
| `result_id` | integer | |
| `patient_id` | integer | Joins to `patients.csv` |
| `ordering_facility_id` | integer | Facility that ordered the test; joins to `facilities.csv` |
| `performing_lab_id` | integer | Laboratory that performed it; joins to `facilities.csv` |
| `loinc_code` | text | LOINC code of the test |
| `test_name` | text | LOINC long name |
| `specimen_date` | date | Date the specimen was collected |
| `result_date` | date | |
| `result_value` | text | `Detected`, `Not detected`, `Reactive`, `Nonreactive`, an organism as `SNOMED CT code^name`, or a number |
| `result_unit` | text | Unit of a numeric result (`%` or `ug/dL`); blank otherwise |
| `interpretation` | text | `positive`, `negative`, `normal`, or `abnormal` |

### `case_reports.csv` (2,847 rows) · one row per case report

| Column | Type | Description |
|---|---|---|
| `case_id` | integer | |
| `patient_id` | integer | Joins to `patients.csv` |
| `condition` | text | Condition code; joins to `conditions.condition_code` |
| `onset_date` | date | Date symptoms began; blank if unknown or not applicable |
| `specimen_date` | date | Date the diagnostic specimen was collected |
| `result_date` | date | Date the laboratory result was final |
| `report_date` | date | Date the reporter sent the report |
| `received_ts` | timestamp | When the Department of Public Health received it |
| `reporting_facility_id` | integer | Who reported it; joins to `facilities.csv` |
| `case_status` | text | `confirmed`, `probable`, `suspect`, or `not_a_case` |

### `immunizations.csv` (120,879 rows) · one row per dose

| Column | Type | Description |
|---|---|---|
| `dose_id` | integer | |
| `patient_id` | integer | Joins to `patients.csv` |
| `cvx_code` | text | CVX vaccine code; read as text to keep leading zeros (`03`, `08`) |
| `vaccine_name` | text | |
| `admin_date` | date | Date the dose was given |
| `facility_id` | integer | Where it was given; joins to `facilities.csv` |

### `ed_visits.csv` (42,345 rows) · one row per emergency department visit in the syndromic feed

| Column | Type | Description |
|---|---|---|
| `visit_id` | integer | |
| `patient_id` | integer | Joins to `patients.csv` |
| `hospital_id` | integer | Joins to `facilities.facility_id` |
| `visit_ts` | timestamp | Arrival time |
| `age_group` | text | `0-4`, `5-17`, `18-44`, `45-64`, or `65+` |
| `sex` | text | `F` or `M` |
| `zip` | text | Patient's ZIP code |
| `chief_complaint` | text | Reason for the visit as recorded at triage |
| `discharge_dx_code` | text | ICD-10-CM code of the emergency department diagnosis |
| `disposition` | text | `discharged`, `admitted`, `transferred`, or `left without being seen` |

### `facilities.csv` (47 rows) · one row per site

| Column | Type | Description |
|---|---|---|
| `facility_id` | integer | |
| `facility_name` | text | |
| `facility_type` | text | `hospital`, `laboratory`, `public_health_lab`, `clinic`, `school_clinic`, `mobile_clinic`, `dental`, `dph_clinic`, `physician_office`, `urgent_care`, or `pharmacy` |
| `system` | text | Owner: `PCHS`, `Lucero CHC`, `Cordillera Health`, `Sagebrush Health Partners`, `DPH`, `CareRx`, or `Independent` |
| `zip` | text | |
| `clia_number` | text | CLIA certificate number for sites that test specimens; blank otherwise |
| `has_ed` | boolean | Has an emergency department |
| `syndromic_connected` | boolean | Sends emergency department data to syndromic surveillance |
| `city` | text | |

### `zip_codes.csv` (27 rows) · one row per ZIP code

| Column | Type | Description |
|---|---|---|
| `zip` | text | |
| `zip3` | text | First three digits |
| `city` | text | |
| `region` | text | `Basin`, `Corridor`, or `Foothills` |
| `population_2025` | integer | Residents in 2025, for the whole county (not the sample) |
| `sewershed` | text | Wastewater treatment plant serving the ZIP code (`BASIN` or `CORRIDOR`); blank if no monitored plant serves it |

### `conditions.csv` (17 rows) · one row per reportable condition

| Column | Type | Description |
|---|---|---|
| `condition_code` | text | |
| `condition_name` | text | |
| `category` | text | `sti`, `hepatitis`, `enteric`, `respiratory`, `vaccine_preventable`, `fungal`, or `other` |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
