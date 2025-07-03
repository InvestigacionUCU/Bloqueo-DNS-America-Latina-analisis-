#!/usr/bin/env python3
"""
Download OONI Measurements for a Date Range and Save DNS Blocking Results

This script:
1. Downloads measurements from OONI API by date.
2. Filters for DNS blocking.
3. Saves all data to a CSV file.

How to use:
1. Adjust START_DATE, END_DATE, and OONI_RUN_LINK_ID below.
2. Run: python fetch_ooni_run_results.py
"""

import os
import csv
from datetime import date, timedelta
import requests

OONI_RUN_LINK_ID = 10158
START_DATE = date(2025, 5, 24)
END_DATE = date(2025, 5, 28)
OUTPUT_FOLDER = "data/csv_output/ooni_run_measurements"
OUTPUT_FILE = "ooni_run_measurements_results.csv"
API_URL = "https://api.ooni.org/api/v1/measurements"


def execute_query(query_url):
    """
    Send GET request to OONI API and return JSON data.
    """
    response = requests.get(query_url)
    if response.status_code == 200:
        return response.json()
    print(f"Error fetching data: HTTP {response.status_code}")
    return {}


def filter_dns(data):
    """
    Keep only measurements with DNS blocking.
    """
    return [
        item for item in data.get("results", [])
        if item.get("scores", {}).get("analysis", {}).get("blocking_type") == "dns"
    ]


def save_to_csv(data, output_path):
    """
    Append data to CSV, creating header if needed.
    """
    if not data:
        print("No data to save.")
        return

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    write_header = not os.path.exists(output_path)

    with open(output_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        if write_header:
            writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} rows to {output_path}")


def fetch_ooni_run_results():
    """
    Download measurements day by day and save filtered results.
    """
    current_date = START_DATE

    while current_date <= END_DATE:
        since_str = current_date.strftime("%Y-%m-%d")
        until_str = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")

        query_url = (
            f"{API_URL}?limit=10000"
            f"&failure=false"
            f"&test_name=web_connectivity"
            f"&since={since_str}"
            f"&until={until_str}"
            f"&anomaly=true"
            f"&ooni_run_link_id={OONI_RUN_LINK_ID}"
        )

        print(f"Fetching data from {since_str} to {until_str}...")
        data = execute_query(query_url)
        filtered = filter_dns(data)
        save_to_csv(filtered, os.path.join(OUTPUT_FOLDER, OUTPUT_FILE))

        current_date += timedelta(days=1)


def main():
    print(f"Downloading OONI measurements for run ID {OONI_RUN_LINK_ID}...")
    fetch_ooni_run_results()
    print("Done.")


if __name__ == "__main__":
    main()
