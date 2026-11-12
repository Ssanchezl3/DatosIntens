"""
SI3008 - Grupo 4
Script 0: Generación de un dataset SINTÉTICO de taxis amarillos NYC (enero 2026)
que reproduce las propiedades verificadas del archivo oficial.

IMPORTANTE PARA EL/LA ESTUDIANTE:
-----------------------------------
La docente entrega el archivo real `yellow_tripdata_2026-01.parquet`.
Si ya lo tienes, OMITE este script y usa el archivo real.
Este generador sirve para que el notebook sea ejecutable de principio a fin
aunque todavía no tengas el archivo oficial. Documenta la semilla (SEED=2026)
en la bitácora si usas datos sintéticos.

Propiedades que reproduce (Anexo A del enunciado):
- ~3.72M registros, 20 columnas (aquí usamos una muestra reducida por memoria)
- columna cbd_congestion_fee con valores {0.75, 0.00, -0.75}
- patrón de nulos ligado a payment_type == 0 (~29.2%)
- algunos fare_amount <= 0, trip_distance <= 0, trip_distance > 100
- rango de fechas que desborda levemente el mes
"""
import numpy as np
import pandas as pd

SEED = 2026
rng = np.random.default_rng(SEED)

# Muestra reducida para que corra en Colab/entornos con poca RAM.
# Para el trabajo real usa el archivo completo de la docente.
N = 200_000

# --- Zonas (PULocationID / DOLocationID) 1..263 como en la TLC ---
zones = np.arange(1, 264)
pu = rng.choice(zones, size=N)
do = rng.choice(zones, size=N)

# --- Fechas dentro de enero 2026, con un pequeño desborde a dic-2025 y feb-2026 ---
base = pd.Timestamp("2026-01-01")
offsets_min = rng.integers(-180, 44700, size=N)  # minutos; algunos negativos => dic 2025
pickup = (base + pd.to_timedelta(offsets_min, unit="m")).to_numpy()
duration_min = rng.gamma(shape=2.0, scale=7.0, size=N) + 1  # duración viaje
dropoff = pickup + pd.to_timedelta(duration_min, unit="m").to_numpy()

# Inyectar 1 registro con dropoff < pickup (como el hallazgo oficial)
dropoff[0] = pickup[0] - pd.Timedelta(minutes=5).to_timedelta64()

# --- Medidas del viaje ---
trip_distance = np.round(rng.gamma(shape=2.0, scale=1.8, size=N), 2)
fare_amount = np.round(3.0 + trip_distance * rng.uniform(2.5, 3.5, size=N), 2)

# Inyectar anomalías
neg_fare_idx = rng.choice(N, size=int(N*0.011), replace=False)   # ~1.1% fare<=0
fare_amount[neg_fare_idx] = -np.abs(fare_amount[neg_fare_idx])
zero_dist_idx = rng.choice(N, size=int(N*0.034), replace=False)  # ~3.4% dist<=0
trip_distance[zero_dist_idx] = 0.0
far_idx = rng.choice(N, size=int(N*0.00004)+1, replace=False)    # muy pocos >100 millas
trip_distance[far_idx] = rng.uniform(101, 150, size=len(far_idx))

# --- payment_type: 0 marca el subgrupo con nulos (~29.2%) ---
payment_type = rng.choice([1, 2, 3, 4], size=N, p=[0.68, 0.27, 0.03, 0.02]).astype(float)
null_mask = rng.random(N) < 0.292
payment_type[null_mask] = 0.0

# Columnas que se vuelven nulas cuando payment_type == 0
passenger_count = rng.integers(1, 6, size=N).astype(float)
RatecodeID = rng.choice([1, 2, 3, 4, 5], size=N, p=[0.9, 0.04, 0.03, 0.02, 0.01]).astype(float)
store_and_fwd_flag = np.where(rng.random(N) < 0.02, "Y", "N").astype(object)
congestion_surcharge = np.round(rng.choice([0.0, 2.5], size=N, p=[0.2, 0.8]), 2)
Airport_fee = np.round(rng.choice([0.0, 1.75], size=N, p=[0.9, 0.1]), 2)

for col in [passenger_count, RatecodeID, congestion_surcharge, Airport_fee]:
    col[null_mask] = np.nan
store_and_fwd_flag = np.where(null_mask, None, store_and_fwd_flag)

# --- cbd_congestion_fee: {0.75, 0.00, -0.75} con proporciones del Anexo A ---
cbd = rng.choice([0.75, 0.00, -0.75], size=N, p=[0.70, 0.293, 0.007])

# --- Otras columnas monetarias para completar 20 columnas ---
VendorID = rng.choice([1, 2], size=N).astype("int64")
extra = np.round(rng.choice([0.0, 0.5, 1.0], size=N), 2)
mta_tax = np.full(N, 0.5)
tip_amount = np.where(payment_type == 1,
                      np.round(fare_amount * rng.uniform(0.0, 0.3, size=N), 2), 0.0)
tolls_amount = np.round(rng.choice([0.0, 6.55], size=N, p=[0.95, 0.05]), 2)
improvement_surcharge = np.full(N, 1.0)
total_amount = np.round(
    np.nan_to_num(fare_amount) + extra + mta_tax + tip_amount + tolls_amount +
    improvement_surcharge + np.nan_to_num(congestion_surcharge) +
    np.nan_to_num(Airport_fee) + cbd, 2)

df = pd.DataFrame({
    "VendorID": VendorID,
    "tpep_pickup_datetime": pickup,
    "tpep_dropoff_datetime": dropoff,
    "passenger_count": passenger_count,
    "trip_distance": trip_distance,
    "RatecodeID": RatecodeID,
    "store_and_fwd_flag": store_and_fwd_flag,
    "PULocationID": pu.astype("int64"),
    "DOLocationID": do.astype("int64"),
    "payment_type": payment_type,
    "fare_amount": fare_amount,
    "extra": extra,
    "mta_tax": mta_tax,
    "tip_amount": tip_amount,
    "tolls_amount": tolls_amount,
    "improvement_surcharge": improvement_surcharge,
    "total_amount": total_amount,
    "congestion_surcharge": congestion_surcharge,
    "Airport_fee": Airport_fee,
    "cbd_congestion_fee": cbd,
})

df.to_parquet("datos/yellow_tripdata_2026-01_sintetico.parquet", index=False)
print(f"Dataset generado: {len(df):,} filas x {df.shape[1]} columnas")
print(f"Nulos en payment_type==0: {(payment_type==0).sum():,} ({(payment_type==0).mean()*100:.1f}%)")
print(df["cbd_congestion_fee"].value_counts())

# --- Tabla de zonas (taxi zone lookup) ---
boroughs = ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island", "EWR"]
zone_df = pd.DataFrame({
    "LocationID": zones,
    "Borough": rng.choice(boroughs, size=len(zones), p=[0.4, 0.2, 0.2, 0.12, 0.07, 0.01]),
    "Zone": [f"Zone_{i}" for i in zones],
    "service_zone": rng.choice(["Yellow Zone", "Boro Zone", "Airports", "EWR"], size=len(zones)),
})
zone_df.to_csv("datos/taxi_zone_lookup.csv", index=False)
print(f"\nTabla de zonas: {len(zone_df)} zonas")
