import os
from utils.query_builder import QueryBuilder
from obtener_mediciones_ooni_1.get_global_list import get_global_list
from datetime import date, timedelta

query_db = "https://api.ooni.org/api/v1/measurements"

def extraer_datos_de_todas_las_listas_ejecutadas() -> None:
    file_path = "data/lista_global.csv"
    if os.path.exists(file_path):
        os.remove(file_path)

    start_date = date(2025, 4, 19)
    end_date = date(2025, 4, 20)

    current_date = start_date
    
    while current_date <= end_date:
        since_str = current_date.strftime("%Y-%m-%d")
        until_str = (current_date + timedelta(days=1)).strftime("%Y-%m-%d")

        query_builder = QueryBuilder() \
            .set_base_url(query_db) \
            .set_test_name("web_connectivity") \
            .set_since(since_str) \
            .set_until(until_str) \
            .set_ooni_run_link_id("10158") \
            .build()

        get_global_list(query_builder, 10000, True, "data", "lista_global", "a", False)

        current_date += timedelta(days=1)
        
extraer_datos_de_todas_las_listas_ejecutadas()
