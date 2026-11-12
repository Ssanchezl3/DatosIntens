# 🟢 Guía Rol B — Leidy Roldán (Ingeniera de plataforma en la nube)

Esta guía tiene **todo lo que necesitas** para tu parte: subir las tablas a S3,
catalogarlas con Glue, consultarlas con Athena y medir costos.

---

## 📦 1. Qué hay en esta carpeta (`tablas_para_S3/`)

| Archivo | Qué es |
|---|---|
| `dimensiones/dim_tiempo.parquet` | Dimensión de tiempo (744 filas) |
| `dimensiones/dim_zona.parquet` | Dimensión de zona (265 zonas TLC) |
| `dimensiones/dim_pago.parquet` | Dimensión de método de pago |
| `dimensiones/dim_tarifa.parquet` | Dimensión de tipo de tarifa |
| `fct_viajes_muestra/…parquet` | **Muestra** de la tabla de hechos (100.000 viajes, 1,2 MB) |

> ⚠️ **Importante sobre la tabla de hechos:** aquí está solo una **muestra** de 100k viajes
> (la completa son 3,72 M y pesa demasiado para GitHub). Sirve para que montes y pruebes
> TODO el flujo en AWS. Para los números finales del informe, genera la tabla completa así:
>
> ```bash
> # Santiago (Rol A) ya tiene esto; corre el notebook con el .parquet oficial en datos/
> python 02_esquema_estrella.py
> # Esto crea lago/star/fct_viajes_parquet/ y lago/star/fct_viajes_particionado/
> ```
> Y sube esas carpetas completas a S3 (son las mismas rutas que abajo).

---

## ☁️ 2. Subir a Amazon S3

1. Entra a **AWS Academy Learner Lab** → inicia el lab → abre la **consola de AWS**.
2. Ve a **S3** → **Create bucket**. Nombre único, p. ej. `grupo4-taxi-si3008-<tusiniciales>`.
3. Dentro del bucket, crea esta estructura de carpetas y sube los archivos:

```
s3://TU-BUCKET/
├── star/
│   ├── dim_tiempo/        <- sube dim_tiempo.parquet
│   ├── dim_zona/          <- sube dim_zona.parquet
│   ├── dim_pago/          <- sube dim_pago.parquet
│   ├── dim_tarifa/        <- sube dim_tarifa.parquet
│   ├── fct_viajes_parquet/        <- sube la tabla de hechos en Parquet
│   └── fct_viajes_particionado/   <- sube las carpetas fecha=2026-01-01/ ... (particionado)
└── csv/
    └── fct_viajes.csv     <- versión CSV (para comparar escaneo)
```

> 💡 Cada tabla va en **su propia carpeta** (Glue cataloga por carpeta, no por archivo).

📸 **EVIDENCIA 1:** toma captura del bucket con las carpetas → va en la **sección 4.5** del informe.

---

## 🔎 3. Catalogar con AWS Glue Crawler

1. Ve a **AWS Glue** → **Crawlers** → **Create crawler**.
2. Data source: **S3**, apunta a `s3://TU-BUCKET/star/`.
3. IAM role: usa el rol del Learner Lab (p. ej. `LabRole`).
4. Database de destino: crea una nueva, p. ej. `taxi_db`.
5. Ejecuta el crawler. Al terminar, verás las tablas catalogadas con su esquema inferido.

📸 **EVIDENCIA 2:** captura del catálogo de Glue con las tablas y columnas → **sección 4.3**.

✍️ **Para el informe (sección 5.1, pregunta 1):** compara el esquema que **infirió** el Crawler
con el que **diseñó** Santiago. Anota diferencias típicas: tipos más amplios (`bigint` vs `int16`),
`string` para fechas, y la columna de partición `fecha` detectada aparte.

---

## 📊 4. Consultar con Amazon Athena

1. Ve a **Athena** → selecciona la base `taxi_db`.
2. Configura el **query result location** (una carpeta en S3, p. ej. `s3://TU-BUCKET/athena-results/`).
3. Abre el archivo **`informe/consultas_athena_ROL_B.sql`** (está en el repo) y ejecuta las 5 consultas.
4. **Repite al menos la Q1 en las 3 configuraciones**: CSV, Parquet sin partición y Parquet particionado.
5. Tras cada ejecución, Athena muestra abajo **"Data scanned"** y **"Run time"**. Anótalos.

📸 **EVIDENCIA 3:** captura de una consulta con "Data scanned" y "Run time" visibles → **sección 4.4**.

---

## 💰 5. Estimar el costo

- Fórmula: **Costo = (Data scanned en TB) × (tarifa de Athena por TB)**.
- Consulta la **tarifa vigente** en https://aws.amazon.com/athena/pricing/ (anota la fecha).
- Llena la **tabla de la sección 4.4** del informe con: datos escaneados, tiempo y costo por configuración.

✍️ **Para la sección 5.1, pregunta 2:** el Parquet particionado reduce el escaneo **solo si la
consulta filtra por fecha** (partition pruning). Si consultas todo el mes, no ayuda.

---

## ✅ 6. Checklist de tu entrega

- [ ] Bucket S3 con las tablas (EVIDENCIA 1)
- [ ] Glue Crawler ejecutado y comparación de esquemas (EVIDENCIA 2)
- [ ] 5 consultas en Athena + Q1 en 3 formatos (EVIDENCIA 3)
- [ ] Tabla de costos (sección 4.4) completa
- [ ] Redactar secciones 4.3, 4.4, 4.5, 5.1 y 5.2 del informe
- [ ] Pegar las 3 evidencias en los espacios `[ESPACIO PARA EVIDENCIA]` del PDF

> Si el Learner Lab NO está disponible, avísenle a la docente en la semana 15 (el enunciado
> permite una alternativa local que conserve la comparación entre formatos).
