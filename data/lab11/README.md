# Lab 11 · Build the Harness Before You Trust the Model (Week 12)

Three hundred free-text case-report narratives, the kind an investigator writes after interviewing a patient, in English and Spanish. The task: extract four fields from each report and triage it.

| Field | Values |
|---|---|
| `hospitalized` | `yes`, `no`, or `unknown` |
| `onset_date` | `YYYY-MM-DD`, or `unknown` |
| `occupation` | `food_handler`, `health_care`, `child_care`, `other`, or `unknown` |
| `priority` | `urgent` or `routine` |

`annotation_guide.md` gives the rules the human reviewers followed. `gold_labels.csv` holds the adjudicated labels for all 300 reports, and `annotator2_labels.csv` a second reviewer's independent labels for 100 of them, for measuring agreement.

**The model outputs are recorded and simulated.** `model_outputs_v1.jsonl` and `model_outputs_v2.jsonl` were written by a program built to behave like two versions of a language-model extractor. No real model produced them. They let everyone score the same outputs, before and alongside any live model the class uses. `model_outputs_v1_rerun.jsonl` is version 1 run again on 50 of the reports.

Each output's `raw_output` is the text the "model" returned. It is supposed to be one JSON object with the four fields and an `evidence` object quoting the report for each field, like this:

```json
{"hospitalized": "no", "onset_date": "unknown", "occupation": "other", "priority": "routine",
 "evidence": {"hospitalized": "An ED visit on the second day ended in discharge the same evening",
              "onset_date": "", "occupation": "The patient works as a delivery driver", "priority": ""}}
```

Validate every output before you use it. If you call a model yourself, ask for the same shape so the same harness scores it.

| File | One row is | Rows |
|---|---|---|
| `case_narratives.csv` | a report | 300 |
| `gold_labels.csv` | a report's adjudicated labels | 300 |
| `annotator2_labels.csv` | a report's second-reviewer labels | 100 |
| `model_outputs_v1.jsonl` | a version 1 output (one JSON object per line) | 300 |
| `model_outputs_v2.jsonl` | a version 2 output | 300 |
| `model_outputs_v1_rerun.jsonl` | a version 1 output from a second run | 50 |
| `annotation_guide.md` | the reviewers' rules | |

## Load

```python
import json, pandas as pd, requests
reports = pd.read_csv(COURSE_URL + "lab11/case_narratives.csv")
gold = pd.read_csv(COURSE_URL + "lab11/gold_labels.csv", dtype=str)
v1 = [json.loads(line) for line in requests.get(COURSE_URL + "lab11/model_outputs_v1.jsonl").text.splitlines()]
```

## Data dictionary

### `case_narratives.csv` (300 rows) · one row per report

| Column | Type | Description |
|---|---|---|
| `report_id` | text | `R0001` to `R0300` |
| `language` | text | `en` or `es` |
| `text` | text | The narrative |

### `gold_labels.csv` (300 rows) and `annotator2_labels.csv` (100 rows) · one row per report

| Column | Type | Description |
|---|---|---|
| `report_id` | text | Joins to `case_narratives.csv` |
| `hospitalized` | text | |
| `onset_date` | text | A date or `unknown` |
| `occupation` | text | |
| `priority` | text | |

### The `.jsonl` files · one JSON object per line

| Key | Description |
|---|---|
| `report_id` | Joins to `case_narratives.csv` |
| `model_version` | `v1` or `v2` |
| `run` | Rerun file only: the run number |
| `raw_output` | The text returned, as a string; parse it yourself |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
