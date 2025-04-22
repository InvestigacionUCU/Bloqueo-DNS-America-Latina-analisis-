
import csv

from obtener_categorias_3.category_ooni import cetegory
from utils.query_builder import QueryBuilder


def categorias_ooni(archivo_entrada: str):
    measurement_uids = []
    query = QueryBuilder() \
        .set_base_url("https://api.ooni.io/api/v1/measurement_meta") \
        .build()
        
    with open(archivo_entrada, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            measurement_uids.append(row.get('measurement_uid', None))

    for measurement_uid in measurement_uids:
        cetegory(query, measurement_uid, archivo_entrada)
        
categorias_ooni("data/bloqueos_ooni/uruguay.csv")
