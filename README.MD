# DNS Blocking Analysis and Classification Toolkit

This repository contains a collection of Python scripts for:

- Downloading measurement data from the [OONI](https://ooni.org) API  
- Cleaning and normalizing URLs  
- Merging measurement results with manual classifications  
- Tag-based classification of websites  
- Exporting reports in CSV and Excel  

The project is designed for transparency research and censorship measurement workflows.

---

## Project Structure

```

dns-blocking-analysis/
│
├── src/
│ ├── classification/
│ │ ├── classify_urls_by_tags.py
│ │ ├── generate_unique_inputs.py
│ │
│ ├── ooni/
│ │ ├── fetch_ooni_historical_data.py
│ │ ├── fetch_ooni_run_results.py
│ │ ├── fetch_measurements_by_resolver.py
│ │
│ ├── processing/
│ │ ├── merge_dig_with_classification.py
│ │ ├── merge_vpn_with_manual.py
│ │ ├── mark_common_blocked_domains.py
│ │ └── mark_common_inaccessible_inputs.py
│
├── data/
│ ├── csv_output/
│ │ ├── dns_dig_results/
│ │ ├── local_measurements/
│ │ ├── ooni_historical_measurements/
│ │ ├── ooni_run_measurements/
│ │ ├── ooni_measurements_by_resolver_ip/
│ │ ├── url_classification/
│ │ └── vpn_measurements/
│ │
│ └── excel/
│ ├── manual_classification/
│ └── tag_classification/
│
├── requirements.txt
├── .gitignore
└── README.md

```

---

## Requirements

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## OONI Data Download Scripts

### `fetch_ooni_historical_data.py`

* Downloads historical measurements from 2023–2025 for multiple countries.
* Filters results with DNS blocking.
* Saves deduplicated CSV.

Configuration at the top:

```python
COUNTRIES = ["UY", "VE", "HN", "AR"]
START_YEAR = 2023
END_YEAR = 2025
```

---

### `fetch_ooni_run_results.py`

* Downloads measurements for a specific `ooni_run_link_id` over a date range.
* Filters DNS blocking.
* Saves to CSV.

Configuration:

```python
OONI_RUN_LINK_ID = 10158
START_DATE = date(2025, 5, 24)
END_DATE = date(2025, 5, 28)
```

---

### `fetch_measurements_by_resolver.py`

* Loads measurement UIDs from CSV.
* Fetches raw measurement data.
* Extracts fields and saves separate CSVs per `resolver_ip`.

Configure `INPUT_CSV_PATH` at the top.

---

## URL Classification Scripts

### `classify_urls_by_tags.py`

* Loads a list of URLs.
* Downloads HTML content.
* Counts keyword occurrences by category.
* Outputs a CSV of detected categories and scores.

Configure:

```python
TAGS_CSV_PATH = "data/csv_output/url_classification/tags_dictionary.csv"
INPUT_URLS_PATH = "data/csv_output/url_classification/inputs_pre_tagging.csv"
OUTPUT_CSV_PATH = "data/csv_output/url_classification/categorized_tags.csv"
```

---

### `generate_unique_inputs.py`

* Aggregates unique URLs across multiple CSVs.
* Filters out rows marked as not accessible.

Change `DIRECTORY_TO_PROCESS` in the script.

---

## Processing and Merging Scripts

### `merge_dig_with_classification.py`

* Merges Dig measurement results with manual classifications.
* Normalizes domains to improve matches.
* Exports Excel reports.

Configure:

```python
COUNTRY_NAME = "venezuela"
```

---

### `merge_vpn_with_manual.py`

* Merges VPN experiment results with manual classifications.
* Deduplicates by base domain.
* Fills missing labels as `NO_CLASSIFIED`.
* Exports to Excel.

Configure:

```python
FILE_NAME = "venezuela_vpn"
```

---

### `mark_common_blocked_domains.py`

* Marks domains that are blocked in all Dig files as `NOACCESIBLEPORMETODO`.

Configure:

```python
DIRECTORY_TO_PROCESS = "data/csv_output/dns_dig_results"
```

---

### `mark_common_inaccessible_inputs.py`

* Marks inputs that are inaccessible in all measurement files as `NOACCESIBLEPORMETODO`.

Configure:

```python
DIRECTORY_TO_PROCESS = "data/csv_output/local_measurements"
```

---

## Usage Example

Each script can be run directly:

```bash
python src/ooni/fetch_ooni_historical_data.py
python src/classification/classify_urls_by_tags.py
python src/processing/merge_vpn_with_manual.py
```

