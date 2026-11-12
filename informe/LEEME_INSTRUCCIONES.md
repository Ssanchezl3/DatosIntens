# 📋 Guía del entregable — Grupo 4 (SI3008)

## ✅ Lo que YA está hecho (automático)

- **Informe en PDF**: `Informe_Grupo4_SI3008.pdf` (9 páginas, estructura completa exigida).
- **Notebook ejecutable**: `Grupo4_esquema_estrella.ipynb` (tu parte, Rol A).
- **Diagramas**: ER (Figura 1), esquema estrella (Figura 2), gráfico de tamaños (Figura 3).
- **Tablas del esquema estrella** materializadas en Parquet y CSV (carpeta `lago/`).
- **Consultas SQL de Athena** listas para tu amiga: `consultas_athena_ROL_B.sql`.

---

## 👤 LO QUE TIENES QUE HACER TÚ (Rol A) — poco

1. **Reemplazar tus nombres** en el PDF donde dice `[ TU NOMBRE ]` y `[ NOMBRE AMIGA ]`
   (portada, Anexo 1 y Anexo 3). → Me puedes pedir que lo haga yo si me das los nombres.
2. **Conseguir el archivo oficial** `yellow_tripdata_2026-01.parquet` de la docente y ponerlo
   en `datos/`. Luego re-ejecutar el notebook para que las cifras sean las reales (3.72M viajes).
   Si no lo tienes aún, el notebook ya corre con datos sintéticos (semilla 2026).
3. **Entregarle a tu amiga** las tablas de la carpeta `lago/star/` (son los archivos que ella sube a S3).

## 👥 LO QUE HACEN LAS DOS

- Rellenar la **bitácora** (Anexo 3) con fechas reales.
- Llenar la **declaración de uso de IA** (Anexo 2).
- El **resumen de 1 página** (máx. 300 palabras) — pídemelo y te lo genero.

## 👤 LO QUE HACE TU AMIGA (Rol B) — necesita AWS

1. Subir las tablas de `lago/star/` a un bucket de **Amazon S3**.
2. Correr un **Glue Crawler** para catalogarlas.
3. Ejecutar las 5 consultas de `consultas_athena_ROL_B.sql` en **Athena**, en 3 formatos
   (CSV, Parquet, Parquet particionado) y anotar *Data scanned* + *Run time*.
4. **Pegar las fotos/capturas** en los espacios marcados `[ESPACIO PARA EVIDENCIA]` del PDF
   (secciones 4.3, 4.4 y 4.5).
5. Llenar la tabla de costos de la sección 4.4.

---

## 📸 Sobre los espacios para fotos

El PDF tiene **cajas punteadas** que dicen `[ESPACIO PARA EVIDENCIA]` con instrucciones adentro.
Esas fotos son de AWS y **solo las puede tomar quien tenga la consola abierta** (Rol B).
Si al final NO usan AWS (alternativa local que menciona el enunciado), esas cajas se pueden quitar
—avísame y te genero una versión sin ellas.
