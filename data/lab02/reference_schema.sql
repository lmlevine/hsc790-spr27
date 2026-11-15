-- H SC 790, Lab 1 reference schema (released with Lab 2).
-- Use this if your own Lab 1 schema is incomplete. It is one defensible design,
-- not the only one. Run it in DuckDB before loading the Lab 2 batches.

CREATE TABLE facility (
  facility_id    INTEGER PRIMARY KEY,
  facility_name  VARCHAR NOT NULL,        -- one canonical name per facility
  facility_type  VARCHAR NOT NULL,
  clia_number    VARCHAR
);

CREATE TABLE condition (
  condition_code VARCHAR PRIMARY KEY,
  condition_name VARCHAR NOT NULL
);

CREATE TABLE patient (
  patient_id     INTEGER PRIMARY KEY,
  last_name      VARCHAR NOT NULL,
  first_name     VARCHAR NOT NULL,
  birth_date     DATE,
  sex            VARCHAR CHECK (sex IN ('F', 'M', 'U')),
  ethnicity      VARCHAR,
  street_address VARCHAR,                 -- most recent address seen
  city           VARCHAR,
  zip            VARCHAR CHECK (zip IS NULL OR length(zip) = 5)
);

-- race is multi-valued: one row per patient per race reported
CREATE TABLE patient_race (
  patient_id     INTEGER NOT NULL REFERENCES patient(patient_id),
  race           VARCHAR NOT NULL,
  PRIMARY KEY (patient_id, race)
);

CREATE TABLE case_report (
  case_id        INTEGER PRIMARY KEY,
  patient_id     INTEGER NOT NULL REFERENCES patient(patient_id),
  condition_code VARCHAR NOT NULL REFERENCES condition(condition_code),
  facility_id    INTEGER REFERENCES facility(facility_id),
  onset_date     DATE,
  specimen_date  DATE,
  result_date    DATE,
  report_date    DATE NOT NULL,
  case_status    VARCHAR NOT NULL CHECK (case_status IN
      ('confirmed', 'probable', 'suspect', 'not_a_case')),
  CHECK (specimen_date IS NULL OR report_date >= specimen_date),
  CHECK (onset_date IS NULL OR specimen_date IS NULL OR onset_date <= specimen_date)
);

-- reference code table used by the quality checks
CREATE TABLE ref_status (code VARCHAR PRIMARY KEY, label VARCHAR NOT NULL);
