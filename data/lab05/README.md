# Lab 5 · Link Three Sources Without a Shared Identifier (Week 6)

Three files describe overlapping groups of Puente County residents. Each comes from a different system, and no identifier is shared between them.

- `ehr.csv`: the patient list of a clinic network's electronic health record.
- `lab.csv`: person details taken from laboratory reports.
- `imm.csv`: person records from the county immunization registry.

`truth_key.csv` names the real person behind every record. Use it only to evaluate your links (precision and recall, overall and by group), never as an input to blocking or matching. Each person has at most one record in each file.

| File | One row is | Rows |
|---|---|---|
| `ehr.csv` | an EHR patient | 16,327 |
| `lab.csv` | a person on a laboratory report | 4,812 |
| `imm.csv` | an immunization registry person | 17,402 |
| `truth_key.csv` | a record and the person behind it | 38,541 |

## Load

Splink 5 runs on DuckDB in the notebook. Install it first: `!pip install -q splink==5.0.0`.

```python
import pandas as pd
ehr = pd.read_csv(COURSE_URL + "lab05/ehr.csv", dtype=str)
lab = pd.read_csv(COURSE_URL + "lab05/lab.csv", dtype=str)
imm = pd.read_csv(COURSE_URL + "lab05/imm.csv", dtype=str)
truth = pd.read_csv(COURSE_URL + "lab05/truth_key.csv", dtype=str)
```

Each source keeps its own conventions. Read everything as text and standardize before you compare.

## Data dictionary

### `ehr.csv` (16,327 rows) · one row per EHR patient

| Column | Type | Description |
|---|---|---|
| `rec_id` | text | Record identifier, unique within the file |
| `first_name` | text | Upper case |
| `middle_initial` | text | Blank if none |
| `last_name` | text | Upper case |
| `birth_date` | text | `YYYY-MM-DD` |
| `sex` | text | `F` or `M` |
| `street` | text | Current address |
| `zip` | text | |
| `phone` | text | Ten digits; blank if none |
| `race` | text | One or more races, separated by `;` |
| `ethnicity` | text | `Hispanic or Latino` or `Not Hispanic or Latino` |

### `lab.csv` (4,812 rows) · one row per person on a laboratory report

| Column | Type | Description |
|---|---|---|
| `rec_id` | text | Record identifier, unique within the file |
| `first_name` | text | As entered at the laboratory |
| `last_name` | text | As entered at the laboratory |
| `birth_date` | text | `MM/DD/YYYY` |
| `sex` | text | `F`, `M`, or `U` |
| `street` | text | Blank if not on the report |
| `zip` | text | |

### `imm.csv` (17,402 rows) · one row per registry person

| Column | Type | Description |
|---|---|---|
| `rec_id` | text | Record identifier, unique within the file |
| `first_name` | text | Given name or names, upper case |
| `last_name` | text | Upper case |
| `birth_date` | text | `YYYYMMDD` |
| `sex` | text | `F` or `M` |
| `street` | text | Address on file at the registry |
| `zip` | text | |

### `truth_key.csv` (38,541 rows) · one row per record in the three files

| Column | Type | Description |
|---|---|---|
| `source` | text | `ehr`, `lab`, or `imm` |
| `rec_id` | text | Joins to `rec_id` in that source |
| `person_key` | text | The real person; records with the same `person_key` belong together |
| `race_ethnicity` | text | The person's group, for evaluating results by group: `Hispanic or Latino`, `White`, `Black`, `Asian or Pacific Islander`, or `Multiracial or other` |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
