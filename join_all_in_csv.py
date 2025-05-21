import pandas as pd

# Leer archivo 1: URLs y deducción ooni
df1 = pd.read_csv("csv_output/clasification/categorizated_manual_list.csv")
df1.columns = df1.columns.str.strip()

# Leer archivo 2: Estado DNS (Dominio, Status, Bloqueado)
df2 = pd.read_csv("csv_output/digs/Cuba.csv")
df2.columns = df2.columns.str.strip()

# Leer archivo 3: Fallos DNS/HTTP/accessible
df3 = pd.read_csv("vpn/cuba_vpn.csv")
df3.columns = df3.columns.str.strip()

# Normalizar dominios
df1["dominio"] = df1["url"].str.replace("https://", "").str.replace("http://", "").str.strip().str.lower().str.rstrip("/")
df2["Dominio"] = df2["Dominio"].str.replace("https://", "").str.replace("http://", "").str.strip().str.lower().str.rstrip("/")
df3["input_normalizada"] = df3["input"].str.replace("https://", "").str.replace("http://", "").str.strip().str.lower().str.rstrip("/")

# Eliminar duplicados
df1 = df1.drop_duplicates(subset=["dominio"])
df2 = df2.drop_duplicates(subset=["Dominio"])
df3 = df3.drop_duplicates(subset=["input_normalizada"])

# Mapas de fallas y estado
df3_grouped = df3.groupby("input_normalizada").first()
mapa_fallas = df3_grouped[[
    "dns_experiment_failure",
    "http_experiment_failure",
    "accessible",
    "resolver_asn",
    "resolver_ip"
]].to_dict(orient="index")
mapa_estado = df2.set_index("Dominio")[["Status", "Bloqueado"]].to_dict(orient="index")

# Agregar columnas al df1
df1["dns_experiment_failure(OONI)"] = df1["dominio"].map(lambda x: mapa_fallas.get(x, {}).get("dns_experiment_failure", ""))
df1["http_experiment_failure(OONI)"] = df1["dominio"].map(lambda x: mapa_fallas.get(x, {}).get("http_experiment_failure", ""))

df1["accessible(OONI)"] = df1["dominio"].map(lambda x: mapa_fallas.get(x, {}).get("accessible", ""))

# Reemplazar vacíos por "NOERROR"
df1["accessible(OONI)"] = df1["accessible(OONI)"].astype(str).str.strip().replace(
    {"": "SI", "False": "NO", "false": "NO", "True": "SI", "true": "SI"}
)

df1["resolver_asn(OONI)"] = df1["dominio"].map(lambda x: mapa_fallas.get(x, {}).get("resolver_asn", ""))
df1["resolver_ip(OONI)"] = df1["dominio"].map(lambda x: mapa_fallas.get(x, {}).get("resolver_ip", ""))

df1["Status(DIG)"] = df1["dominio"].map(lambda x: mapa_estado.get(x, {}).get("Status", ""))
df1["accessible(DIG)"] = df1["dominio"].map(lambda x: mapa_estado.get(x, {}).get("Bloqueado", ""))

df1["accessible(DIG)"] = df1["accessible(DIG)"].astype(str).str.strip().replace(
    {"SI": "NO", "Si": "NO", "Sí": "NO", "NO": "SI", "No": "SI"}
)
df1["deduccion primaria"] = df1["deduccion primaria"].fillna("").replace("", "SIN DEDUCCION")
df1["deduccion secundaria"] = df1["deduccion secundaria"].fillna("").replace("", "SIN DEDUCCION")

# Limpiar URLs
df1["url"] = df1["url"].str.replace("https://", "").str.replace("http://", "").str.strip().str.lower().str.rstrip("/")


# Exportar con columnas renombradas y en orden deseado
df1[[  
    "url",
    "accessible(OONI)",
    "accessible(DIG)",
    "dns_experiment_failure(OONI)",
    "http_experiment_failure(OONI)",
    "Status(DIG)",
    "resolver_asn(OONI)",
    "resolver_ip(OONI)",
    "deduccion primaria",
    "deduccion secundaria"
]].to_csv("cuba_vpn_result.csv", index=False)


df = pd.read_csv('cuba_vpn_result.csv')
df.to_excel('cuba_vpn.xlsx', index=False)
