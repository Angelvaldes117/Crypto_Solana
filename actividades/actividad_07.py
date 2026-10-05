import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar los datos de los siete días
df = pd.read_csv("datos_solana_7_dias.csv")

# Convertir fecha a UTC
df["time"] = pd.to_datetime(df["time"], utc=True)

# Calcular el rango de cada vela
df["rango_usd"] = df["high"] - df["low"]

# Seleccionar las 10 velas con mayor rango
top_10 = (
    df.nlargest(10, "rango_usd")
    .sort_values("rango_usd", ascending=False)
    .copy()
)

# Etiqueta para la gráfica
top_10["fecha_etiqueta"] = top_10["time"].dt.strftime(
    "%m-%d %H:%M"
)

inicio = df["time"].min()
fin = df["time"].max()

print("ACTIVIDAD 7 - MAYOR MOVIMIENTO DENTRO DE UNA VELA")
print("-------------------------------------------------")
print("Símbolo: SOLUSD")
print("Temporalidad: H1")
print("Registros analizados:", len(df))

print("\nPeríodo analizado:")
print("Desde:", inicio)
print("Hasta:", fin)

print("\n10 VELAS CON MAYOR RANGO HIGH - LOW:")

print(
    top_10[
        ["time", "high", "low", "rango_usd"]
    ].to_string(index=False)
)

# Mostrar la vela con mayor movimiento
mayor = top_10.iloc[0]

print("\nMAYOR MOVIMIENTO:")
print("Fecha:", mayor["time"])
print(f"Máximo: {mayor['high']:.2f} USD")
print(f"Mínimo: {mayor['low']:.2f} USD")
print(f"Rango: {mayor['rango_usd']:.2f} USD")

# Crear carpeta si no existe
os.makedirs("graficas", exist_ok=True)

# Gráfica
plt.figure(figsize=(13, 7))

plt.bar(
    top_10["fecha_etiqueta"],
    top_10["rango_usd"]
)

plt.title(
    "10 velas horarias de SOLUSD con mayor rango High-Low\n"
    f"{inicio.strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{fin.strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel("Fecha y hora (UTC)")
plt.ylabel("Rango High-Low (USD)")

plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)

# Colocar el valor encima de cada barra
for i, valor in enumerate(top_10["rango_usd"]):
    plt.text(
        i,
        valor,
        f"{valor:.2f}",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

ruta = "graficas/actividad_07_mayores_rangos.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nGráfica guardada en:")
print(ruta)

plt.show()