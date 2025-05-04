import csv
import os
import requests
import pandas as pd


def filter_dns(data: dict) -> list:
    result = []
    if "results" in data:
        for item in data["results"]:
            if item.get("scores", {}).get("analysis", {}).get("blocking_type") == "dns":
                result.append(item)
    return result


def remove_duplicates(data: list) -> list:
    seen_inputs = set()
    result = []

    for item in data:
        input_value = item.get("input")
        if input_value not in seen_inputs:
            result.append(item)
            seen_inputs.add(input_value)

    return result


def get_month_range(year: int, month: int) -> tuple:
    start_date = f"{year}-{month:02d}-01"
    if month == 2:
        end_date = f"{year}-{month:02d}-28"
    elif month in [4, 6, 9, 11]:
        end_date = f"{year}-{month:02d}-30"
    else:
        end_date = f"{year}-{month:02d}-31"
    return start_date, end_date


def execute_query(query: str) -> dict:
    response = requests.get(query)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return {}


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


def get_data(since: int = 2023, until: int = 2025) -> None:
    countries: list = ["UY", "VE", "HN", "AR", "CU", "SV", "NI", "GT"]
    query ="https://api.ooni.org/api/v1/measurements"
    for country in countries:
        while since <= until:
            for month in range(1, 13):
                if since == 2025 and month == 2:
                    break
                i, f = get_month_range(since, month)
                queryEx = f"{query}?limit=2000&failure=false&probe_cc={country}&test_name=web_connectivity&since={i}&until={f}&anomaly=true"
                
                data = execute_query(queryEx)   
                filtered_data = remove_duplicates(filter_dns(data))    
                save_to_csv(filtered_data, f"historical_data", output_folder="csv_output/historical_data")
                       
            since += 1
        since = 2023
        

def delete_duplicates():
    df = pd.read_csv("csv_output/historical_data/historical_data.csv")
    df_limpio = df.drop_duplicates(subset="input")
    df_limpio.to_csv("csv_output/historical_data/historical_data.csv", index=False)

get_data()
delete_duplicates()