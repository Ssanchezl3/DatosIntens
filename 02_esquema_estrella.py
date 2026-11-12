"""
SI3008 - Grupo 4  -  ROL A (Modelador/a de datos)
Script 1: Del modelo entidad-relacion al esquema estrella.

Construye, a partir del dataset de taxis:
  - dim_tiempo   (granularidad: hora, NO por marca de tiempo exacta)
  - dim_zona     (desde taxi_zone_lookup)
  - dim_pago     (catalogo de payment_type)
  - dim_tarifa   (catalogo de RatecodeID)
  - fct_viajes   (tabla de hechos, grano = 1 viaje)
Materializa todo en Parquet y genera una version PARTICIONADA por dia.
Valida la integridad referencial.
"""
import os
import pandas as pd
import numpy as np

os.makedirs("lago/bronze", exist_ok=True)
os.makedirs("lago/star", exist_ok=True)
os.makedirs("lago/star/fct_viajes_parquet", exist_ok=True)
os.makedirs("lago/star/fct_viajes_particionado", exist_ok=True)
os.makedirs("lago/csv", exist_ok=True)

# ---------------------------------------------------------------
# 1. Cargar datos
# ---------------------------------------------------------------
# Usa el archivo oficial si existe; si no, el sintetico.
RUTA_OFICIAL = "datos/yellow_tripdata_2026-01.parquet"
RUTA_SINT = "datos/yellow_tripdata_2026-01_sintetico.parquet"
ruta = RUTA_OFICIAL if os.path.exists(RUTA_OFICIAL) else RUTA_SINT
print(f"Cargando: {ruta}")
df = pd.read_parquet(ruta)
zonas = pd.read_csv("datos/taxi_zone_lookup.csv")
print(f"  {len(df):,} viajes | {df.shape[1]} columnas")

# ---------------------------------------------------------------
# 2. Limpieza minima (consistencia basica antes de modelar)
#    - dropoff >= pickup
#    - solo viajes dentro de enero 2026
# ---------------------------------------------------------------
df = df[df["tpep_dropoff_datetime"] >= df["tpep_pickup_datetime"]]
mes = (df["tpep_pickup_datetime"] >= "2026-01-01") & (df["tpep_pickup_datetime"] < "2026-02-01")
df = df[mes].reset_index(drop=True)
print(f"  Tras limpieza temporal: {len(df):,} viajes")

# ===============================================================
# PASO 1 del esquema estrella: GRANO DEL HECHO
#   Grano = un (1) viaje de taxi.  -> 1 fila en fct_viajes por viaje.
# ===============================================================

# ===============================================================
# PASO 2: DIMENSIONES   (tiempo, zona, pago, tarifa)
# PASO 3: GRANULARIDAD de cada dimension
# PASO 4: CLAVES FORANEAS
# ===============================================================

# ---- dim_tiempo (granularidad = HORA) -------------------------
# Justificacion: el analisis de demanda se hace por hora/dia/dow.
# No se crea una fila por timestamp exacto porque multiplicaria el
# tamano de la dimension sin aportar valor analitico.
horas = pd.date_range("2026-01-01", "2026-02-01", freq="h", inclusive="left")
dim_tiempo = pd.DataFrame({"hora_ts": horas})
dim_tiempo["tiempo_id"] = (dim_tiempo["hora_ts"].dt.strftime("%Y%m%d%H")).astype("int64")
dim_tiempo["fecha"] = dim_tiempo["hora_ts"].dt.date.astype("string")
dim_tiempo["anio"] = dim_tiempo["hora_ts"].dt.year.astype("int16")
dim_tiempo["mes"] = dim_tiempo["hora_ts"].dt.month.astype("int8")
dim_tiempo["dia"] = dim_tiempo["hora_ts"].dt.day.astype("int8")
dim_tiempo["hora"] = dim_tiempo["hora_ts"].dt.hour.astype("int8")
dim_tiempo["dia_semana"] = dim_tiempo["hora_ts"].dt.dayofweek.astype("int8")  # 0=lunes
dim_tiempo["nombre_dia"] = dim_tiempo["hora_ts"].dt.day_name()
dim_tiempo["es_fin_semana"] = dim_tiempo["dia_semana"].isin([5, 6])
dim_tiempo["franja"] = pd.cut(dim_tiempo["hora"],
                              bins=[-1, 5, 11, 17, 21, 23],
                              labels=["Madrugada", "Mañana", "Tarde", "Noche", "Noche"],
                              ordered=False).astype("string")

# ---- dim_zona -------------------------------------------------
dim_zona = zonas.rename(columns={"LocationID": "zona_id",
                                 "Borough": "distrito",
                                 "Zone": "zona",
                                 "service_zone": "zona_servicio"}).copy()
dim_zona["zona_id"] = dim_zona["zona_id"].astype("int64")

# ---- dim_pago -------------------------------------------------
dim_pago = pd.DataFrame({
    "pago_id": [0, 1, 2, 3, 4, 5, 6],
    "metodo_pago": ["Desconocido/No reportado", "Tarjeta de crédito", "Efectivo",
                    "Sin cargo", "Disputa", "Desconocido", "Viaje anulado"],
})

# ---- dim_tarifa (RatecodeID) ----------------------------------
dim_tarifa = pd.DataFrame({
    "tarifa_id": [1, 2, 3, 4, 5, 6, 99],
    "tipo_tarifa": ["Tarifa estándar", "JFK", "Newark", "Nassau/Westchester",
                    "Tarifa negociada", "Viaje compartido", "Nulo/Desconocido"],
})

# ===============================================================
# TABLA DE HECHOS: fct_viajes (grano = 1 viaje)
# ===============================================================
fct = pd.DataFrame()
# claves foraneas
fct["tiempo_id"] = (df["tpep_pickup_datetime"].dt.strftime("%Y%m%d%H")).astype("int64")
fct["zona_pu_id"] = df["PULocationID"].astype("int64")
fct["zona_do_id"] = df["DOLocationID"].astype("int64")
fct["pago_id"] = df["payment_type"].fillna(0).astype("int64")
fct["tarifa_id"] = df["RatecodeID"].fillna(99).astype("int64")
# medidas (hechos aditivos)
fct["trip_distance"] = df["trip_distance"].astype("float32")
fct["fare_amount"] = df["fare_amount"].astype("float32")
fct["tip_amount"] = df["tip_amount"].astype("float32")
fct["tolls_amount"] = df["tolls_amount"].astype("float32")
fct["total_amount"] = df["total_amount"].astype("float32")
fct["cbd_congestion_fee"] = df["cbd_congestion_fee"].astype("float32")
fct["passenger_count"] = df["passenger_count"].astype("float32")
# para particionar
fct["fecha"] = df["tpep_pickup_datetime"].dt.date.astype("string")

# ===============================================================
# VALIDACION DE INTEGRIDAD REFERENCIAL
# ===============================================================
def validar(fk_col, dim_col, dim_df, nombre):
    faltantes = set(fct[fk_col].unique()) - set(dim_df[dim_col].unique())
    ok = len(faltantes) == 0
    print(f"  [{'OK ' if ok else 'FALLA'}] {nombre}: "
          f"{'integridad referencial correcta' if ok else f'claves huerfanas: {faltantes}'}")
    return ok

print("\nValidacion de integridad referencial:")
validar("tiempo_id", "tiempo_id", dim_tiempo, "fct.tiempo_id -> dim_tiempo")
validar("zona_pu_id", "zona_id", dim_zona, "fct.zona_pu_id -> dim_zona")
validar("zona_do_id", "zona_id", dim_zona, "fct.zona_do_id -> dim_zona")
validar("pago_id", "pago_id", dim_pago, "fct.pago_id -> dim_pago")
validar("tarifa_id", "tarifa_id", dim_tarifa, "fct.tarifa_id -> dim_tarifa")

# ===============================================================
# MATERIALIZACION EN PARQUET  (3 configuraciones para el Rol B)
# ===============================================================
# (a) dimensiones
dim_tiempo.drop(columns=["hora_ts"]).to_parquet("lago/star/dim_tiempo.parquet", index=False)
dim_zona.to_parquet("lago/star/dim_zona.parquet", index=False)
dim_pago.to_parquet("lago/star/dim_pago.parquet", index=False)
dim_tarifa.to_parquet("lago/star/dim_tarifa.parquet", index=False)

# (b) hechos - Parquet SIN particion
fct.drop(columns=["fecha"]).to_parquet(
    "lago/star/fct_viajes_parquet/fct_viajes.parquet", index=False)

# (c) hechos - Parquet PARTICIONADO por dia
fct.to_parquet("lago/star/fct_viajes_particionado",
               partition_cols=["fecha"], index=False)

# (d) hechos - CSV (para comparar costo de escaneo en Athena)
fct.drop(columns=["fecha"]).to_csv("lago/csv/fct_viajes.csv", index=False)

print("\nTablas materializadas en lago/star/ (Parquet) y lago/csv/ (CSV).")
print("Particiones creadas (por dia):",
      len([d for d in os.listdir('lago/star/fct_viajes_particionado') if d.startswith('fecha=')]))

# ---------------------------------------------------------------
# Resumen de tamanos (alimenta la tabla del informe)
# ---------------------------------------------------------------
def tam(path):
    if os.path.isfile(path):
        return os.path.getsize(path)
    total = 0
    for root, _, files in os.walk(path):
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
    return total

print("\nTamanos en disco:")
for etq, p in [("fct CSV", "lago/csv/fct_viajes.csv"),
               ("fct Parquet (sin particion)", "lago/star/fct_viajes_parquet"),
               ("fct Parquet (particionado)", "lago/star/fct_viajes_particionado")]:
    print(f"  {etq:32s}: {tam(p)/1e6:8.2f} MB")

# Guardar metricas para el informe / graficos
metr = {
    "n_viajes": len(fct),
    "n_dim_tiempo": len(dim_tiempo),
    "n_dim_zona": len(dim_zona),
    "csv_mb": tam("lago/csv/fct_viajes.csv")/1e6,
    "parquet_mb": tam("lago/star/fct_viajes_parquet")/1e6,
    "parquet_part_mb": tam("lago/star/fct_viajes_particionado")/1e6,
}
pd.Series(metr).to_json("lago/metricas.json")
print("\nMetricas guardadas en lago/metricas.json")
