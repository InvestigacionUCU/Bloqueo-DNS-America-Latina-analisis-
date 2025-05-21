import os
import pandas as pd

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

    # Encontrar inputs comunes a todos los CSV
    common_inputs = set(dataframes[0]['input'].dropna())
    for df in dataframes[1:]:
        common_inputs &= set(df['input'].dropna())

    if not common_inputs:
        print("No hay 'input' comunes entre todos los archivos.")
        return

    # Función para saber si accessible es False (booleano o string 'false')
    def is_accessible_false(value):
        if pd.isna(value):
            return False
        if isinstance(value, bool):
            return value is False
        return str(value).strip().lower() == 'false'

    inputs_to_update = set()
    for inp in common_inputs:
        # Revisar que en todos los CSV, para este input, accessible sea False
        if all(
            df.loc[df['input'] == inp, 'accessible'].apply(is_accessible_false).all()
            for df in dataframes
        ):
            inputs_to_update.add(inp)

    if not inputs_to_update:
        print("No hay inputs comunes con 'accessible' = False en todos los CSV.")
        return

    # Actualizar los CSV originales
    for path, df in zip(csv_files, dataframes):
        mask = df['input'].isin(inputs_to_update)
        df.loc[mask & df['accessible'].apply(is_accessible_false), 'accessible'] = 'NOACCESIBLEPORMETODO'
        df.to_csv(path, index=False)
        print(f"Archivo actualizado: {path}")

# Ejecutar
mesh("csv_output/vpn")
