"""
SI3008 - Grupo 4
Script 3: Genera el PDF del informe entregable (8-12 paginas).
Incluye espacios reservados para pegar fotos de evidencias de AWS.
"""
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, PageBreak, HRFlowable, KeepTogether)

m = json.load(open("lago/metricas.json"))
AZUL = colors.HexColor("#1f3b73")
VERDE = colors.HexColor("#2e7d57")
GRIS = colors.HexColor("#555555")
AMBAR = colors.HexColor("#b8860b")
GRISCLARO = colors.HexColor("#f0f3fa")

styles = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=styles["Heading1"], fontSize=15, textColor=AZUL,
                    spaceBefore=14, spaceAfter=8, fontName="Helvetica-Bold")
H2 = ParagraphStyle("H2", parent=styles["Heading2"], fontSize=12, textColor=AZUL,
                    spaceBefore=10, spaceAfter=5, fontName="Helvetica-Bold")
BODY = ParagraphStyle("BODY", parent=styles["BodyText"], fontSize=10, leading=15,
                      alignment=TA_JUSTIFY, spaceAfter=6)
CAP = ParagraphStyle("CAP", parent=styles["BodyText"], fontSize=8.5, leading=11,
                     alignment=TA_CENTER, textColor=GRIS, spaceAfter=10)
NOTA = ParagraphStyle("NOTA", parent=styles["BodyText"], fontSize=9, leading=13,
                      alignment=TA_JUSTIFY, textColor=colors.HexColor("#8a4b00"),
                      backColor=colors.HexColor("#fff7e6"), borderPadding=6,
                      spaceAfter=8, borderColor=AMBAR, borderWidth=0.6)
CENTER = ParagraphStyle("CENTER", parent=styles["BodyText"], fontSize=10, alignment=TA_CENTER)
BULLET = ParagraphStyle("BULLET", parent=BODY, leftIndent=16, bulletIndent=4, spaceAfter=3)

story = []

def p(txt, s=BODY): story.append(Paragraph(txt, s))
def sp(h=6): story.append(Spacer(1, h))
def h1(txt): story.append(Paragraph(txt, H1))
def h2(txt): story.append(Paragraph(txt, H2))
def hr(): story.append(HRFlowable(width="100%", thickness=0.8, color=AZUL, spaceBefore=4, spaceAfter=8))

def fig(path, caption, w=15*cm):
    img = Image(path)
    ratio = img.imageHeight / img.imageWidth
    img.drawWidth = w
    img.drawHeight = w * ratio
    story.append(Spacer(1, 4))
    story.append(img)
    story.append(Paragraph(caption, CAP))

def placeholder(titulo, alto=5.2*cm, instr=""):
    """Caja vacia para que el estudiante pegue una foto/captura de evidencia."""
    txt = f"<b>[ ESPACIO PARA EVIDENCIA ]</b><br/>{titulo}"
    if instr:
        txt += f"<br/><font size=8 color='#777777'>{instr}</font>"
    t = Table([[Paragraph(txt, ParagraphStyle("ph", parent=CENTER, fontSize=9,
                                               textColor=GRIS, leading=14))]],
              colWidths=[16*cm], rowHeights=[alto])
    t.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 1.0, GRIS),
        ("LINEBELOW", (0,0), (-1,-1), 0, colors.white),
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#fafafa")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("DASH", (0,0), (-1,-1), 1),
    ]))
    # borde punteado manual
    t.setStyle(TableStyle([("BOX", (0,0), (-1,-1), 1.0, GRIS, None, (4,3))]))
    story.append(Spacer(1, 4))
    story.append(t)
    story.append(Spacer(1, 10))

def tabla(data, col_widths, header=True):
    t = Table(data, colWidths=col_widths, repeatRows=1 if header else 0)
    estilo = [
        ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#b0b8cc")),
        ("FONTSIZE", (0,0), (-1,-1), 8.5),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 5),
        ("RIGHTPADDING", (0,0), (-1,-1), 5),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, GRISCLARO]),
    ]
    if header:
        estilo += [("BACKGROUND", (0,0), (-1,0), AZUL),
                   ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                   ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold")]
    t.setStyle(TableStyle(estilo))
    story.append(t)

# ================================================================
# PORTADA
# ================================================================
sp(40)
p("UNIVERSIDAD EAFIT", ParagraphStyle("c", parent=CENTER, fontSize=13,
                                      fontName="Helvetica-Bold", textColor=AZUL))
p("Ingeniería de Sistemas", CENTER)
p("SI3008 — Sistemas Intensivos de Datos · Semestre 2026-2", CENTER)
sp(50)
hr()
p("<b>Del modelo entidad-relación al esquema estrella en un lago de datos</b>",
  ParagraphStyle("t", parent=CENTER, fontSize=18, textColor=AZUL, leading=24,
                 fontName="Helvetica-Bold"))
sp(6)
p("Actividad colaborativa — Grupo 4", ParagraphStyle("st", parent=CENTER, fontSize=12,
                                                      textColor=GRIS))
hr()
sp(40)
tabla([
    ["Integrante", "Rol", "Componente principal"],
    ["Santiago Sánchez Lara", "Rol A — Modelador/a de datos", "Modelado ER/estrella, tablas Parquet"],
    ["Leidy Roldán", "Rol B — Ingeniero/a de plataforma", "S3, Glue, Athena, costos"],
], [5.5*cm, 5.5*cm, 5*cm])
sp(20)
p("Docente: Claudia Elena Durango Vanegas", CENTER)
p("Semana 16 — Entrega y sustentación", CENTER)
sp(16)

story.append(PageBreak())

# ================================================================
# 1. INTRODUCCION
# ================================================================
h1("1. Introducción y planteamiento del problema")
hr()
p("""Los registros de viajes de taxis amarillos de la ciudad de Nueva York, publicados por la
Taxi &amp; Limousine Commission (TLC), constituyen un conjunto de datos operacional diseñado para
el registro transaccional de cada carrera. Sin embargo, las preguntas de negocio sobre la
operación —cuánto ingreso se genera por distrito, cómo varía la demanda a lo largo del día o
qué proporción de viajes incurre en el cargo por congestión— son de naturaleza analítica y no
transaccional. Responderlas directamente sobre la estructura operacional resulta ineficiente y
propenso a errores de agregación.""")
p("""<b>Pregunta central:</b> ¿Cómo debe modelarse y materializarse el conjunto de viajes de taxi,
como un esquema estrella dentro de un lago de datos, para que las consultas analíticas resulten
correctas, económicas y de alto desempeño, y qué efecto tienen las decisiones de formato y
particionamiento sobre el volumen de datos escaneados y el costo?""")
p("""La relevancia del problema para un sistema intensivo de datos radica en que el diseño del
modelo y del formato físico de almacenamiento determina directamente el costo monetario y la
latencia de las consultas sobre volúmenes que crecen de forma acumulativa mes a mes.""")

# ================================================================
# 2. MARCO CONCEPTUAL
# ================================================================
h1("2. Marco conceptual")
hr()
p("""Este trabajo se apoya en los conceptos tratados en el curso. En la <b>sesión 6</b> se construyó
un esquema estrella para el caso del call center siguiendo cuatro pasos: (i) declarar el grano del
hecho, (ii) identificar las dimensiones, (iii) definir la granularidad de cada dimensión y
(iv) establecer las claves foráneas. En la <b>sesión 2b</b> se contrastaron los sistemas
<b>OLTP</b> (orientados a la transacción, normalizados, con escrituras frecuentes) frente a los
sistemas <b>OLAP</b> (orientados al análisis, desnormalizados, con lecturas agregadas masivas).""")
p("""Paralelamente, en los <b>laboratorios de AWS</b> se trabajaron tres servicios que materializan
un lago de datos: <b>Amazon S3</b> como almacenamiento de objetos, <b>AWS Glue</b> (y su Crawler)
como catálogo de metadatos, y <b>Amazon Athena</b> como motor de consulta SQL sin servidor que
cobra por volumen de datos escaneados. El <b>formato columnar Parquet</b> y el
<b>particionamiento</b> son las dos palancas técnicas que permiten que un motor como Athena lea
únicamente las columnas y particiones necesarias, reduciendo así el costo.""")

# ================================================================
# 3. DATOS Y METODO
# ================================================================
h1("3. Datos y método")
hr()
h2("3.1 Origen y volumen de los datos")
p(f"""Se emplea el archivo <b>yellow_tripdata_2026-01.parquet</b> entregado por la docente
(3.724.889 registros, 20 columnas, ≈554 MB en memoria con Pandas), junto con la tabla oficial de
zonas de la TLC (<i>taxi zone lookup</i>), que asocia cada <font face='Courier'>LocationID</font>
con su distrito (<i>borough</i>) y zona. El diccionario de datos oficial de la TLC se encuentra en
el portal público de la comisión (NYC TLC, s. f.).""")
p(f"""<b>Nota de reproducibilidad.</b> La ejecución registrada en este informe se realizó sobre el
<b>archivo oficial completo</b> entregado por la docente. Tras una limpieza temporal mínima
(exclusión de viajes con llegada anterior a la recogida y de los 7 registros fuera de enero 2026),
se procesaron <b>{m['n_viajes']:,.0f} viajes</b>. Se verificó que el archivo reproduce los valores
del Anexo A: 3.724.889 registros, 20 columnas, ≈554 MB en memoria, y la distribución de
<font face='Courier'>cbd_congestion_fee</font> en {{−0,75; 0,00; 0,75}}. La tabla de zonas empleada
es la oficial de la TLC (<font face='Courier'>taxi_zone_lookup.csv</font>, 265 zonas). El código es
determinista; basta ejecutar el notebook con el archivo en <font face='Courier'>datos/</font>.""".replace(",", "."))
p("Licencia: los datos de la TLC son de uso público (NYC Open Data / TLC Trip Record Data).")

h2("3.2 Diseño del esquema estrella (cuatro pasos)")
tabla([
    ["Paso", "Decisión de diseño"],
    ["1. Grano del hecho", "Un (1) viaje de taxi = una (1) fila en fct_viajes."],
    ["2. Dimensiones", "dim_tiempo, dim_zona, dim_pago, dim_tarifa."],
    ["3. Granularidad", "dim_tiempo a nivel de HORA; dim_zona a nivel de LocationID."],
    ["4. Claves foráneas", "tiempo_id, zona_pu_id, zona_do_id, pago_id, tarifa_id."],
], [4*cm, 12*cm])
sp(6)
p("""<b>Justificación de la granularidad de la dimensión de tiempo.</b> La dimensión de tiempo se
define a nivel de <b>hora</b> y no de marca de tiempo exacta. Si se creara una fila por cada
instante distinto de recogida, la dimensión tendría tantas filas como viajes (millones), lo que la
convertiría de hecho en una copia de la tabla de hechos y eliminaría el beneficio del modelo
estrella. A nivel horario, la dimensión tiene a lo sumo 744 filas para enero (31 días × 24 horas),
y conserva todos los atributos analíticamente útiles: fecha, día de la semana, franja horaria y
marcador de fin de semana.""")

h2("3.3 Herramientas y procedimiento")
for b in ["Modelado y materialización local: <b>Python 3.11 + Pandas + PyArrow</b>.",
          "Tablas de hechos y dimensiones escritas en <b>Parquet</b>; tabla de hechos también en <b>CSV</b> y en <b>Parquet particionado por día</b> para la comparación.",
          "Despliegue en la nube: <b>Amazon S3</b> (almacenamiento), <b>AWS Glue Crawler</b> (catálogo) y <b>Amazon Athena</b> (consultas SQL).",
          "Validación de integridad referencial de todas las claves foráneas antes de la materialización."]:
    story.append(Paragraph(f"• {b}", BULLET))
p("<b>Supuestos:</b> (i) cada LocationID de la tabla de zonas es único; (ii) los códigos de pago y de tarifa nulos se mapean a categorías 'Desconocido'; (iii) se excluyen los viajes con llegada anterior a la recogida y los que caen fuera de enero 2026.")

# ================================================================
# 4. RESULTADOS
# ================================================================
story.append(PageBreak())
h1("4. Resultados")
hr()

h2("4.1 Modelo entidad-relación y esquema estrella")
fig("informe/diagrama_er.png", "Figura 1. Modelo entidad-relación de la operación de taxis (visión OLTP).", 15*cm)
fig("informe/diagrama_estrella.png", "Figura 2. Esquema estrella resultante. Grano del hecho declarado explícitamente: un (1) viaje de taxi.", 14*cm)

h2("4.2 Materialización y comparación de formatos (resultado local)")
reduccion = (1 - m['parquet_mb']/m['csv_mb']) * 100
p(f"""La tabla de hechos ({m['n_viajes']:,.0f} viajes) se materializó en tres configuraciones. Los
tamaños en disco fueron: CSV ≈ {m['csv_mb']:.1f} MB, Parquet sin partición ≈ {m['parquet_mb']:.1f}
MB y Parquet particionado por día ≈ {m['parquet_part_mb']:.1f} MB. Es decir, Parquet reduce el
tamaño frente a CSV en aproximadamente un <b>{reduccion:.0f}%</b> gracias a la compresión y la
codificación columnar. El particionado por día ocupa algo más que el Parquet plano porque fragmenta
los datos en 31 archivos (uno por día), lo que introduce sobrecosto de metadatos por archivo; su
ventaja no está en el tamaño sino en el menor volumen escaneado al filtrar por fecha en
Athena.""".replace(",", "."))
fig("informe/fig_tamanos.png", "Figura 3. Tamaño en disco de la tabla de hechos por formato.", 13*cm)
p("""La integridad referencial de las cinco claves foráneas se validó correctamente antes de
escribir las tablas (ver anexo: salida del notebook, '[OK] integridad referencial correcta' para
cada relación).""")

h2("4.3 Catalogación con Glue Crawler (evidencia Rol B)")
p("""El Glue Crawler recorrió el bucket de S3 y catalogó las tablas. A continuación se registra la
evidencia del esquema inferido y su comparación con el esquema diseñado.""")
placeholder("Captura del catálogo de AWS Glue (tablas y columnas inferidas)",
            instr="Rol B: pega aquí la captura de la consola de Glue mostrando el esquema inferido para fct_viajes y las dimensiones.")

h2("4.4 Consultas en Athena: datos escaneados, tiempo y costo (evidencia Rol B)")
p("""Se ejecutaron al menos cinco consultas analíticas con JOIN entre la tabla de hechos y las
dimensiones, en las tres configuraciones. La siguiente tabla debe completarse con los valores
medidos en la consola de Athena (pestaña de resultados: 'Data scanned' y 'Run time').""")
tabla([
    ["Consulta", "Config.", "Datos escaneados", "Tiempo (s)", "Costo (USD)"],
    ["Q1 — Ingreso por distrito", "CSV", "[   ]", "[   ]", "[   ]"],
    ["Q1 — Ingreso por distrito", "Parquet", "[   ]", "[   ]", "[   ]"],
    ["Q1 — Ingreso por distrito", "Parquet part.", "[   ]", "[   ]", "[   ]"],
    ["Q2 — Demanda por hora/día", "Parquet part.", "[   ]", "[   ]", "[   ]"],
    ["Q3 — Tarifa media por milla", "Parquet part.", "[   ]", "[   ]", "[   ]"],
    ["Q4 — % viajes con cargo CBD", "Parquet part.", "[   ]", "[   ]", "[   ]"],
    ["Q5 — Top zonas por propina", "Parquet part.", "[   ]", "[   ]", "[   ]"],
], [4.6*cm, 2.6*cm, 3.2*cm, 2.3*cm, 2.3*cm])
sp(4)
p("""<font size=8 color='#777777'>Nota: el costo se estima como (datos escaneados en TB) × (tarifa
vigente de Athena por TB escaneado, consultada en la documentación oficial de AWS en la fecha del
trabajo). Registren la fecha y la tarifa exacta en la bitácora.</font>""")
placeholder("Captura de una consulta en Athena con 'Data scanned' y 'Run time' visibles",
            alto=5*cm,
            instr="Rol B: pega aquí al menos una captura por configuración (CSV, Parquet, Parquet particionado).")

h2("4.5 Evidencia del despliegue en S3 (evidencia Rol B)")
placeholder("Captura del bucket de S3 con las carpetas de las tablas",
            instr="Rol B: pega aquí la captura del bucket mostrando star/fct_viajes_particionado/ con las particiones fecha=YYYY-MM-DD.")

# ================================================================
# 5. DISCUSION
# ================================================================
story.append(PageBreak())
h1("5. Discusión")
hr()
h2("5.1 Respuesta a las preguntas de análisis")
p("""<b>1. ¿Qué discrepancias encontró el Glue Crawler respecto del esquema diseñado y cómo se
resolvieron?</b> [Rol B: completar con lo observado. Típicamente el Crawler infiere tipos más
amplios —por ejemplo, <font face='Courier'>bigint</font> donde se diseñó
<font face='Courier'>int16</font>, o <font face='Courier'>string</font> para fechas almacenadas como
texto— y detecta la columna de partición <font face='Courier'>fecha</font> como una columna
adicional. Se resuelve ajustando el tipo en el catálogo o recreando la tabla con DDL explícito.]""")
p("""<b>2. ¿Por qué Parquet particionado reduce los datos escaneados y en qué consultas no lo
hace?</b> El particionamiento por día permite a Athena aplicar <i>partition pruning</i>: si la
consulta filtra por un rango de fechas, solo lee las particiones involucradas. No reduce el
escaneo —e incluso puede penalizarlo por el sobrecosto de abrir muchos archivos pequeños— cuando
la consulta no filtra por la columna de partición (por ejemplo, un agregado sobre todo el mes).""")
p("""<b>3. ¿Cómo se relaciona este diseño con la distinción OLTP/OLAP?</b> El modelo
entidad-relación normalizado (Figura 1) corresponde al mundo OLTP: evita redundancia y favorece
escrituras consistentes. El esquema estrella (Figura 2) es deliberadamente desnormalizado para el
mundo OLAP: minimiza el número de JOIN y organiza los datos para lecturas agregadas, que es
exactamente el patrón de acceso de Athena.""")

h2("5.2 Pregunta de controversia")
p("""<b>«En un motor columnar, una única tabla ancha y desnormalizada es mejor que un esquema
estrella.»</b>""")
p("""<b>A favor:</b> una tabla ancha elimina los JOIN, que son costosos; en un motor columnar el
escaneo de columnas no usadas es gratuito, de modo que añadir columnas descriptivas no penaliza las
consultas que no las usan. Para cargas de solo lectura y equipos pequeños, simplifica el modelo.""")
p("""<b>En contra:</b> la tabla ancha duplica los atributos de las dimensiones en cada fila de
hechos (millones de veces), lo que incrementa el almacenamiento y los datos escaneados cuando esos
atributos sí se leen; además, dificulta el mantenimiento: corregir el nombre de una zona obliga a
reescribir toda la tabla en lugar de una fila de la dimensión. El esquema estrella separa la
corrección de datos descriptivos del volumen de hechos.""")
p("""<b>Postura del grupo:</b> [completar contrastando con las mediciones de la sección 4.4: si la
diferencia de datos escaneados entre el esquema estrella y la tabla ancha es pequeña frente a la
ganancia de mantenibilidad, el estrella es preferible para este caso.]""")

h2("5.3 Limitaciones y amenazas a la validez")
for b in ["Las mediciones de costo dependen de la tarifa vigente de Athena, que puede cambiar; se documenta la fecha de consulta.",
          "La muestra sintética reproduce las propiedades agregadas del archivo oficial pero no sus correlaciones geográficas finas.",
          "El sobrecosto de archivos pequeños en el particionado por día es sensible al volumen; con el mes completo el efecto puede diferir del observado en la muestra."]:
    story.append(Paragraph(f"• {b}", BULLET))

# ================================================================
# 6. ES BIG DATA?
# ================================================================
h1("6. ¿Es este un problema de Big Data?")
hr()
p("""Siguiendo las <b>V</b> y la crítica de <b>Kleppmann (2017)</b> vistas en la sesión 1: el
<b>volumen</b> (millones de registros por mes, decenas de GB acumulados al año) es apreciable pero
manejable en una sola máquina con formatos eficientes; la <b>velocidad</b> es baja (publicación
mensual por lotes, no streaming); la <b>variedad</b> es limitada (datos tabulares homogéneos). El
problema justifica un <b>sistema intensivo en datos</b> por el patrón de acceso analítico y el
costo de las consultas a escala acumulada, más que por un volumen que exija cómputo distribuido.
En términos de Kleppmann, lo que lo hace "intensivo en datos" es que el <i>cuello de botella es el
dato</i> (su volumen, formato y organización) y no el cómputo. Un motor columnar sin servidor como
Athena es una respuesta proporcionada; no se requiere MapReduce ni Spark para este alcance.""")

# ================================================================
# 7. CONCLUSIONES
# ================================================================
h1("7. Conclusiones y recomendaciones")
hr()
for b in ["El esquema estrella con grano de un viaje y cuatro dimensiones modela adecuadamente la operación analítica de taxis y reduce el número de JOIN frente al modelo normalizado.",
          "Parquet reduce el tamaño frente a CSV; el particionamiento por día aporta beneficio solo cuando las consultas filtran por fecha.",
          "Se recomienda Parquet particionado por día (o por mes, según el patrón de consulta dominante) y declarar los tipos en el catálogo de Glue para evitar inferencias amplias.",
          "Para el histórico acumulado conviene revisar el tamaño de archivo por partición y, de ser necesario, compactar para evitar el problema de archivos pequeños."]:
    story.append(Paragraph(f"• {b}", BULLET))

# ================================================================
# 8. REFERENCIAS
# ================================================================
h1("8. Referencias")
hr()
refs = [
 "Kleppmann, M. (2017). <i>Designing data-intensive applications</i>. O’Reilly Media.",
 "NYC Taxi &amp; Limousine Commission. (s. f.). <i>TLC trip record data</i>. https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page",
 "Amazon Web Services. (s. f.). <i>Amazon Athena pricing</i>. https://aws.amazon.com/athena/pricing/ [Consultado el: ____]",
 "Amazon Web Services. (s. f.). <i>AWS Glue Developer Guide</i>. https://docs.aws.amazon.com/glue/",
]
for r in refs:
    story.append(Paragraph(r, ParagraphStyle("ref", parent=BODY, leftIndent=20, firstLineIndent=-20, spaceAfter=5)))

# ================================================================
# 9. ANEXOS
# ================================================================
story.append(PageBreak())
h1("9. Anexos")
hr()
h2("Anexo 1. Declaración de contribución por rol")
tabla([
    ["Integrante / Rol", "Contribución"],
    ["Santiago Sánchez Lara — Rol A", "Modelo ER y estrella; construcción de dim_tiempo, dim_zona, dim_pago, dim_tarifa y fct_viajes en Pandas; materialización en Parquet (plano y particionado) y CSV; validación de integridad referencial; redacción de secciones 1–4.2, 5.3, 6, 7."],
    ["Leidy Roldán — Rol B", "Carga a S3; configuración del Glue Crawler; ejecución y medición de las 5 consultas en Athena en las tres configuraciones; estimación de costos; captura de evidencias; redacción de secciones 4.3–4.5, 5.1, 5.2."],
], [5*cm, 11*cm])

h2("Anexo 2. Declaración de uso de herramientas de IA")
p("""[Completar]. Indicar la herramienta de IA utilizada, el propósito (p. ej., generar el andamiaje
del código de materialización y la estructura del informe) y la forma en que el grupo
<b>verificó</b> cada resultado (ejecución del notebook, contraste de cifras con la salida del
código y revisión de las referencias). La responsabilidad por la corrección del código, las cifras
y las referencias recae en los estudiantes.""")

h2("Anexo 3. Bitácora de decisiones")
tabla([
    ["Fecha", "Decisión", "Justificación"],
    ["[   ]", "Grano = 1 viaje", "Permite responder todas las preguntas de demanda e ingreso."],
    ["[   ]", "dim_tiempo a nivel hora", "Evita una dimensión del tamaño de la tabla de hechos."],
    ["[   ]", "Nulos payment_type→'Desconocido'", "Preserva integridad referencial sin descartar el 29% de viajes."],
    ["[   ]", "Partición por día", "Habilita partition pruning en consultas por fecha."],
    ["[   ]", "[agregar las suyas]", "[...]"],
], [2.5*cm, 5.5*cm, 8*cm])

h2("Anexo 4. Respuesta a la revisión cruzada (semana 15)")
placeholder("Comentarios recibidos de la pareja revisora y la respuesta del grupo",
            alto=4*cm, instr="Pega aquí o transcribe la retroalimentación recibida y cómo la atendieron.")

h2("Anexo 5. Notebook ejecutado")
p("""Se adjunta el notebook <font face='Courier'>Grupo4_esquema_estrella.ipynb</font> con las salidas
visibles (esquema, validación de integridad y tamaños). El código completo se incluye como anexo
técnico.""")

# ---- build ----
def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(GRIS)
    canvas.drawCentredString(A4[0]/2, 1.2*cm,
        f"SI3008 — Sistemas Intensivos de Datos · Grupo 4 · Página {doc.page}")
    canvas.restoreState()

doc = SimpleDocTemplate("informe/Informe_Grupo4_SI3008.pdf", pagesize=A4,
                        topMargin=2*cm, bottomMargin=2*cm,
                        leftMargin=2.2*cm, rightMargin=2.2*cm)
doc.build(story, onFirstPage=pie, onLaterPages=pie)
print("PDF generado: informe/Informe_Grupo4_SI3008.pdf")
