import csv
import os
from datetime import date, timedelta
import requests


def execute_query(query: str) -> dict:
    response = requests.get(query)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return {}


def filter_dns(data: dict) -> list:
    result = []
    if "results" in data:
        for item in data["results"]:
            if item.get("scores", {}).get("analysis", {}).get("blocking_type") == "dns":
                result.append(item)
    return result


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
    
    
def extraer_datos_de_todas_las_listas_ejecutadas() -> None:
    query = "https://api.ooni.org/api/v1/measurements"
    ooni_run_link_id = 10158
    start_date = date(2025, 5, 24)
    end_date = date(2025, 5, 28)

    current_date = start_date
    
    while current_date <= end_date:
        since_str = current_date.strftime("%Y-%m-%d")
        until_str = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")
            
        queryEx = f"{query}?limit=10000&failure=false&test_name=web_connectivity&since={since_str}&until={until_str}&anomaly=true&ooni_run_link_id={ooni_run_link_id}"
        data = execute_query(queryEx)   
        filtered_data = filter_dns(data)  
        save_to_csv(filtered_data, f"ooni_executation_result", output_folder="csv_output/ooni_executation_result")
        current_date += timedelta(days=1)
        
        
extraer_datos_de_todas_las_listas_ejecutadas()
