#!/usr/bin/env python3
"""
Mark Common Inaccessible Inputs in CSV Files

This script processes all CSV files in a given directory,
finds inputs that are present in every file and consistently inaccessible,
and marks them as 'NOACCESIBLEPORMETODO'.

To use it:
1. Adjust DIRECTORY_TO_PROCESS below.
2. Run: python mark_common_inaccessible.py
"""

import os
import pandas as pd

DIRECTORY_TO_PROCESS = "data/csv_output/local_measurements"


def load_valid_csvs(directory):
    """
    Load CSV files that contain the required columns.
    Returns a list of pandas DataFrames.
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
        if {'input', 'accessible'}.issubset(df.columns):
            dataframes.append(df)
        else:
            print(f"Skipping {path}: missing required columns.")
    return csv_files, dataframes


def get_common_inputs(dataframes):
    """
    Find inputs present in all dataframes.
    """
    common_inputs = set(dataframes[0]['input'].dropna())
    for df in dataframes[1:]:
        common_inputs &= set(df['input'].dropna())
    return common_inputs


def is_accessible_false(value):
    """
    Determine whether a value indicates 'inaccessible'.
    """
    if pd.isna(value):
        return False
    str_val = str(value).strip().lower()
    return str_val in {'false', '0', 'no'}


def find_inputs_to_update(common_inputs, dataframes):
    """
    Return the set of inputs that are inaccessible in all dataframes.
    """
    inputs_to_update = set()
    for inp in common_inputs:
        if all(
            df.loc[df['input'] == inp, 'accessible'].apply(is_accessible_false).all()
            for df in dataframes
        ):
            inputs_to_update.add(inp)
    return inputs_to_update


def update_csvs(csv_files, dataframes, inputs_to_update):
    """
    Update the CSVs in place, marking the selected inputs.
    """
    for path, df in zip(csv_files, dataframes):
        mask = df['input'].isin(inputs_to_update)

        df['accessible'] = df['accessible'].astype(object)

        before_changes = (df['accessible'] == 'NOACCESIBLEPORMETODO').sum()

        df.loc[mask & df['accessible'].apply(is_accessible_false), 'accessible'] = 'NOACCESIBLEPORMETODO'

        after_changes = (df['accessible'] == 'NOACCESIBLEPORMETODO').sum()
        changes_made = after_changes - before_changes

        df.to_csv(path, index=False)
        print(f"{os.path.basename(path)}: {changes_made} rows updated.")


def main():
    print(f"Processing directory: {DIRECTORY_TO_PROCESS}")
    csv_files, dataframes = load_valid_csvs(DIRECTORY_TO_PROCESS)

    if len(dataframes) < 2:
        print("Not enough valid CSV files to compare.")
        return

    common_inputs = get_common_inputs(dataframes)

    if not common_inputs:
        print("No common 'input' values found across all files.")
        return

    inputs_to_update = find_inputs_to_update(common_inputs, dataframes)

    if not inputs_to_update:
        print("No inputs consistently marked as inaccessible across all files.")
        return

    print(f"Total inputs to update: {len(inputs_to_update)}")

    update_csvs(csv_files, dataframes, inputs_to_update)


if __name__ == "__main__":
    main()
