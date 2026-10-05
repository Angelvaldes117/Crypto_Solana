import pandas as pd
import matplotlib.pyplot as plt
import os

# Leer los datos obtenidos en la Actividad 4
df = pd.read_csv("datos_solana_7_dias.csv")

# Convertir fechas a UTC
df["time"] = pd.to_datetime(df["time"], utc=True)

# Buscar máximo y mínimo utilizando el precio de cierre
indice_max = df["close"].idxmax()
indice_min = df["close"].idxmin()

precio_max = df.loc[indice_max, "close"]
fecha_max = df.loc[indice_max, "time"]

precio_min = df.loc[indice_min, "close"]
fecha_min = df.loc[indice_min, "time"]

# Período analizado
inicio = df["time"].min()
fin = df["time"].max()

print("ACTIVIDAD 6 - EVOLUCIÓN DEL PRECIO")
print("----------------------------------")

print("Símbolo: SOLUSD")
print("Temporalidad: H1")
print("Registros analizados:", len(df))

print("\nPeríodo analizado:")
print("Desde:", inicio)
print("Hasta:", fin)

print("\nPrecio de cierre máximo:")
print("Precio:", precio_max, "USD")
print("Fecha:", fecha_max)

print("\nPrecio de cierre mínimo:")
print("Precio:", precio_min, "USD")
print("Fecha:", fecha_min)

# Crear carpeta para las gráficas
os.makedirs("graficas", exist_ok=True)

# Crear gráfica
plt.figure(figsize=(14, 7))

plt.plot(
    df["time"],
    df["close"],
    label="Precio de cierre"
)

# Punto máximo
plt.scatter(
    fecha_max,
    precio_max,
    s=100,
    label=f"Máximo: {precio_max:.2f} USD"
)

# Punto mínimo
plt.scatter(
    fecha_min,
    precio_min,
    s=100,
    label=f"Mínimo: {precio_min:.2f} USD"
)

# Etiquetas de máximo y mínimo
plt.annotate(
    f"Máximo\n{precio_max:.2f} USD",
    xy=(fecha_max, precio_max),
    xytext=(15, 15),
    textcoords="offset points",
    arrowprops=dict(arrowstyle="->")
)

plt.annotate(
    f"Mínimo\n{precio_min:.2f} USD",
    xy=(fecha_min, precio_min),
    xytext=(15, -35),
    textcoords="offset points",
    arrowprops=dict(arrowstyle="->")
)

plt.title(
    "Evolución del precio de cierre de SOLUSD\n"
    f"{inicio.strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{fin.strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel("Fecha y hora (UTC)")
plt.ylabel("Precio de cierre (USD)")

plt.legend()
plt.grid(True, alpha=0.3)

plt.xticks(rotation=45)

plt.tight_layout()

# Guardar gráfica
ruta = "graficas/actividad_06_evolucion_precio.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nGráfica guardada en:")
print(ruta)

plt.show()