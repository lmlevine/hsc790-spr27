# Lab 4 · Two Front Doors, One Registry (Week 5)

Laboratory results reach the registry through two channels.

- **HL7 v2.** `elr_batch_2027-02-15.hl7` is one week of electronic laboratory reports received February 15 to 21, 2027: 432 ORU^R01 messages, HL7 version 2.5.1, from five laboratories.
- **FHIR R4.** The `fhir/` folder holds what the regional health information organization's FHIR server returned for a search for laboratory Observations with their Patients included, 100 Observations per page.

Parse both, map them to your registry, and land them through your Lab 2 checks.

| File | What it is |
|---|---|
| `elr_batch_2027-02-15.hl7` | The v2 batch: 432 messages |
| `fhir/metadata.json` | The server's CapabilityStatement (`GET [base]/metadata`) |
| `fhir/observation_page_1.json` to `observation_page_4.json` | The four pages of the search, as `searchset` Bundles |
| `fhir/transaction_bundle.json` | The same Patients and Observations as one `transaction` Bundle, for loading onto a test server |
| `fhir_offline.py` | Serves the bundled pages in place of a live server |
| `load_fhir_test_server.py` | Loads `transaction_bundle.json` onto a public test server (instructor use) |

## The v2 file

Messages follow one another; each starts with an `MSH` segment. The standard separates segments with carriage returns, but this file uses newlines, as many files do, so split on either. Each message has the segments `MSH`, `PID`, `ORC`, `OBR`, `OBX`, and `SPM`.

```python
import requests
text = requests.get(COURSE_URL + "lab04/elr_batch_2027-02-15.hl7").text
lines = text.replace("\r", "\n").split("\n")
messages, cur = [], []
for line in lines:
    if line.startswith("MSH|") and cur:
        messages.append(cur); cur = []
    if line:
        cur.append(line)
messages.append(cur)
```

Fields you will need. Remember that in `MSH` the field separator itself is MSH-1, so `line.split("|")[n]` is MSH-(n+1); in every other segment `split("|")[n]` is field n.

| Field | Content |
|---|---|
| MSH-4 | Sending facility (`name^CLIA number^CLIA`) |
| MSH-7 | Date and time the message was sent |
| MSH-10 | Message control ID |
| PID-3 | Patient identifier at the sending laboratory |
| PID-5 | Name (`family^given^middle initial`) |
| PID-7 | Birth date |
| PID-8 | Sex |
| PID-10 | Race (`code^text^system`) |
| PID-11 | Address (`street^^city^state^ZIP`) |
| PID-13 | Phone |
| PID-22 | Ethnicity (`code^text^system`) |
| ORC-3, OBR-3 | Accession number (filler order number) |
| ORC-21 | Ordering facility name |
| OBR-4 | Test ordered (`code^text^coding system`) |
| OBR-7 | Specimen collection date and time |
| OBX-3 | Test performed (`code^text^coding system`) |
| OBX-5 | Result (`code^text^coding system`) |
| OBX-11 | Result status |
| OBX-14 | Date and time of the result |
| SPM-4 | Specimen type |
| SPM-17 | Specimen collection date and time |

## The FHIR pages

The search the pages answer:

```
GET https://fhir.puente-hio.example/baseR4/Observation?_tag=https://hsc790.example/tags|hsc790-spring2027&_count=100&_include=Observation:patient
```

That server is fictional, so `fhir_offline.py` stands in for it: `fetch(url, params)` returns the bundled page that a request for `url` would have returned. Use it in place of `requests.get(url, params=params).json()` and the paging loop on the slide runs unchanged.

```python
import urllib.request
urllib.request.urlretrieve(COURSE_URL + "lab04/fhir_offline.py", "fhir_offline.py")
import fhir_offline as fo
fo.COURSE_URL = COURSE_URL

BASE = "https://fhir.puente-hio.example/baseR4"
TAG = "https://hsc790.example/tags|hsc790-spring2027"
bundle = fo.fetch(BASE + "/Observation", {"_tag": TAG, "_count": 100, "_include": "Observation:patient"})
```

Each page is a Bundle of type `searchset`. Its `link` list has a `self` link and, on every page but the last, a `next` link. In `entry`, Observations have `search.mode = "match"` and the Patients they reference have `search.mode = "include"`; a Patient referenced from several pages is included on each of them.

- **Observation:** `id`, `identifier` (accession number), `status`, `category`, `code` (LOINC), `valueCodeableConcept` or `valueQuantity`, `subject` (a reference to the Patient), `effectiveDateTime`.
- **Patient:** `id`, `identifier` (the information organization's person index), `name`, `gender`, `birthDate`, `address`, and the US Core race and ethnicity extensions.

If the instructor loads the same resources onto a public FHIR test server, set `BASE` to that server, use `requests.get`, and search with the same tag. Public test servers are open to everyone: never post anything but synthetic data to one.

---

`COURSE_URL` is the raw address of the repository's `data/` folder; the course README shows how to set it. Everything in this folder is synthetic.
