import pandas as pd
from urllib.parse import urlparse

file = "venezuela_vpn"

# Función para extraer el dominio base (ej: www.facebook.com → facebook.com)
def extraer_dominio_base(url):
    if pd.isna(url):
        return ''
    try:
        url = url.strip().lower()
        if not url.startswith('http'):
            url = 'http://' + url
        netloc = urlparse(url).netloc or urlparse('http://' + url).path
        netloc = netloc.replace('www.', '')
        partes = netloc.split('.')
        if len(partes) >= 2:
            return '.'.join(partes[-2:])  # Ej: 1xbet.com, facebook.com
        else:
            return netloc
    except:
        return ''

# Leer CSVs
csv1 = pd.read_csv(f'csv_output/pruebas/vpn/{file}.csv')
csv2 = pd.read_csv('csv_output/clasification/manual_vpn.csv')

# Normalizar y agregar columnas
csv1['input_normalizado'] = csv1['input'].str.replace('https://', '', regex=False)\
                                        .str.replace('http://', '', regex=False)\
                                        .str.replace('www.', '', regex=False)\
                                        .str.rstrip('/')
csv1['dominio_base'] = csv1['input'].apply(extraer_dominio_base)
csv2['dominio_base'] = csv2['input'].apply(lambda x: extraer_dominio_base(str(x)))

# ❗ Agrupar csv2 para quedarnos con una deducción por dominio base
csv2_cleaned = csv2.groupby('dominio_base')['deduccion'].agg(
    lambda x: x.mode().iloc[0] if not x.mode().empty else x.iloc[0]
).reset_index()

# Filtrar columnas necesarias
csv1_filtered = csv1[['input_normalizado', 'dominio_base', 'dns_experiment_failure',
                      'http_experiment_failure', 'accessible', 'resolver_asn',
                      'resolver_ip', 'status_code']].copy()
csv1_filtered.rename(columns={'accessible': 'accesible'}, inplace=True)
csv2_filtered = csv2_cleaned[['dominio_base', 'deduccion']].copy()

# Merge por dominio base
merged = pd.merge(csv1_filtered, csv2_filtered, how='left', on='dominio_base')

# Rellenar deducciones faltantes
merged['deduccion'] = merged['deduccion'].fillna('NO_CLASIFICADO')

# Eliminar duplicados exactos de input_normalizado (con rutas distintas permitidas)
merged = merged.drop_duplicates(subset='input_normalizado', keep='first')

# Exportar a Excel
merged.to_excel(f'excel/por manual/vpn/{file}.xlsx', index=False)

# Vista previa
print(merged[['input_normalizado', 'dominio_base', 'deduccion']].head())
