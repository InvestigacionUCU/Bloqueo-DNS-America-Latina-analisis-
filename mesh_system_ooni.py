import os
import pandas as pd

def mesh(directory: str) -> None:
    csv_files = [os.path.join(directory, f) for f in sorted(os.listdir(directory)) if f.endswith('.csv')]

    if not csv_files:
        print("No se encontraron archivos CSV en el directorio.")
        return

    dataframes = []
    for file in csv_files:
        df = pd.read_csv(file)
        if 'input' not in df.columns or 'accessible' not in df.columns:
            print(f"El archivo {file} no contiene las columnas necesarias. Se omitirá.")
            continue
        dataframes.append(df)

    if len(dataframes) < 2:
        print("No hay suficientes archivos válidos para comparar.")
        return

    # Encontrar inputs comunes a todos los CSV
    common_inputs = set(dataframes[0]['input'].dropna())
    for df in dataframes[1:]:
        common_inputs &= set(df['input'].dropna())

    if not common_inputs:
        print("No hay 'input' comunes entre todos los archivos.")
        return

    # Función robusta para saber si accessible es False
    def is_accessible_false(value):
        if pd.isna(value):
            return False
        str_val = str(value).strip().lower()
        return str_val in ['false', '0', 'no']

    inputs_to_update = set()
    for inp in common_inputs:
        if all(
            df.loc[df['input'] == inp, 'accessible'].apply(is_accessible_false).all()
            for df in dataframes
        ):
            inputs_to_update.add(inp)

    if not inputs_to_update:
        print("No hay inputs comunes con 'accessible' = False en todos los CSV.")
        return

    print(f"Total de inputs a actualizar: {len(inputs_to_update)}")

    # Actualizar los CSV originales
    for path, df in zip(csv_files, dataframes):
        mask = df['input'].isin(inputs_to_update)

        # Convertir tipo para evitar warning al asignar string
        df['accessible'] = df['accessible'].astype(object)

        cambios_antes = (df['accessible'] == 'NOACCESIBLEPORMETODO').sum()

        df.loc[mask & df['accessible'].apply(is_accessible_false), 'accessible'] = 'NOACCESIBLEPORMETODO'

        cambios_despues = (df['accessible'] == 'NOACCESIBLEPORMETODO').sum()
        cambios_realizados = cambios_despues - cambios_antes

        df.to_csv(path, index=False)
        print(f"{os.path.basename(path)}: {cambios_realizados} cambios realizados.")

# Ejecutar
mesh("csv_output/locales")
