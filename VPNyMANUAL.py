import pandas as pd

# Leer el archivo CSV principal (el que tiene solo 'input')
df1 = pd.read_csv('inputs_unificados.csv')  # reemplazá con el nombre real
# Leer el archivo CSV con deducciones
df2 = pd.read_csv('csv_output/clasification/manual.csv')  # reemplazá con el nombre real

# Asegurarse de que las columnas relevantes se llamen igual para hacer merge
# Normalizar por si hay espacios o letras mayúsculas
df1['input'] = df1['input'].str.strip().str.lower()
df2['input'] = df2['input'].str.strip().str.lower()

# Hacemos el merge con left join para mantener todos los del primer archivo
df_merged = df1.merge(df2[['input', 'deduccion']], on='input', how='left')

# Guardamos el resultado
df_merged.to_csv('archivo_salida.csv', index=False)
print("Archivo generado: archivo_salida.csv")
