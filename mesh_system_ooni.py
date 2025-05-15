import os
import pandas as pd
import csv

def save_to_csv(data: list, label: str, output_folder: str = "csv_output") -> None:
    if not data:
        print("No hay datos para guardar.")
        return

    os.makedirs(output_folder, exist_ok=True)
    file_name = f"{output_folder}/{label}.csv"
    headers = list(data[0].keys())
    write_header = not os.path.exists(file_name)

    with open(file_name, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        if write_header:
            writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Archivo guardado: {file_name}")


def mesh(directory: str) -> None:
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    dataframes = [pd.read_csv(file) for file in csv_files]

    common_inputs = set(dataframes[0]['input'])
    for df in dataframes[1:]:
        common_inputs &= set(df['input'])

    result_df = pd.DataFrame(common_inputs, columns=["input"])
    save_to_csv(result_df.to_dict(orient="records"), label="pages_no_longer_exist", output_folder="csv_output/pages_no_longer_exist")


def delete_url(directory: str, reference_file_path: str) -> None:
    reference_df = pd.read_csv(reference_file_path)
    reference_input = reference_df["input"]
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]

    for file in csv_files:
        if os.path.abspath(file) == os.path.abspath(reference_file_path):
            continue

        current_df = pd.read_csv(file)
        filtered_df = current_df[~current_df['input'].isin(reference_input)]

        if not filtered_df.equals(current_df):
            filtered_df.to_csv(file, index=False)


# Ejecutar
mesh("csv_output/lists")
delete_url("csv_output/lists", "csv_output/pages_no_longer_exist/pages_no_longer_exist.csv")
