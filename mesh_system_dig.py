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


def mesh_digs(directory: str) -> None:
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    dataframes = [pd.read_csv(file) for file in csv_files]

    # Intersección de dominios
    common_domains = set(dataframes[0]["Dominio"].str.strip())
    for df in dataframes[1:]:
        common_domains &= set(df["Dominio"].str.strip())

    # Filtrar solo los que están bloqueados en TODOS los archivos
    blocked_domains = []
    for domain in common_domains:
        blocked_in_all = all(
            df[df["Dominio"].str.strip() == domain]["Bloqueado"].str.strip().str.lower().eq("sí").any()
            for df in dataframes
        )
        if blocked_in_all:
            blocked_domains.append(domain)

    # Guardar los dominios bloqueados comunes con sus datos
    result_rows = []
    for df in dataframes:
        result_rows.extend(df[df["Dominio"].str.strip().isin(blocked_domains)].to_dict(orient="records"))
        break  # Solo necesitamos una muestra de datos para guardar (son iguales en todos)

    save_to_csv(result_rows, label="digs_no_long_exist", output_folder="csv_output/digs_no_long_exist")


def delete_domains(directory: str, reference_file_path: str) -> None:
    reference_df = pd.read_csv(reference_file_path)
    reference_domains = reference_df["Dominio"].str.strip()
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]

    for file in csv_files:
        if os.path.abspath(file) == os.path.abspath(reference_file_path):
            continue

        current_df = pd.read_csv(file)
        filtered_df = current_df[~current_df["Dominio"].str.strip().isin(reference_domains)]

        if not filtered_df.equals(current_df):
            filtered_df.to_csv(file, index=False)

# Ejecutar
mesh_digs("csv_output/digs")
delete_domains("csv_output/digs", "csv_output/digs_no_long_exist/digs_no_long_exist.csv")
