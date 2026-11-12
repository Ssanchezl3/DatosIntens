"""
SI3008 - Grupo 4 - ROL A
Script 2: Genera los diagramas y graficos para el informe:
  - diagrama_er.png        (modelo entidad-relacion)
  - diagrama_estrella.png  (esquema estrella)
  - fig_tamanos.png        (comparacion de tamanos CSV/Parquet/particionado)
"""
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import pandas as pd

AZUL = "#1f3b73"
AZULC = "#d6e0f5"
VERDE = "#2e7d57"
VERDEC = "#d6efe2"
GRIS = "#555555"

def caja(ax, x, y, w, h, titulo, lineas, fc, ec):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fc, ec=ec, lw=1.8, zorder=2))
    ax.text(x + w/2, y + h - 0.26, titulo, ha="center", va="top",
            fontsize=10.5, fontweight="bold", color=ec, zorder=3)
    n = len(lineas)
    # espaciado adaptativo para que las lineas nunca se salgan de la caja
    espacio = min(0.30, (h - 0.55) / max(n, 1))
    for i, ln in enumerate(lineas):
        ax.text(x + 0.12, y + h - 0.58 - i*espacio, ln, ha="left", va="top",
                fontsize=7.8, color="#222", zorder=3)

# ============================================================
# 1. DIAGRAMA ENTIDAD-RELACION (modelo operacional / OLTP)
# ============================================================
fig, ax = plt.subplots(figsize=(9.5, 6))
ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis("off")
ax.set_title("Figura 1. Modelo entidad-relación de la operación de taxis (OLTP)",
             fontsize=11, fontweight="bold", color=AZUL, pad=10)

caja(ax, 4.4, 5.3, 3.2, 2.5, "VIAJE",
     ["PK id_viaje", "pickup_datetime", "dropoff_datetime", "trip_distance",
      "fare_amount, tip, total", "FK id_vendor", "FK PULocationID / DOLocationID",
      "FK payment_type / RatecodeID"], "#fff4d6", "#b8860b")
caja(ax, 0.3, 1.9, 2.7, 1.9, "ZONA", ["PK LocationID", "Borough", "Zone", "service_zone"], AZULC, AZUL)
caja(ax, 3.4, 1.9, 2.4, 1.9, "VENDOR", ["PK VendorID", "nombre"], AZULC, AZUL)
caja(ax, 6.2, 1.9, 2.4, 1.9, "PAGO", ["PK payment_type", "metodo"], AZULC, AZUL)
caja(ax, 9.0, 1.9, 2.6, 1.9, "TARIFA", ["PK RatecodeID", "tipo_tarifa"], AZULC, AZUL)

for (x, y) in [(1.7, 3.8), (4.6, 3.8), (7.4, 3.8), (10.3, 3.8)]:
    ax.add_patch(FancyArrowPatch((6.0, 5.3), (x, y), arrowstyle="-|>",
                                 mutation_scale=14, color=GRIS, lw=1.3,
                                 connectionstyle="arc3,rad=0.0", zorder=1))
ax.text(6.3, 4.55, "N : 1", fontsize=8, color=GRIS, ha="center", style="italic")
plt.tight_layout()
plt.savefig("informe/diagrama_er.png", dpi=150, bbox_inches="tight")
plt.close()

# ============================================================
# 2. DIAGRAMA ESQUEMA ESTRELLA
# ============================================================
fig, ax = plt.subplots(figsize=(9.5, 7))
ax.set_xlim(0, 12); ax.set_ylim(0, 9); ax.axis("off")
ax.set_title("Figura 2. Esquema estrella — grano del hecho: un (1) viaje de taxi",
             fontsize=11, fontweight="bold", color=VERDE, pad=10)

caja(ax, 3.9, 2.95, 4.2, 3.2, "FCT_VIAJES (hechos)",
     ["grano: 1 viaje", "FK tiempo_id", "FK zona_pu_id / zona_do_id",
      "FK pago_id / tarifa_id", "· trip_distance", "· fare / tip / total",
      "· cbd_congestion_fee"], VERDEC, VERDE)

caja(ax, 4.4, 6.6, 3.2, 1.8, "DIM_TIEMPO",
     ["PK tiempo_id (hora)", "fecha, anio, mes, dia", "hora, dia_semana", "franja, fin_semana"], AZULC, AZUL)
caja(ax, 0.3, 4.0, 3.0, 1.7, "DIM_ZONA",
     ["PK zona_id", "distrito (borough)", "zona", "zona_servicio"], AZULC, AZUL)
caja(ax, 8.7, 4.0, 3.0, 1.7, "DIM_PAGO",
     ["PK pago_id", "metodo_pago"], AZULC, AZUL)
caja(ax, 4.4, 0.6, 3.2, 1.7, "DIM_TARIFA",
     ["PK tarifa_id", "tipo_tarifa"], AZULC, AZUL)

cx, cy = 6.0, 4.55
for (x, y) in [(6.0, 6.6), (3.9, 4.85), (8.1, 4.85), (6.0, 2.3)]:
    ax.add_patch(FancyArrowPatch((cx, cy), (x, y), arrowstyle="-|>",
                                 mutation_scale=13, color=GRIS, lw=1.3, zorder=1))
plt.tight_layout()
plt.savefig("informe/diagrama_estrella.png", dpi=150, bbox_inches="tight")
plt.close()

# ============================================================
# 3. GRAFICO DE TAMANOS (CSV vs Parquet vs particionado)
# ============================================================
m = json.load(open("lago/metricas.json"))
fig, ax = plt.subplots(figsize=(7.5, 4.2))
etiquetas = ["CSV", "Parquet\n(sin partición)", "Parquet\n(particionado)"]
valores = [m["csv_mb"], m["parquet_mb"], m["parquet_part_mb"]]
colores = ["#c0504d", VERDE, AZUL]
barras = ax.bar(etiquetas, valores, color=colores, width=0.55)
ax.set_ylabel("Tamaño en disco (MB)")
ax.set_title("Figura 3. Tamaño de la tabla de hechos por formato de almacenamiento",
             fontsize=10.5, fontweight="bold", color=AZUL)
for b, v in zip(barras, valores):
    ax.text(b.get_x() + b.get_width()/2, v + max(valores)*0.02,
            f"{v:.1f} MB", ha="center", fontsize=9, fontweight="bold")
ax.spines[["top", "right"]].set_visible(False)
plt.tight_layout()
plt.savefig("informe/fig_tamanos.png", dpi=150, bbox_inches="tight")
plt.close()

print("Diagramas y graficos generados en informe/")
