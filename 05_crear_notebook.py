"""Crea el notebook Grupo4_esquema_estrella.ipynb a partir de los scripts del Rol A."""
import json

def code(src): return {"cell_type":"code","metadata":{},"execution_count":None,"outputs":[],"source":src.splitlines(keepends=True)}
def md(src): return {"cell_type":"markdown","metadata":{},"source":src.splitlines(keepends=True)}

cells = [
 md("# SI3008 — Grupo 4\n"
    "## Del modelo entidad-relación al esquema estrella en un lago de datos\n\n"
    "**Rol A — Modelador/a de datos.** Este notebook construye el esquema estrella, lo "
    "materializa en Parquet (plano y particionado) y CSV, y valida la integridad referencial.\n\n"
    "> Si tienes el archivo oficial `yellow_tripdata_2026-01.parquet`, colócalo en `datos/`. "
    "Si no, ejecuta primero la celda del generador sintético (semilla 2026)."),
 md("### 0. Dependencias"),
 code("# !pip install pandas pyarrow matplotlib numpy\nimport os, numpy as np, pandas as pd\nos.makedirs('datos', exist_ok=True)"),
 md("### 1. (Opcional) Generar datos sintéticos si no tienes el archivo oficial"),
 code(open("01_generar_datos.py").read()),
 md("### 2. Construcción del esquema estrella, materialización y validación"),
 code(open("02_esquema_estrella.py").read()),
 md("### 3. Diagramas y gráficos"),
 code(open("03_diagramas.py").read()),
 md("### 4. Verificación rápida de las tablas resultantes"),
 code("import pandas as pd\n"
      "print('dim_tiempo:'); display(pd.read_parquet('lago/star/dim_tiempo.parquet').head())\n"
      "print('dim_zona:');   display(pd.read_parquet('lago/star/dim_zona.parquet').head())\n"
      "print('fct_viajes:'); display(pd.read_parquet('lago/star/fct_viajes_parquet/fct_viajes.parquet').head())"),
]
nb = {"cells":cells,"metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
      "language_info":{"name":"python","version":"3.11"}},"nbformat":4,"nbformat_minor":5}
json.dump(nb, open("informe/Grupo4_esquema_estrella.ipynb","w"), ensure_ascii=False, indent=1)
print("Notebook creado: informe/Grupo4_esquema_estrella.ipynb")
