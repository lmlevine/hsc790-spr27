"""Offline stand-in for the FHIR server in Lab 4.

The bundled pages in this folder are the responses a FHIR server returned to
    GET [base]/Observation?_tag=...&_count=100&_include=Observation:patient
Their "next" links point at a fictional server. fetch() reads the matching page
from the course repository instead, so the paging loop on the slide works unchanged:
replace requests.get(url, params=params).json() with fetch(url, params).
"""
from urllib.parse import parse_qs, urlparse

import requests

COURSE_URL = "https://raw.githubusercontent.com/<org>/<repo>/main/data/"   # set this in your notebook


def fetch(url, params=None, course_url=None):
    base = (course_url or COURSE_URL).rstrip("/") + "/lab04/fhir/"
    path = urlparse(url).path
    if path.endswith("/metadata"):
        return requests.get(base + "metadata.json").json()
    page = parse_qs(urlparse(url).query).get("_page", ["1"])[0]
    return requests.get(base + f"observation_page_{page}.json").json()
