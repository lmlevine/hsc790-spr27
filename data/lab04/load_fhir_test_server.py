"""Load the Lab 4 FHIR resources onto a public FHIR R4 test server (instructor, before class).

Every resource carries the course tag, so students can search with
    _tag=https://hsc790.example/tags|hsc790-spring2027
Public test servers are shared and are reset from time to time; run this the day before
class and again in the morning if needed. Only synthetic data may be posted.

Usage:  python load_fhir_test_server.py [BASE]    (default BASE below)
"""
import json
import sys
from pathlib import Path

import requests

BASE = sys.argv[1] if len(sys.argv) > 1 else "https://hapi.fhir.org/baseR4"
bundle = json.loads((Path(__file__).parent / "fhir" / "transaction_bundle.json").read_text())
resp = requests.post(BASE, json=bundle, headers={"Content-Type": "application/fhir+json"}, timeout=120)
print("HTTP", resp.status_code)
resp.raise_for_status()
out = resp.json()
codes = [e.get("response", {}).get("status", "") for e in out.get("entry", [])]
print(len(codes), "entries;", sum(c.startswith("2") for c in codes), "succeeded")
check = requests.get(BASE + "/Observation", params={"_tag": "https://hsc790.example/tags|hsc790-spring2027",
                                                    "_summary": "count"}, timeout=60).json()
print("Observations with the course tag on the server:", check.get("total"))
