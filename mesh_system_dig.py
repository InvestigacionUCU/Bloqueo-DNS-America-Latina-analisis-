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

    if not csv_files:
        print("No se encontraron archivos CSV en el directorio.")
        return

    dataframes = []
    for file in csv_files:
        df = pd.read_csv(file)
        if 'input' not in df.columns or 'accessible' not in df.columns:
            print(f"El archivo {file} no contiene las columnas necesarias.")
            return
        dataframes.append(df)

    common_inputs = set(dataframes[0]['input'].dropna())
    for df in dataframes[1:]:
        common_inputs &= set(df['input'].dropna())

    if not common_inputs:
        print("No hay 'input' comunes entre todos los archivos.")
        return

    common_data = [{'input': url} for url in sorted(common_inputs)]
    save_to_csv(common_data, label="pages_no_longer_exist", output_folder="csv_output/pages_vpn_no_longer_exist")

    # Modificar los CSV originales
    for path, df in zip(csv_files, dataframes):
        mask = df['input'].isin(common_inputs)
        df['accessible'] = df['accessible'].astype('object')
        df.loc[mask, 'accessible'] = 'NOACCESIBLEPORMETODO'
        df.to_csv(path, index=False)
        print(f"Archivo actualizado: {path}")

# Ejecutar
mesh("csv_output/vpn")