# eliminar duplicados de la columna input con un archivo de entrada y el mismo de salida

def eliminar_duplicados(input_file: str, output_file: str) -> None:
    """
    Elimina duplicados de la columna 'input' en un archivo CSV y guarda el resultado en otro archivo CSV.
    
    :param input_file: Ruta del archivo CSV de entrada.
    :param output_file: Ruta del archivo CSV de salida.
    """
    import pandas as pd

    # Leer el archivo CSV de entrada
    df = pd.read_csv(input_file)

    # Eliminar duplicados basados en la columna 'input'
    df_sin_duplicados = df.drop_duplicates(subset=['input'])

    # Guardar el DataFrame resultante en un nuevo archivo CSV
    df_sin_duplicados.to_csv(output_file, index=False)
    
eliminar_duplicados("data/bloqueos_ooni/200.40.53.6.csv", "data/bloqueos_ooni/uruguay.csv")