import os
import pandas as pd
import csv

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

    for file, df in zip(csv_files, dataframes):
        mask = (df["Dominio"].str.strip().isin(blocked_domains)) & (df["Bloqueado"] == "Sí")
        df.loc[mask, "Bloqueado"] = "NOACCESIBLEPORMETODO"
        df.to_csv(file, index=False)
        print(f"Archivo actualizado: {file}")

# Ejecutar
mesh_digs("csv_output/digs")