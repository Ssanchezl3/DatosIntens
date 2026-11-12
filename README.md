# SI3008 — Grupo 4: Del modelo entidad-relación al esquema estrella en un lago de datos

**Universidad EAFIT — Ingeniería de Sistemas — Sistemas Intensivos de Datos (2026-2)**

| Integrante | Rol | Componente |
|------------|-----|-----------|
| Santiago Sánchez Lara | Rol A — Modelador/a de datos | Modelado ER/estrella, tablas Parquet |
| Leidy Roldán | Rol B — Ingeniero/a de plataforma | S3, Glue, Athena, costos |

## Contenido del repositorio

```
├── informe/
│   ├── Informe_Grupo4_SI3008.pdf        <- Informe entregable (PDF)
│   ├── Grupo4_esquema_estrella.ipynb    <- Notebook ejecutable (Rol A)
│   ├── consultas_athena_ROL_B.sql       <- Consultas de Athena (Rol B)
│   ├── LEEME_INSTRUCCIONES.md           <- Quién hace qué
│   ├── diagrama_er.png
│   ├── diagrama_estrella.png
│   └── fig_tamanos.png
├── 01_generar_datos.py                  <- Dataset sintético (semilla 2026)
├── 02_esquema_estrella.py               <- Construye el esquema estrella
├── 03_diagramas.py                      <- Diagramas y gráficos
├── 04_generar_pdf.py                    <- Genera el PDF
├── 05_crear_notebook.py                 <- Genera el notebook
├── datos/taxi_zone_lookup.csv
└── requirements.txt
```

## Cómo ejecutar (Rol A)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python 01_generar_datos.py       # o coloca el archivo oficial en datos/
python 02_esquema_estrella.py
python 03_diagramas.py
```

> **Archivo oficial:** coloca `yellow_tripdata_2026-01.parquet` en `datos/` para usar los datos reales.
> Está excluido del repo por su tamaño (ver `.gitignore`).

## Flujo de trabajo

1. **Rol A** construye las tablas del esquema estrella (`lago/star/`).
2. **Rol B** las sube a **Amazon S3**, cataloga con **Glue Crawler** y consulta con **Athena**.
3. Ambos completan el informe y pegan las evidencias de AWS en los espacios marcados del PDF.
