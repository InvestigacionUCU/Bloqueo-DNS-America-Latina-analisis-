import os
import pandas as pd

def mesh_digs(directory: str) -> None:
    csv_files = [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.csv')]
    if not csv_files:
        print("No se encontraron archivos CSV en el directorio.")
        return

    # Leer archivos y limpiar los dominios
    dataframes = []
    for path in csv_files:
        df = pd.read_csv(path)
        df["Dominio"] = df["Dominio"].str.strip()
        dataframes.append(df)

    # Encontrar dominios comunes
    common_domains = set(dataframes[0]["Dominio"])
    for df in dataframes[1:]:
        common_domains &= set(df["Dominio"])

    # Filtrar dominios bloqueados en todos los archivos
    blocked_domains = []
    for domain in common_domains:
        if all(
            df.loc[df["Dominio"] == domain, "Bloqueado"].eq("Sí").any()
            for df in dataframes
        ):
            blocked_domains.append(domain)

    if not blocked_domains:
        print("No hay dominios bloqueados comunes en todos los archivos.")
        return

    # Actualizar archivos
    for path, df in zip(csv_files, dataframes):
        mask = (df["Dominio"].isin(blocked_domains)) & (df["Bloqueado"] == "Sí")
        df.loc[mask, "Bloqueado"] = "NOACCESIBLEPORMETODO"
        df.to_csv(path, index=False)
        print(f"Archivo actualizado: {path}")


# Ejecutar
mesh_digs("csv_output/digs")