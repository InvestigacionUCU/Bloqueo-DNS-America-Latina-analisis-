
import csv

from obtener_categorias_3.category_ooni import cetegory
from utils.query_builder import QueryBuilder


def categorias_ooni(archivo_entrada: str):
    query = QueryBuilder() \
        .set_base_url("https://api.ooni.io/api/v1/measurement_meta") \
        .build()
        
    cetegory(query, archivo_entrada)
        
categorias_ooni("data/global/global.csv")
