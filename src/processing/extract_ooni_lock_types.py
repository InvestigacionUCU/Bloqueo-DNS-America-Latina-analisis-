#!/usr/bin/env python3
"""
Download Raw Measurement Data from OONI and Save to CSV Files by Resolver IP

This script:
1. Reads a CSV containing 'measurement_uid'.
2. Fetches raw measurement data for each UID.
3. Extracts key fields.
4. Saves each row to a CSV named after the 'resolver_ip'.

How to use:
1. Set INPUT_CSV_PATH below.
2. Run: python fetch_measurements_by_resolver.py
"""

import os
import csv
import requests

INPUT_CSV_PATH = "data/csv_output/ooni_run_measurements/ooni_run_measurements_results.csv"
OONI_API_URL = "https://api.ooni.org/api/v1/raw_measurement"


def execute_query(query_url):
    """
    Send GET request to OONI API and return JSON data.
    """
    response = requests.get(query_url)
    if response.status_code == 200:
        return response.json()
    print(f"Error fetching data: HTTP {response.status_code}")
    return {}


def load_measurement_uids(input_csv):
    """
    Read measurement_uids from the input CSV file.
    """
    measurement_uids = []
    with open(input_csv, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            uid = row.get("measurement_uid")
            if uid:
                measurement_uids.append(uid)
    return measurement_uids


def extract_measurement_row(uid, data):
    """
    Extract fields of interest from the API response.
    """
    test_keys = data.get("test_keys", {})
    control = test_keys.get("control", {})
    http_request = control.get("http_request", {})

    return {
        "measurement_uid": uid,
        "input": data.get("input", "None"),
        "dns_experiment_failure": test_keys.get("dns_experiment_failure", "None"),
        "http_experiment_failure": test_keys.get("http_experiment_failure", "None"),
        "dns_consistency": test_keys.get("dns_consistency", "None"),
        "accessible": test_keys.get("accessible", "None"),
        "resolver_asn": data.get("resolver_asn", "None"),
        "resolver_ip": data.get("resolver_ip", "None"),
        "status_code": http_request.get("status_code", "None")
    }


def save_row_by_resolver_ip(row, output_base="data/csv_output/lists"):
    """
    Save the row to a CSV file named after the resolver_ip.
    """
    resolver_ip = row.get("resolver_ip", "Unknown")
    os.makedirs(output_base, exist_ok=True)
    output_path = os.path.join(output_base, f"{resolver_ip}.csv")

    write_header = not os.path.exists(output_path)

    with open(output_path, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())
        if write_header:
            writer.writeheader()
        writer.writerow(row)

    print(f"Saved measurement UID {row['measurement_uid']} to {output_path}")


def process_measurements(input_csv):
    """
    Main processing function.
    """
    uids = load_measurement_uids(input_csv)
    if not uids:
        print("No measurement_uids found in input CSV.")
        return

    print(f"Processing {len(uids)} measurement(s)...")

    for uid in uids:
        query_url = f"{OONI_API_URL}?measurement_uid={uid}"
        data = execute_query(query_url)

        if not data:
            print(f"Skipping UID {uid}: no data returned.")
            continue

        row = extract_measurement_row(uid, data)
        save_row_by_resolver_ip(row)


if __name__ == "__main__":
    print(f"Reading measurement_uids from: {INPUT_CSV_PATH}")
    process_measurements(INPUT_CSV_PATH)
