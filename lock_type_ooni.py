
import csv
import os

import requests

def execute_query(query: str) -> dict:
    response = requests.get(query)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return {}


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
        

def save_to_csv(data: list, label: str, output_folder: str = "csv_output") -> None:
    if not data:
        print("No hay datos para guardar.")
        return

    os.makedirs(output_folder, exist_ok=True)
    file_name = f"{output_folder}/{label}.csv"

    headers = list(data[0].keys())

    with open(file_name, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    print(f"Archivo guardado: {file_name}")
    
    
def lock_type(archivo_entrada: str):
    query = "https://api.ooni.org/api/v1/raw_measurement"
    measurement_uids = []
    with open(archivo_entrada, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            measurement_uids.append(row.get('measurement_uid', None))

    for measurement_uid in measurement_uids:
        if measurement_uid:
            queryEx = f"{query}?measurement_uid={measurement_uid}"
            data = execute_query(queryEx)
            
        if not data:
            print(f"No se pudieron obtener datos")
            return
        
        test_keys = data.get("test_keys", {})
        control = test_keys.get("control", {})
        http_request = control.get("http_request", {})

        row = {
            "measurement_uid": measurement_uid or "None",
            "input": data.get("input", "None"),
            "dns_experiment_failure": test_keys.get("dns_experiment_failure", "None")  or "None",
            "http_experiment_failure": test_keys.get("http_experiment_failure", "None")  or "None",
            "dns_consistency": test_keys.get("dns_consistency", "None")  or "None",
            "accessible": test_keys.get("accessible", "None"),
            "resolver_asn": data.get("resolver_asn", "None"),
            "resolver_ip": data.get("resolver_ip", "None"),
            "status_code": http_request.get("status_code", "None")
        }
        
        for key, value in row.items():
            """  quiero que por cada valor diferente en la linea de resolver_ip escriba en un archivo diferente"""
            if key == "resolver_ip":
                path = f"csv_output/lists/{value}.csv"
                escribir_tipo_de_bloqueo_csv(path, [row], "a")
                
lock_type("csv_output/ooni_executation_result/ooni_executation_result.csv")
