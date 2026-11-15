# Lab 2 · Build a Pipeline That Checks Itself (Week 3)

Two monthly batches from the same intake system as Lab 1, in the same layout plus a `batch_id` column: `batch_1.csv` holds the reports received in April 2026 and `batch_2.csv` the reports received in May 2026. Run each through your staging tables, checks, quarantine, and load, and produce a quality report for each.

The reference code tables are the registry's lists of accepted values. `reference_schema.sql` is one defensible answer to Lab 1, in DuckDB. Use it if your own Lab 1 schema is incomplete; it is not the only good design.

| File | What it is | Rows |
|---|---|---|
| `batch_1.csv` | Reports received in April 2026 | 854 |
| `batch_2.csv` | Reports received in May 2026 | 920 |
| `ref_status.csv` | Accepted case status codes | 4 |
| `ref_condition.csv` | Accepted condition codes | 16 |
| `ref_race.csv` | CDC race category codes and their labels | 6 |
| `reference_schema.sql` | `CREATE TABLE` statements for a reference registry | |

## Load

```python
import duckdb, requests
con = duckdb.connect()
con.sql(requests.get(COURSE_URL + "lab02/reference_schema.sql").text)     # only if you use the reference schema
con.sql(f"CREATE TABLE stg_raw AS SELECT * FROM read_csv_auto('{COURSE_URL}lab02/batch_1.csv')")
```

## Data dictionary

### `batch_1.csv` (854 rows) and `batch_2.csv` (920 rows) · one row per report

The columns are those of `lab01/raw_reports.csv`, plus `batch_id`.

| Column | Type | Description |
|---|---|---|
| `case_id` | integer | Identifier of the report |
| `patient_id` | integer | Person identifier assigned by the intake system; a person keeps the same identifier across Lab 1 and both batches |
| `last_name` | text | |
| `first_name` | text | |
| `birth_date` | date | |
| `sex` | text | `F`, `M`, or `U` (unknown) |
| `race` | text | As sent; more than one race is separated by `;`; blank if not sent |
| `ethnicity` | text | As sent; blank if not sent |
| `street_address` | text | |
| `city` | text | |
| `zip` | text | |
| `phone` | text | Blank if not sent |
| `facility_id` | integer | Reporting facility |
| `facility_name` | text | Reporting facility's name, as sent |
| `facility_type` | text | `hospital`, `laboratory`, or `public_health_lab` |
| `clia_number` | text | |
| `condition_code` | text | |
| `condition_name` | text | |
| `onset_date` | date | Blank if unknown |
| `specimen_date` | date | |
| `result_date` | date | |
| `report_date` | date | |
| `case_status` | text | Case classification, as sent |
| `test_code` | text | LOINC code of the reported test; blank if none |
| `test_name` | text | |
| `result_value` | text | |
| `batch_id` | text | Identifier of the monthly batch |

### `ref_status.csv` (4 rows) · one row per accepted case status

| Column | Type | Description |
|---|---|---|
| `code` | text | Value expected in `case_status` |
| `label` | text | Display label |

### `ref_condition.csv` (16 rows) · one row per accepted condition

| Column | Type | Description |
|---|---|---|
| `condition_code` | text | |
| `condition_name` | text | |

### `ref_race.csv` (6 rows) · one row per race category

| Column | Type | Description |
|---|---|---|
| `code` | text | CDC Race and Ethnicity code |
| `label` | text | OMB race category |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
