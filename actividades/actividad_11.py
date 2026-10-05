import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar datos
df = pd.read_csv("datos_solana_7_dias.csv")

# Convertir fecha a UTC
df["time"] = pd.to_datetime(df["time"], utc=True)

# Ordenar cronológicamente
df = df.sort_values("time").copy()

inicio = df["time"].min()
fin = df["time"].max()

# Crear columna con la fecha UTC
df["fecha"] = df["time"].dt.date

# Crear resumen diario OHLC
resumen_diario = df.groupby("fecha").agg(
    apertura=("open", "first"),
    maximo=("high", "max"),
    minimo=("low", "min"),
    cierre=("close", "last"),
    cantidad_velas=("time", "count")
).reset_index()

# Cambio porcentual dentro de cada día:
# desde la apertura de la primera vela hasta el cierre de la última
resumen_diario["cambio_pct"] = (
    (resumen_diario["cierre"] - resumen_diario["apertura"])
    / resumen_diario["apertura"]
) * 100

print("ACTIVIDAD 11 - RESUMEN DIARIO")
print("-----------------------------")
print("Símbolo: SOLUSD")
print("Temporalidad original: H1")
print("Registros analizados:", len(df))

print("\nPeríodo analizado:")
print("Desde:", inicio)
print("Hasta:", fin)

print("\nRESUMEN DIARIO:")

print(
    resumen_diario[
        [
            "fecha",
            "apertura",
            "maximo",
            "minimo",
            "cierre",
            "cambio_pct",
            "cantidad_velas"
        ]
    ].to_string(index=False)
)

# Guardar resumen para actividades posteriores
resumen_diario.to_csv(
    "resumen_diario_solana.csv",
    index=False
)

# Crear carpeta
os.makedirs("graficas", exist_ok=True)

# Preparar fechas para la gráfica
resumen_diario["fecha"] = pd.to_datetime(
    resumen_diario["fecha"]
)

# Crear gráfica
plt.figure(figsize=(12, 7))

plt.plot(
    resumen_diario["fecha"],
    resumen_diario["cierre"],
    marker="o",
    linewidth=2,
    label="Cierre diario"
)

# Mostrar precio encima de cada punto
for fecha, cierre in zip(
    resumen_diario["fecha"],
    resumen_diario["cierre"]
):
    plt.annotate(
        f"{cierre:.2f}",
        (fecha, cierre),
        textcoords="offset points",
        xytext=(0, 8),
        ha="center"
    )

plt.title(
    "Evolución del cierre diario de SOLUSD\n"
    f"{inicio.strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{fin.strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel("Fecha (UTC)")
plt.ylabel("Precio de cierre diario (USD)")

plt.grid(True, alpha=0.3)
plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()

ruta = "graficas/actividad_11_cierre_diario.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nResumen guardado en:")
print("resumen_diario_solana.csv")

print("\nGráfica guardada en:")
print(ruta)

plt.show()