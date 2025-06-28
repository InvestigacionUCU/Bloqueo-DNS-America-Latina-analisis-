import os
import pandas as pd
from urllib.parse import urlparse

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

def juntar_inputs_sin_repetidos(directorio):
    inputs_set = set()
    
    for archivo in os.listdir(directorio):
        if archivo.endswith('.csv'):
            ruta = os.path.join(directorio, archivo)
            try:
                df = pd.read_csv(ruta)
                if 'input' in df.columns and 'accessible' in df.columns:
                    df_filtrado = df[df['accessible'] != 'NOACCESIBLEPORMETODO']
                    urls_normalizadas = df_filtrado['input'].apply(normalizar_url)
                    inputs_set.update(urls_normalizadas)
            except Exception as e:
                print(f"Error leyendo {archivo}: {e}")

    df_resultado = pd.DataFrame(sorted(inputs_set), columns=['input'])
    df_resultado.to_csv('inputs_unificados.csv', index=False)
    print("Archivo 'inputs_unificados.csv' creado con éxito.")
    
juntar_inputs_sin_repetidos('csv_output/pruebas/vpn')
