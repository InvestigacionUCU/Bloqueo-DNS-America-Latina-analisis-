import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
import csv
import urllib3
import re

headers = [header.lower() for header in ["ALDR", "REL", "PORN", "PROV", "POLR", "HUMR", "ENV", "MILX", "HATE", "NEWS", "XED", "PUBH",
                "GMB", "ANON", "DATE", "GRP", "LGBT", "FILE", "HACK", "COMT", "MMED", "HOST", "SRCH", "GAME",
                "CULTR", "ECON", "GOVT", "COMM", "CTRL", "IGO", "MISC"]]


def eliminar_urls_duplicadas(archivo):
    df = pd.read_csv(archivo)
    df_sin_duplicados = df.drop_duplicates(subset=['url'])
    df_sin_duplicados.to_csv(archivo, index=False)


def fetch_text(url, max_reintentos=2, espera=5):
    intentos = 0 

    headers = {    
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "es-ES,en;q=0.9",
        "Connection": "keep-alive",
    }

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    session = requests.Session()
    session.headers.update(headers)

    while intentos < max_reintentos:
        try:
            r = session.get(url, timeout=30, verify=False)
            r.raise_for_status()
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()
            texto = ' '.join(soup.get_text().split()).strip()
            return texto
        except requests.exceptions.RequestException as e:
            intentos += 1
            print(f"Error al obtener la URL ({intentos}/{max_reintentos}): {e}")
            if intentos < max_reintentos:
                time.sleep(espera)

    return None


def fetch_tags(tags_csv_path):
    dic = {}
    with open(tags_csv_path, 'r', encoding='utf-8', newline='') as archivo_tags:
        reader = csv.reader(archivo_tags)
        next(reader)
        for row in reader:
            code = row[0].strip().lower()
            tags = [tag.strip().lower() for tag in row[1].split(',')] 
            dic[code] = tags
        
    return dic


def clasify_web(web, categories, url):
    categories_found = {}
    words = []
    for category, tags in categories.items():
        for tag in tags:
            count_web = len(re.findall(rf"\b{re.escape(tag)}\b", web, re.IGNORECASE))
            count_url = len(re.findall(re.escape(tag), url, re.IGNORECASE))

            total_count = count_web + count_url

            if total_count > 0:
                categories_found[category] = categories_found.get(category, 0) + total_count
                words.append(tag)
    return categories_found, words


def save_csv(clasification, url, archivo_output):
    dic = clasification[0]
    words = clasification[1]
    escribir_header = not os.path.exists(archivo_output)
    header = ['url', 'palabras encontradas'] + headers + ['deduccion']
    with open(archivo_output, 'a', encoding='utf-8', newline='') as archivo_clasificacion:
        writer = csv.writer(archivo_clasificacion)
        
        if escribir_header:
            writer.writerow(header)
            
        writer.writerow([url, words] + [dic.get(head, 0) for head in headers] + [deduccion(dic)])    
        
    
def deduccion(dic):
    if not dic:
        return None
    
    sorted_items = sorted(dic.items(), key=lambda x: x[1], reverse=True)
    max_value = sorted_items[0][1]
    max_categories = [key for key, value in sorted_items if value == max_value]
    
    if len(max_categories) >= 2:
        return max_categories
    
    return [sorted_items[0][0], sorted_items[1][0]] if len(sorted_items) > 1 else [sorted_items[0][0]]


def main(tags_csv, archivo_input, archivo_output):
    with open(archivo_input, 'r', encoding='utf-8') as entrada:
        reader = csv.reader(entrada)
        next(reader)
        urls = [row[0] for row in reader]
        tags = fetch_tags(tags_csv)
        for url in urls:
            web = fetch_text(url)
                
            if web is None:
                web = ""

            print(f'Procesando la URL: {url}')
            clasification = clasify_web(web, tags, url)
            save_csv(clasification, url, archivo_output)
                
                
main(
    'csv_output/tags.csv',
    'csv_output/clasification/list_pre_clasification_manual.csv',
    'csv_output/clasification/categorizated_manual_list.csv'
)
