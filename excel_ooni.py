import pandas as pd
from urllib.parse import urlparse

file = "argentina3"
def normalizar_url(url):
    if pd.isna(url):
        return ''
    
    # Eliminar http, https, www
    url = url.replace('http://', '').replace('https://', '').replace('www.', '').strip()
    
    # Asegurarse de tener un esquema para urlparse
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    
    try:
        dominio = urlparse(url).netloc  # solo dominio base
    except Exception:
        dominio = url

    return dominio.lower().strip()

csv1 = pd.read_csv(f'csv_output/locales/{file}.csv')
csv2 = pd.read_csv('csv_output/clasification/categorizated_manual_list.csv')

# Normalizar y preparar CSV 1
csv1['dominio'] = csv1['input'].apply(normalizar_url)
csv1_filtered = csv1[['dominio', 'dns_experiment_failure', 'http_experiment_failure', 'accessible', 'resolver_asn', 'resolver_ip']].copy()
csv1_filtered.rename(columns={'accessible': 'accesible'}, inplace=True)

# Normalizar y preparar CSV 2
csv2['dominio'] = csv2['url'].apply(normalizar_url)
csv2_filtered = csv2[['dominio', 'deduccion primaria', 'deduccion secundaria']].copy()

# Merge por dominio
merged = pd.merge(csv1_filtered, csv2_filtered, how='left', on='dominio')

# Eliminar duplicados por dominio (si hay más de uno, se queda con el primero)
merged.drop_duplicates(subset='dominio', inplace=True)

# Exportar a Excel
merged.to_excel(f'excel/locales/{file}.xlsx', index=False)