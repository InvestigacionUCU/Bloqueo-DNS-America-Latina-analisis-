#!/usr/bin/env python3
"""
Download and Save Historical OONI Data

This script:
1. Iterates over a set of countries and date ranges.
2. Downloads measurements from OONI API.
3. Filters DNS blocking results.
4. Removes duplicate inputs.
5. Saves data incrementally into a CSV.

How to use:
Just run: python fetch_historical_ooni.py
"""

import os
import csv
import requests
import pandas as pd

COUNTRIES = ["UY", "VE", "HN", "AR", "CU", "SV", "NI", "GT"]
START_YEAR = 2023
END_YEAR = 2025
OUTPUT_FOLDER = "data/csv_output/ooni_historical_measurements"
OUTPUT_FILE = f"{OUTPUT_FOLDER}/all_countries.csv"
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


def remove_duplicates(data):
    """
    Remove duplicate entries by 'input'.
    """
    seen_inputs = set()
    unique_data = []
    for item in data:
        input_value = item.get("input")
        if input_value not in seen_inputs:
            unique_data.append(item)
            seen_inputs.add(input_value)
    return unique_data


def get_month_range(year, month):
    """
    Return start and end date strings for a month.
    """
    start = f"{year}-{month:02d}-01"
    if month == 2:
        end = f"{year}-{month:02d}-28"
    elif month in [4, 6, 9, 11]:
        end = f"{year}-{month:02d}-30"
    else:
        end = f"{year}-{month:02d}-31"
    return start, end


def save_to_csv(data, file_path):
    """
    Append data to CSV, creating header if needed.
    """
    if not data:
        print("No data to save.")
        return

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    write_header = not os.path.exists(file_path)

    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=data[0].keys())
        if write_header:
            writer.writeheader()
        writer.writerows(data)

    print(f"Saved {len(data)} rows to {file_path}")


def fetch_data():
    """
    Download and save data month by month for all countries.
    """
    for country in COUNTRIES:
        year = START_YEAR
        while year <= END_YEAR:
            for month in range(1, 13):
                if year == 2025 and month == 2:
                    break

                start_date, end_date = get_month_range(year, month)
                query_url = (
                    f"{API_URL}?limit=2000"
                    f"&failure=false"
                    f"&probe_cc={country}"
                    f"&test_name=web_connectivity"
                    f"&since={start_date}"
                    f"&until={end_date}"
                    f"&anomaly=true"
                )

                data = execute_query(query_url)
                filtered = remove_duplicates(filter_dns(data))
                save_to_csv(filtered, OUTPUT_FILE)

            year += 1


def deduplicate_final_csv():
    """
    After all data is collected, remove duplicates again.
    """
    if not os.path.exists(OUTPUT_FILE):
        print("No CSV to deduplicate.")
        return

    df = pd.read_csv(OUTPUT_FILE)
    df_clean = df.drop_duplicates(subset="input")
    df_clean.to_csv(OUTPUT_FILE, index=False)
    print("Final deduplication completed.")


def main():
    print("Fetching historical OONI data...")
    fetch_data()
    print("Removing duplicates...")
    deduplicate_final_csv()
    print("Done.")


if __name__ == "__main__":
    main()
