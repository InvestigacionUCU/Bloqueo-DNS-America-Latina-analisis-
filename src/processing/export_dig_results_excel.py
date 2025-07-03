#!/usr/bin/env python3
"""
Merge Dig Blocking Results with Manual Classification

This script:
1. Loads a Dig CSV file with blocking information.
2. Loads a CSV with manual classifications.
3. Normalizes URLs/domains to enable matching.
4. Joins both datasets.
5. Exports the combined result to Excel.

How to use:
1. Set COUNTRY_NAME below.
2. Run: python merge_dig_with_classification.py
"""

import pandas as pd
import os

COUNTRY_NAME = "venezuela"

# 👉 Paths
DIG_CSV_PATH = f"data/csv_output/dns_dig_results/{COUNTRY_NAME}.csv"
CLASSIFICATION_CSV_PATH = "data/csv_output/url_classification/categorized_tags.csv"
OUTPUT_EXCEL_PATH = f"data/excel/manual_classification/dig/{COUNTRY_NAME}_dig_classification.xlsx"


def normalize_url(url):
    """
    Remove scheme and www from URL or domain.
    """
    if pd.isna(url):
        return ""
    url = str(url)
    url = url.replace("http://", "").replace("https://", "")
    url = url.replace("www.", "").strip().rstrip("/")
    return url


def load_and_prepare_dig(csv_path):
    """
    Load Dig CSV and prepare columns.
    """
    df = pd.read_csv(csv_path)
    df_filtered = df[df["Bloqueado"] == "Sí"].copy()
    df_filtered["domain"] = df_filtered["Dominio"]
    df_filtered["status"] = df_filtered["Status"]
    df_filtered["accessible"] = "No"
    df_filtered["normalized_domain"] = df_filtered["domain"].apply(normalize_url)
    return df_filtered


def load_and_prepare_classification(csv_path):
    """
    Load classification CSV and normalize URLs.
    """
    df = pd.read_csv(csv_path)
    df["normalized_url"] = df["url"].apply(normalize_url)
    return df[["normalized_url", "deduccion primaria", "deduccion secundaria"]].copy()


def merge_data(dig_df, class_df):
    """
    Merge Dig and classification dataframes on normalized URL/domain.
    """
    merged = pd.merge(
        dig_df[["domain", "status", "accessible", "normalized_domain"]],
        class_df,
        how="left",
        left_on="normalized_domain",
        right_on="normalized_url"
    )
    merged.drop(columns=["normalized_domain", "normalized_url"], inplace=True)
    return merged


def main():
    if not os.path.exists(DIG_CSV_PATH):
        print(f"Dig file not found: {DIG_CSV_PATH}")
        return
    if not os.path.exists(CLASSIFICATION_CSV_PATH):
        print(f"Classification file not found: {CLASSIFICATION_CSV_PATH}")
        return

    print(f"Loading Dig data from: {DIG_CSV_PATH}")
    dig_df = load_and_prepare_dig(DIG_CSV_PATH)

    print(f"Loading classification data from: {CLASSIFICATION_CSV_PATH}")
    class_df = load_and_prepare_classification(CLASSIFICATION_CSV_PATH)

    print("Merging datasets...")
    result_df = merge_data(dig_df, class_df)

    print(f"Exporting merged data to Excel: {OUTPUT_EXCEL_PATH}")
    result_df.to_excel(OUTPUT_EXCEL_PATH, index=False)
    print("Done.")


if __name__ == "__main__":
    main()
