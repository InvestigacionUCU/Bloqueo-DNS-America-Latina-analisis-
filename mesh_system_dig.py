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
    if not csv_files:
        print("No se encontraron archivos CSV en el directorio.")
        return

    dataframes = [pd.read_csv(file) for file in csv_files]

    # Intersección de dominios en todos los CSV
    common_domains = set(dataframes[0]["Dominio"].str.strip())
    for df in dataframes[1:]:
        common_domains &= set(df["Dominio"].str.strip())

    # Filtrar solo dominios bloqueados en TODOS los archivos
    blocked_domains = []
    for domain in common_domains:
        blocked_in_all = all(
            (df_domain := df[df["Dominio"].str.strip() == domain])["Bloqueado"].eq("Sí").any()
            for df in dataframes
        )
        if blocked_in_all:
            blocked_domains.append(domain)


    if not blocked_domains:
        print("No hay dominios bloqueados comunes en todos los archivos.")
        return


    df_first = dataframes[0]
    result_rows = df_first[
        (df_first["Dominio"].str.strip().isin(blocked_domains)) &
        (df_first["Bloqueado"] == "Sí")
    ].to_dict(orient="records")

    save_to_csv(result_rows, label="digs_no_long_exist", output_folder="csv_output/digs_no_long_exist")
    for file, df in zip(csv_files, dataframes):
        mask = (df["Dominio"].str.strip().isin(blocked_domains)) & (df["Bloqueado"] == "Sí")
        df.loc[mask, "Bloqueado"] = "NOACCESIBLEPORMETODO"
        df.to_csv(file, index=False)
        print(f"Archivo actualizado: {file}")

# Ejecutar
mesh_digs("test")