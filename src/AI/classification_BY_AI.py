import csv
import subprocess
import re
import json

def main(archivo_ejecutable: str, archivo_entrada: str, archivo_salida: str, fila_inicio: int = 1) -> None:
    try:
        categories = ["ALDR", "REL", "PORN", "PROV", "POLR", "HUMR", "ENV", "MILX", "HATE", "NEWS", "XED", "PUBH",
                      "GMB", "ANON", "DATE", "GRP", "LGBT", "FILE", "HACK", "COMT", "MMED", "HOST", "SRCH", "GAME",
                      "CULTR", "ECON", "GOVT", "COMM", "CTRL", "IGO", "MISC"]

        with open(archivo_entrada, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        if not rows:
            print("El archivo de entrada está vacío.")
            return

        header = ["url"] + categories + ["output"]

        file_is_empty = True  
        try:
            with open(archivo_salida, "r", encoding='utf-8') as f_out:
                if f_out.read(1):  
                    file_is_empty = False
        except FileNotFoundError:
            file_is_empty = True 

        with open(archivo_salida, "a", newline='', encoding='utf-8') as f_out:
            writer = csv.writer(f_out)

            if file_is_empty:
                writer.writerow(header)  

            for i in range(1, len(rows)):
                if i < fila_inicio:
                    continue

                row = rows[i]
                url = row[0]
                print(f"Procesando fila {i}: {url}")

                result = subprocess.run(
                    ["python", archivo_ejecutable, url],
                    capture_output=True,
                    text=True
                )

                detected_categories = {cat: 0 for cat in categories}
                category_counts = {}
                
                print("Salida del script Python:")
                print(result.stdout)

                match = re.search(r'\{(.+?)\}', result.stdout, re.DOTALL)
                if match:
                    json_data = match.group(0)
                    try:
                        category_counts = json.loads(json_data.replace("'", '"'))
                        print("Datos extraídos:")
                        print(category_counts)

                        for category, count in category_counts.items():
                            if category in detected_categories:
                                detected_categories[category] = count
                    except json.JSONDecodeError:
                        print(f"Error al procesar el JSON: {json_data}")

                row_data = [url] + [detected_categories[cat] for cat in categories]

                category_output = ", ".join([cat.lower() for cat in category_counts.keys()])

                row_data.append(category_output)

                writer.writerow(row_data)

        print(f"Proceso finalizado. Resultados guardados en '{archivo_salida}'.")

    except Exception as e:
        print(f"Error: {e}")

main(
    "src/services/clasificar_url_y_contenido_service.py",
    "data/url_classification/inputs_pre_tagging.csv",
    "outputIA.csv",
    "categoriasIA_output.csv",
    fila_inicio=1
)