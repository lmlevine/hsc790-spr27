# Lab 1 · Build a Reportable-Disease Registry (Week 2)

`raw_reports.csv` is every case report the Puente County Department of Public Health received from January 1 through March 31, 2026, exported from its intake system as one wide table. Each row is one report, with the patient's details and the reporting facility's details written out in full on that row. Your job is to turn it into a normalized registry with keys, constraints, and a data dictionary.

| File | One row is | Rows |
|---|---|---|
| `raw_reports.csv` | a case report as received | 2,555 |

## Load

```python
import duckdb
con = duckdb.connect()
con.sql(f"CREATE TABLE raw_reports AS SELECT * FROM read_csv_auto('{COURSE_URL}lab01/raw_reports.csv')")
```

## Data dictionary

### `raw_reports.csv` (2,555 rows) · one row per report

| Column | Type | Description |
|---|---|---|
| `case_id` | integer | Identifier of the report |
| `patient_id` | integer | Person identifier assigned by the intake system |
| `last_name` | text | |
| `first_name` | text | |
| `birth_date` | date | |
| `sex` | text | `F`, `M`, or `U` (unknown) |
| `race` | text | As sent by the reporter; more than one race is separated by `;`; blank if not sent |
| `ethnicity` | text | As sent; blank if not sent |
| `street_address` | text | Patient's address on the report |
| `city` | text | |
| `zip` | text | |
| `phone` | text | Blank if not sent |
| `facility_id` | integer | Reporting facility (the same numbering as `commons/facilities.csv`) |
| `facility_name` | text | Reporting facility's name, as sent |
| `facility_type` | text | `hospital`, `laboratory`, or `public_health_lab` |
| `clia_number` | text | Reporting facility's CLIA number |
| `condition_code` | text | |
| `condition_name` | text | |
| `onset_date` | date | Date symptoms began; blank if unknown |
| `specimen_date` | date | Date the specimen was collected |
| `result_date` | date | Date of the laboratory result |
| `report_date` | date | Date on the report |
| `case_status` | text | Case classification, as sent |
| `test_code` | text | LOINC code of the reported test; blank if the report names no test |
| `test_name` | text | Name of the test, as sent |
| `result_value` | text | Result, as sent |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
