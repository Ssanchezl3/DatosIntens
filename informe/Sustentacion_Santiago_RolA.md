# 🎤 Sustentación individual — Santiago Sánchez Lara (Rol A)
### Grupo 4 · Del modelo ER al esquema estrella en un lago de datos · 3–5 min

> **Recuerda:** la sustentación es individual y te pueden preguntar de CUALQUIER parte,
> también de lo de Leidy. Por eso el guion cubre el trabajo completo, pero resaltando lo tuyo.

---

## ⏱️ Guion hablado (≈4 minutos)

### 1. Apertura — el problema (30 s)
"Los datos de taxis de Nueva York son **transaccionales**: una fila por viaje, pensada para
*registrar*, no para *analizar*. Nuestra pregunta fue: **¿cómo modelar y guardar esos viajes para
que las consultas analíticas sean correctas, rápidas y baratas?** La respuesta fue un **esquema
estrella** dentro de un **lago de datos**."

### 2. Lo que hice yo — Rol A: modelado (90 s)
"Yo fui el **modelador de datos**. Partí del modelo entidad-relación de la operación (Figura 1) y lo
transformé en un esquema estrella siguiendo los **cuatro pasos** vistos en clase:
1. **Grano del hecho:** un viaje = una fila en `fct_viajes`.
2. **Dimensiones:** tiempo, zona, pago y tarifa.
3. **Granularidad:** la dimensión de tiempo la hice a nivel de **hora**, no de timestamp exacto —
   si no, tendría millones de filas y dejaría de ser una dimensión.
4. **Claves foráneas:** cinco FKs que conectan los hechos con las dimensiones.

Lo implementé en **Python con Pandas**, materialicé todo en **Parquet** y generé una versión
**particionada por día**. Antes de escribir, **validé la integridad referencial**: las 5 claves
foráneas apuntan correctamente a sus dimensiones."

### 3. El resultado clave (45 s)
"Procesamos los **3,72 millones de viajes reales** de enero. El hallazgo más fuerte:
la misma tabla ocupa **204 MB en CSV pero solo 33 MB en Parquet** — una reducción de ~84% —
gracias a la compresión y al almacenamiento por columnas."

### 4. Lo que hizo Leidy — Rol B: la nube (45 s)
"Leidy tomó mis tablas y las llevó a **AWS**: las subió a **S3**, las catalogó con un **Glue
Crawler** y las consultó con **Athena**. Midió, para 5 consultas, cuántos datos escanea cada
formato y cuánto cuesta. La conclusión: el **Parquet particionado** reduce el escaneo —y por tanto
el costo— cuando la consulta **filtra por fecha**."

### 5. Cierre — ¿es Big Data? (30 s)
"¿Es esto Big Data? El **volumen** es grande pero manejable en una máquina; no hay streaming ni
necesidad de Spark. Lo que lo hace un sistema **intensivo en datos** no es el cómputo, sino que el
**cuello de botella es el dato**: su volumen, su formato y su organización. Por eso Athena —un motor
columnar sin servidor— es la respuesta proporcionada. Gracias."

---

## 🗂️ Versión diapositivas (5 slides)

**Slide 1 — Portada**
- Grupo 4: Del modelo ER al esquema estrella
- Santiago Sánchez Lara (Rol A) · Leidy Roldán (Rol B)

**Slide 2 — El problema**
- Datos de taxis = transaccionales (OLTP)
- Preguntas de negocio = analíticas (OLAP)
- Objetivo: consultas correctas, rápidas y baratas

**Slide 3 — Mi parte (Rol A): el modelo** [Figura 2, esquema estrella]
- Grano: 1 viaje · Dimensiones: tiempo, zona, pago, tarifa
- dim_tiempo a nivel HORA (no timestamp)
- Parquet + partición por día · integridad referencial OK

**Slide 4 — Resultado + parte de Leidy (Rol B)** [Figura 3, tamaños]
- 3,72 M viajes · CSV 204 MB → Parquet 33 MB (−84%)
- Leidy: S3 + Glue + Athena → costo por formato
- Partición ayuda solo si se filtra por fecha

**Slide 5 — ¿Es Big Data? + cierre**
- Volumen alto pero manejable; sin Spark/streaming
- Intensivo en datos = el dato es el cuello de botella

---

## 🎯 Preguntas probables (prepáralas)

| Pregunta | Respuesta corta |
|---|---|
| ¿Por qué estrella y no el modelo normalizado? | Menos JOINs, lecturas agregadas rápidas (OLAP). |
| ¿Por qué dim_tiempo por hora? | Evita una dimensión del tamaño de la tabla de hechos. |
| ¿Por qué Parquet pesa menos? | Columnar + compresión; lee solo las columnas usadas. |
| ¿Cuándo NO ayuda el particionado? | Cuando la consulta no filtra por la columna de partición (fecha). |
| ¿Qué validaste? | Integridad referencial: las 5 FKs apuntan a dimensiones existentes. |
| ¿Es Big Data? | Es intensivo en datos (el dato es el cuello de botella), no exige Spark. |
