import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar datos
df = pd.read_csv("datos_solana_7_dias.csv")

# Convertir fecha a UTC
df["time"] = pd.to_datetime(df["time"], utc=True)

# Ordenar cronológicamente
df = df.sort_values("time").reset_index(drop=True)

# Calcular media móvil de 20 velas
df["ma20"] = df["close"].rolling(window=20).mean()

# Determinar posición respecto a la media móvil
df["encima_ma20"] = df["close"] > df["ma20"]

# Detectar cruces de abajo hacia arriba
df["cruce_alcista"] = (
    (df["encima_ma20"] == True) &
    (df["encima_ma20"].shift(1) == False) &
    (df["ma20"].notna()) &
    (df["ma20"].shift(1).notna())
)

cruces = df[df["cruce_alcista"]].copy()

print("ACTIVIDAD 15 - MEDIA MÓVIL DE 20 VELAS")
print("----------------------------------------")
print("Símbolo: SOLUSD")
print("Temporalidad: H1")
print("Ventana de media móvil: 20 velas")
print("Registros analizados:", len(df))

print("\nPeríodo analizado:")
print("Desde:", df["time"].min())
print("Hasta:", df["time"].max())

print("\nPrimer valor disponible de MA20:")

primer_ma = df[df["ma20"].notna()].iloc[0]

print("Fecha:", primer_ma["time"])
print(f"Cierre: {primer_ma['close']:.2f} USD")
print(f"MA20: {primer_ma['ma20']:.2f} USD")

print("\nCRUCES DEL CIERRE DE ABAJO HACIA ARRIBA DE LA MA20:")
print("Cantidad de cruces:", len(cruces))

if len(cruces) > 0:
    print(
        cruces[
            ["time", "close", "ma20"]
        ].to_string(index=False)
    )
else:
    print("No se detectaron cruces alcistas durante el período.")

# Guardar resultados
df.to_csv(
    "media_movil_solana.csv",
    index=False
)

cruces[
    ["time", "close", "ma20"]
].to_csv(
    "cruces_ma20_solana.csv",
    index=False
)

# Crear carpeta de gráficas
os.makedirs("graficas", exist_ok=True)

# Crear gráfica
plt.figure(figsize=(15, 8))

plt.plot(
    df["time"],
    df["close"],
    label="Precio de cierre"
)

plt.plot(
    df["time"],
    df["ma20"],
    label="Media móvil 20 velas",
    linewidth=2
)

# Marcar cruces
if len(cruces) > 0:
    plt.scatter(
        cruces["time"],
        cruces["close"],
        s=80,
        zorder=5,
        label="Cruce de abajo hacia arriba"
    )

    for _, fila in cruces.iterrows():
        plt.annotate(
            fila["time"].strftime("%m-%d %H:%M"),
            (fila["time"], fila["close"]),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            fontsize=8
        )

plt.title(
    "Precio de cierre de SOLUSD y media móvil de 20 velas\n"
    "2026-09-25 21:00 UTC - 2026-10-02 20:00 UTC"
)

plt.xlabel("Fecha y hora (UTC)")
plt.ylabel("Precio (USD)")

plt.legend()
plt.grid(alpha=0.3)

plt.xticks(rotation=45)

plt.tight_layout()

ruta = "graficas/actividad_15_media_movil.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nDatos guardados en:")
print("media_movil_solana.csv")
print("cruces_ma20_solana.csv")

print("\nGráfica guardada en:")
print(ruta)

plt.show()