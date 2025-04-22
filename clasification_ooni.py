import csv
import requests


def execute_query(query: str) -> dict:
    response = requests.get(query)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return {}


def categorias_ooni(archivo_entrada: str):
    query = "https://api.ooni.io/api/v1/measurement_meta"
    with open(archivo_entrada, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            measurement_uid = row.get('measurement_uid', None)
            try:
                data = f"{query}?measurement_uid={measurement_uid}"
                data = execute_query(data)
                if not data:
                    print(f"No se pudieron obtener datos")
                    continue

                row = {
                    "measurement_uid": measurement_uid or "None",
                    "input": data.get("input", "None"),
                    "category_code": data.get("category_code", "None")
                }
                
                with open("csv_output/categorizated_ooni.csv", mode='a', newline='', encoding='utf-8') as output_csv:
                    fieldnames = ["measurement_uid", "input", "category_code"]
                    writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
                    if output_csv.tell() == 0: 
                        writer.writeheader()
                    writer.writerow(row)
                    
            except Exception as e:
                print(f"Error al obtener datos: {e}")
    

        
categorias_ooni("csv_output/global_list_to_clasification_ooni.csv")
