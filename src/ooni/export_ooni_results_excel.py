#!/usr/bin/env python3
"""
Merge VPN Measurement Results with Manual Classification

This script:
1. Loads VPN experiment data and manual classifications.
2. Normalizes domains.
3. Joins both datasets.
4. Fills missing labels.
5. Exports results to Excel.

How to use:
1. Adjust FILE_NAME below.
2. Run: python merge_vpn_with_manual.py
"""

import pandas as pd
from urllib.parse import urlparse
import os

# without extension
FILE_NAME = "venezuela_vpn"

VPN_CSV_PATH = f"data/csv_output/vpn_measurements/{FILE_NAME}.csv"
MANUAL_CSV_PATH = "data/csv_output/url_classification/manual_vpn.csv"
OUTPUT_EXCEL_PATH = f"data/excel/manual_classification/vpn/{FILE_NAME}.xlsx"


def extract_base_domain(url):
    """
    Extract the base domain (e.g., 'facebook.com').
    """
    if pd.isna(url):
        return ""
    try:
        url = str(url).strip().lower()
        if not url.startswith("http"):
            url = "http://" + url
        netloc = urlparse(url).netloc or urlparse("http://" + url).path
        netloc = netloc.replace("www.", "")
        parts = netloc.split(".")
        if len(parts) >= 2:
            return ".".join(parts[-2:])
        return netloc
    except Exception:
        return ""


def load_and_prepare_vpn_data(csv_path):
    """
    Load VPN measurement CSV and add normalized columns.
    """
    df = pd.read_csv(csv_path)
    df["input_normalized"] = (
        df["input"]
        .str.replace("https://", "", regex=False)
        .str.replace("http://", "", regex=False)
        .str.replace("www.", "", regex=False)
        .str.rstrip("/")
    )
    df["base_domain"] = df["input"].apply(extract_base_domain)
    return df


def load_and_prepare_manual_data(csv_path):
    """
    Load manual classification CSV and deduplicate by domain.
    """
    df = pd.read_csv(csv_path)
    df["base_domain"] = df["input"].apply(lambda x: extract_base_domain(str(x)))

    grouped = df.groupby("base_domain")["deduccion"].agg(
        lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]
    ).reset_index()

    return grouped


def merge_and_export(vpn_df, manual_df, output_path):
    """
    Merge datasets and export to Excel.
    """
    vpn_filtered = vpn_df[
        [
            "input_normalized",
            "base_domain",
            "dns_experiment_failure",
            "http_experiment_failure",
            "accessible",
            "resolver_asn",
            "resolver_ip",
            "status_code",
        ]
    ].copy()
    vpn_filtered.rename(columns={"accessible": "is_accessible"}, inplace=True)

    merged = pd.merge(
        vpn_filtered,
        manual_df,
        how="left",
        on="base_domain"
    )

    merged["deduccion"] = merged["deduccion"].fillna("NO_CLASSIFIED")

    merged = merged.drop_duplicates(subset="input_normalized", keep="first")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged.to_excel(output_path, index=False)

    print(f"Merged data exported to: {output_path}")
    print(merged[["input_normalized", "base_domain", "deduccion"]].head())


def main():
    print(f"Loading VPN data from: {VPN_CSV_PATH}")
    vpn_df = load_and_prepare_vpn_data(VPN_CSV_PATH)

    print(f"Loading manual classification data from: {MANUAL_CSV_PATH}")
    manual_df = load_and_prepare_manual_data(MANUAL_CSV_PATH)

    print("Merging datasets...")
    merge_and_export(vpn_df, manual_df, OUTPUT_EXCEL_PATH)


if __name__ == "__main__":
    main()
