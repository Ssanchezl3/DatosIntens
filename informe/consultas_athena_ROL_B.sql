-- =====================================================================
-- SI3008 - Grupo 4  -  ROL B (Ingeniero/a de plataforma en la nube)
-- Consultas de Athena listas para usar.
-- Reemplaza  <BUCKET>  por el nombre de tu bucket de S3
-- y  <DB>  por el nombre de tu base de datos de Glue (p. ej. taxi_db).
-- =====================================================================

-- ---------------------------------------------------------------------
-- PASO 1. Crear la base de datos (si el Crawler no la creo)
-- ---------------------------------------------------------------------
CREATE DATABASE IF NOT EXISTS taxi_db;

-- ---------------------------------------------------------------------
-- PASO 2. (Opcional) Tablas externas manuales si NO usas Glue Crawler.
--         Si usas el Crawler, el catalogo se crea solo; salta al PASO 3.
-- ---------------------------------------------------------------------

-- Tabla de hechos en PARQUET PARTICIONADO por dia
CREATE EXTERNAL TABLE IF NOT EXISTS taxi_db.fct_viajes_part (
  tiempo_id BIGINT, zona_pu_id BIGINT, zona_do_id BIGINT,
  pago_id BIGINT, tarifa_id BIGINT,
  trip_distance FLOAT, fare_amount FLOAT, tip_amount FLOAT,
  tolls_amount FLOAT, total_amount FLOAT, cbd_congestion_fee FLOAT,
  passenger_count FLOAT
)
PARTITIONED BY (fecha STRING)
STORED AS PARQUET
LOCATION 's3://<BUCKET>/star/fct_viajes_particionado/';
-- Cargar las particiones:
MSCK REPAIR TABLE taxi_db.fct_viajes_part;

-- Dimensiones (ajusta LOCATION a tus rutas reales)
CREATE EXTERNAL TABLE IF NOT EXISTS taxi_db.dim_zona (
  zona_id BIGINT, distrito STRING, zona STRING, zona_servicio STRING)
STORED AS PARQUET LOCATION 's3://<BUCKET>/star/dim_zona/';

CREATE EXTERNAL TABLE IF NOT EXISTS taxi_db.dim_tiempo (
  tiempo_id BIGINT, fecha STRING, anio INT, mes INT, dia INT,
  hora INT, dia_semana INT, nombre_dia STRING, es_fin_semana BOOLEAN, franja STRING)
STORED AS PARQUET LOCATION 's3://<BUCKET>/star/dim_tiempo/';

-- =====================================================================
-- PASO 3. LAS 5 CONSULTAS ANALITICAS (ejecutar en cada configuracion)
-- Tras cada ejecucion, anota en el informe:  Data scanned  y  Run time.
-- =====================================================================

-- Q1 — Ingreso total por distrito
SELECT z.distrito, ROUND(SUM(f.total_amount), 2) AS ingreso_total, COUNT(*) AS viajes
FROM taxi_db.fct_viajes_part f
JOIN taxi_db.dim_zona z ON f.zona_pu_id = z.zona_id
GROUP BY z.distrito
ORDER BY ingreso_total DESC;

-- Q2 — Demanda por hora del dia y dia de la semana
SELECT t.nombre_dia, t.hora, COUNT(*) AS viajes
FROM taxi_db.fct_viajes_part f
JOIN taxi_db.dim_tiempo t ON f.tiempo_id = t.tiempo_id
GROUP BY t.nombre_dia, t.hora
ORDER BY viajes DESC
LIMIT 20;

-- Q3 — Tarifa media por milla por distrito (filtra distancias validas)
SELECT z.distrito,
       ROUND(AVG(f.fare_amount / NULLIF(f.trip_distance,0)), 3) AS tarifa_media_por_milla
FROM taxi_db.fct_viajes_part f
JOIN taxi_db.dim_zona z ON f.zona_pu_id = z.zona_id
WHERE f.trip_distance > 0 AND f.fare_amount > 0
GROUP BY z.distrito
ORDER BY tarifa_media_por_milla DESC;

-- Q4 — Proporcion de viajes con cargo por congestion (CBD)
SELECT ROUND(100.0 * SUM(CASE WHEN f.cbd_congestion_fee > 0 THEN 1 ELSE 0 END) / COUNT(*), 2)
       AS pct_viajes_con_cbd
FROM taxi_db.fct_viajes_part f;

-- Q5 — Top 10 zonas por propina promedio (solo pagos con tarjeta = 1)
SELECT z.zona, z.distrito, ROUND(AVG(f.tip_amount), 2) AS propina_media
FROM taxi_db.fct_viajes_part f
JOIN taxi_db.dim_zona z ON f.zona_pu_id = z.zona_id
WHERE f.pago_id = 1
GROUP BY z.zona, z.distrito
ORDER BY propina_media DESC
LIMIT 10;

-- =====================================================================
-- PASO 4. Repetir Q1 (al menos) en las 3 configuraciones:
--   - CSV                 (tabla sobre s3://<BUCKET>/csv/)
--   - Parquet sin particion (s3://<BUCKET>/star/fct_viajes_parquet/)
--   - Parquet particionado  (esta tabla)
-- y comparar el "Data scanned" de cada una.  Ese es el nucleo del analisis.
-- =====================================================================
