import pandas as pd
from urllib.parse import urlparse

file = "Venezuela"

# Función para normalizar las URLs/dominios
def normalizar_url(url):
    if pd.isna(url):
        return ''
    url = url.replace('http://', '').replace('https://', '')
    url = url.replace('www.', '').strip().rstrip('/')
    return url

# Cargar los archivos CSV
csv1 = pd.read_csv(f'csv_output/digs/{file}.csv')
csv2 = pd.read_csv('csv_output/clasification/categorizated_manual_list.csv')

# Filtrar solo las filas donde "Bloqueado" sea "Sí"
csv1_filtrado = csv1[csv1['Bloqueado'] == "Sí"].copy()

# Crear las columnas requeridas: dominio, status, accesible (va a decir "No")
csv1_filtrado['dominio'] = csv1_filtrado['Dominio']
csv1_filtrado['status'] = csv1_filtrado['Status']
csv1_filtrado['accesible'] = "No"

# Normalizar URLs para hacer el merge
csv1_filtrado['dominio_normalizado'] = csv1_filtrado['dominio'].apply(normalizar_url)
csv2['url_normalizada'] = csv2['url'].apply(normalizar_url)

# Filtrar solo las columnas necesarias del segundo CSV
csv2_filtrado = csv2[['url_normalizada', 'deduccion primaria', 'deduccion secundaria']].copy()

# Hacer el merge por la URL normalizada
resultado = pd.merge(
    csv1_filtrado[['dominio', 'status', 'accesible', 'dominio_normalizado']],
    csv2_filtrado,
    how='left',
    left_on='dominio_normalizado',
    right_on='url_normalizada'
)

# Eliminar columnas auxiliares
resultado.drop(columns=['dominio_normalizado', 'url_normalizada'], inplace=True)

# Exportar a Excel
resultado.to_excel(f'{file}.xlsx', index=False)
