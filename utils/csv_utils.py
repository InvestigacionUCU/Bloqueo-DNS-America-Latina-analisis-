import csv
import os
import pandas as pd
import openpyxl

def save_to_csv(output_file: str, data, mode: str):
    """
    Saves data to a CSV file.

    :param output_file: The output file path.
    :param data: The data to be saved (a list of dictionaries).
    :param mode: The mode in which the file is opened ('w' for write, 'a' for append).
    """
    if data:
        with open(output_file, mode=mode, newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {output_file}")
    else:
        print("No data to save.")
        
def escribir_tipo_de_bloqueo_csv(archivo_salida: str, datos: list, modo: str):
    if datos:
        with open(archivo_salida, mode=modo, newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=datos[0].keys())
            if file.tell() == 0:
                writer.writeheader()
            writer.writerows(datos)
        print(f"Datos guardados en {archivo_salida}")
    else:
        print("No hay datos para guardar.")


def write_blocking_type_to_csv(output_file: str, data: list, mode: str):
    """
    Writes data to a CSV file, only writing headers if the file is empty.

    :param output_file: The output file path.
    :param data: The data to be saved (a list of dictionaries).
    :param mode: The mode in which the file is opened ('w' for write, 'a' for append).
    """
    if data:
        with open(output_file, mode=mode, newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=data[0].keys())
            if file.tell() == 0:  # Only write the header if the file is empty
                writer.writeheader()
            writer.writerows(data)
        print(f"Data saved to {output_file}")
    else:
        print("No data to save.")


def _merge_csv(input_file: str, output_file: str) -> None:
    """
    Merges a CSV file by removing duplicates based on the 'input' column.

    :param input_file: The path to the input CSV file.
    :param output_file: The path to the output CSV file.
    """
    try:
        df = pd.read_csv(input_file)
        df = df[df['input'].str.lower() != 'input']  # Exclude rows where 'input' is 'input'
        df_no_duplicates = df.drop_duplicates(subset='input', keep='first')
        df_no_duplicates[['input']].to_csv(output_file, index=False)
        
        print(f"File {input_file} processed and saved as {output_file}")
    
    except Exception as e:
        print(f"Error processing file {input_file}: {e}")


def create_file_and_path(base_dir: str, file_name: str) -> str:
    """
    Creates the directory if it doesn't exist and returns the full path of the file.

    :param base_dir: The base directory path.
    :param file_name: The name of the file.
    :return: The full path of the file.
    """
    base_dir = os.path.normpath(base_dir)
    os.makedirs(base_dir, exist_ok=True) 
    full_path = os.path.join(base_dir, file_name)
    print(f"Path created or verified: {full_path}")
    return full_path


def create_ooni_run_link(input_file: str, file_name: str, output_dir: str) -> None:
    """
    Processes the input file and saves the results to a new file in the specified directory.

    :param input_file: The input CSV file path.
    :param file_name: The name for the output file.
    :param output_dir: The directory where the output file will be saved.
    """
    output_file = create_file_and_path(output_dir, f"{file_name}.csv")
    _merge_csv(input_file, output_file)

def to_excel(csv_file, excel_file):
    df = pd.read_csv(csv_file)
    df.to_excel(excel_file, index=False)