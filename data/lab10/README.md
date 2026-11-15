# Lab 10 · Train Here, Validate There, Audit Everyone (Week 11)

Outreach staff can reach only a limited number of adults with type 2 diabetes each year, and want to reach those most likely to have an avoidable emergency visit in the next 12 months. Two sites share modeling tables built the same way: **Site A**, Puente County Health Services (PCHS), and **Site B**, Lucero Community Health Centers. Both cover adults with diagnosed type 2 diabetes.

Each row is one member at one prediction moment. Predictors summarize the 12 months before the moment; the two candidate labels, `avoidable_ed_12m` and `cost_12m`, describe the 12 months after it. Site A has two prediction moments (January 1, 2024 and January 1, 2025), so a member present at both has two rows; Site B has one (January 1, 2025).

Read the "When recorded" column before you choose predictors.

| File | One row is | Rows |
|---|---|---|
| `site_a.csv` | a PCHS member at a prediction moment | 21,927 |
| `site_b.csv` | a Lucero member at the prediction moment | 3,207 |

## Load

```python
import pandas as pd
A = pd.read_csv(COURSE_URL + "lab10/site_a.csv", parse_dates=["prediction_date"])
B = pd.read_csv(COURSE_URL + "lab10/site_b.csv", parse_dates=["prediction_date"])
```

## Data dictionary

### `site_a.csv` (21,927 rows) and `site_b.csv` (3,207 rows) · one row per member per prediction moment

| Column | Type | Description | When recorded | Source |
|---|---|---|---|---|
| `member_id` | integer | Pseudonymous member identifier, stable across prediction moments | | Plan |
| `prediction_date` | date | The prediction moment | | |
| `age` | integer | Age in years on the prediction date | At the prediction date | Enrollment file |
| `sex` | text | `F` or `M` | At the prediction date | Enrollment file |
| `region` | text | `Basin`, `Corridor`, or `Foothills` (residence) | At the prediction date | Enrollment file |
| `language` | text | Preferred language: `English`, `Spanish`, or `Other` | At the prediction date | EHR |
| `insurance` | text | Coverage on the prediction date | At the prediction date | Enrollment file |
| `prior_pcp_visits` | integer | Primary care visits in the 12 months before | 12 months before | EHR |
| `prior_ed_visits` | integer | Site A: emergency department visits in the 12 months before (EHR encounters). Site B: emergency and urgent care visits in the 12 months before (claims, place of service 23 or 20) | 12 months before | Site A: EHR; Site B: claims |
| `prior_inpatient_stays` | integer | Inpatient stays in the 12 months before | 12 months before | EHR or claims |
| `a1c_last` | decimal | Most recent hemoglobin A1c (%) in the 12 months before; blank if none | 12 months before | EHR |
| `bmi_last` | decimal | Most recent body mass index in the 12 months before; blank if none | 12 months before | EHR |
| `insulin` | integer | 1 if an insulin prescription was active on the prediction date | At the prediction date | EHR |
| `n_chronic_conditions` | integer | Chronic conditions on the problem list (hypertension, hyperlipidemia, chronic kidney disease, COPD, heart failure, depression, asthma, obesity) | At the prediction date | EHR |
| `prior_cost` | decimal | Total allowed cost, all services, in the 12 months before (dollars) | 12 months before | Claims |
| `care_coordination_flag` | integer | 1 if the EHR shows an active care coordination flag | Extract taken 12.5 months after the prediction date | EHR |
| `avoidable_ed_12m` | integer | Label: 1 if any emergency visit for an ambulatory-care-sensitive condition in the 12 months after | 12 months after | Claims |
| `cost_12m` | decimal | Label: total allowed cost, all services, in the 12 months after (dollars) | 12 months after | Claims |
| `active_conditions_12m` | integer | Active chronic conditions during the 12 months after: a measure of health need, for comparing who each label selects | 12 months after | EHR |

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
