#!/usr/bin/env python3
"""
Mark Common Blocked Domains in CSV Files

This script processes all CSV files in a given directory,
finds domains present in every file that are consistently blocked,
and marks them as 'NOACCESIBLEPORMETODO'.

How to use:
1. Adjust DIRECTORY_TO_PROCESS below.
2. Run: python mark_common_blocked_domains.py
"""

import os
import pandas as pd

DIRECTORY_TO_PROCESS = "data/csv_output/dns_dig_results"


def load_csvs(directory):
    """
    Load CSV files and strip whitespace in 'Dominio' column.
    """
    csv_files = sorted(
        [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    )

    if not csv_files:
        print("No CSV files were found in the directory.")
        return [], []

    dataframes = []
    for path in csv_files:
        df = pd.read_csv(path)
        if 'Dominio' in df.columns and 'Bloqueado' in df.columns:
            df['Dominio'] = df['Dominio'].astype(str).str.strip()
            dataframes.append(df)
        else:
            print(f"Skipping {path}: missing required columns.")
    return csv_files, dataframes


def find_common_domains(dataframes):
    """
    Find domains present in all dataframes.
    """
    common_domains = set(dataframes[0]['Dominio'].dropna())
    for df in dataframes[1:]:
        common_domains &= set(df['Dominio'].dropna())
    return common_domains


def find_blocked_domains(common_domains, dataframes):
    """
    Return domains that are blocked ('Sí') in all dataframes.
    """
    blocked_domains = []
    for domain in common_domains:
        if all(
            df.loc[df['Dominio'] == domain, 'Bloqueado'].eq('Sí').any()
            for df in dataframes
        ):
            blocked_domains.append(domain)
    return blocked_domains


def update_csvs(csv_files, dataframes, blocked_domains):
    """
    Update the CSVs in place, marking the selected domains.
    """
    for path, df in zip(csv_files, dataframes):
        mask = df['Dominio'].isin(blocked_domains) & df['Bloqueado'].eq('Sí')
        updated_rows = mask.sum()
        if updated_rows > 0:
            df.loc[mask, 'Bloqueado'] = 'NOACCESIBLEPORMETODO'
            df.to_csv(path, index=False)
            print(f"{os.path.basename(path)}: {updated_rows} rows updated.")
        else:
            print(f"{os.path.basename(path)}: no rows to update.")


def main():
    print(f"Processing directory: {DIRECTORY_TO_PROCESS}")
    csv_files, dataframes = load_csvs(DIRECTORY_TO_PROCESS)

    if len(dataframes) < 2:
        print("Not enough valid CSV files to compare.")
        return

    common_domains = find_common_domains(dataframes)

    if not common_domains:
        print("No common domains found across all files.")
        return

    blocked_domains = find_blocked_domains(common_domains, dataframes)

    if not blocked_domains:
        print("No domains consistently blocked across all files.")
        return

    print(f"Total domains to update: {len(blocked_domains)}")

    update_csvs(csv_files, dataframes, blocked_domains)


if __name__ == "__main__":
    main()
