import csv
from utils.query import Query
from utils.query_metadata import QueryMetadata
from utils.csv_utils import create_file_and_path
from utils.fetch_data import fetch_data

def cetegory(query: Query, archivo_entrada: str) -> None:
    with open(archivo_entrada, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            measurement_uid = row.get('measurement_uid', None)
            try:
                query_Metadata = QueryMetadata(query)
                query_Metadata = query_Metadata.QueryMetadata(measurement_uid)
                data = fetch_data(query_Metadata)
                if not data:
                    print(f"No se pudieron obtener datos")
                    return

                row = {
                    "measurement_uid": measurement_uid or "None",
                    "input": data.get("input", "None"),
                    "category_code": data.get("category_code", "None")
                }
                
                """ escribir un un archivo salida csv con las columnas de row"""
                output_file = create_file_and_path(archivo_entrada, "categorias_ooni")
                
                


            except Exception as e:
                print(f"Error al obtener datos: {e}")