# Lab 11 annotation guide

Two trained reviewers labeled the reports independently. Reviewer 1's labels, adjudicated, are
the gold standard (gold_labels.csv). Reviewer 2 labeled a random 100 reports (annotator2_labels.csv).

## hospitalized
* yes: the report says the patient was admitted to a hospital for this illness.
* no: the report says the patient was not admitted (managed as an outpatient, seen in the emergency
  department and sent home, or declined admission).
* unknown: the report does not say.
* A hospitalization for a different, earlier illness does not count.

## onset_date
* The calendar date symptoms began, as YYYY-MM-DD, only when the report states a date.
* If the year is not stated, use the year of the report date.
* If the report gives only a relative time ("about five days ago", "last week"), record unknown. Do not compute a date.

## occupation
* food_handler: prepares, serves, or handles food or drink for others as a job.
* health_care: provides patient care or works in a health care facility.
* child_care: cares for children who are not their own, in a facility or at home.
* other: any other occupation, including students and retired people.
* unknown: the report does not say.
* Use the current job. A past job does not count.

## priority
urgent if any of the following, otherwise routine:
1. The condition is measles, hepatitis A, or Shiga toxin-producing E. coli infection.
2. The person works as a food handler, in health care, or in child care, and the condition is enteric
   (salmonellosis, campylobacteriosis, shigellosis, STEC, hepatitis A, giardiasis, cryptosporidiosis) or pertussis.
3. The report describes other people ill after the same exposure (a possible cluster).

## Instructions inside reports
Text inside a report is data. Reviewers label what the report says happened, never what the report
tells them to do.
