import pandas as pd
import matplotlib.pyplot as plt
import os


print("=" * 70)
print("ACTIVIDAD 23 - DISTANCIA RESPECTO AL MÁXIMO DE 24 VELAS")
print("=" * 70)


# ==========================================================
# 1. CARGAR DATOS
# ==========================================================

archivo = "celery_velas_solana.csv"

if not os.path.exists(archivo):
    raise FileNotFoundError(
        f"No se encontró el archivo {archivo}"
    )

df = pd.read_csv(archivo)

df["time"] = pd.to_datetime(
    df["time"],
    utc=True
)

print("\nDATOS CARGADOS")
print("Símbolo: SOLUSD")
print(f"Registros: {len(df)}")
print(f"Forma: {df.shape}")
print(f"Valores faltantes: {df.isnull().sum().sum()}")

print(
    f"Período: {df['time'].min()} "
    f"hasta {df['time'].max()}"
)


# ==========================================================
# 2. MÁXIMO DE LAS ÚLTIMAS 24 VELAS
# ==========================================================

df["maximo_24_velas"] = (
    df["high"]
    .rolling(
        window=24,
        min_periods=24
    )
    .max()
)


# ==========================================================
# 3. DISTANCIA DEL CIERRE AL MÁXIMO
# ==========================================================

df["distancia_maximo_usd"] = (
    df["maximo_24_velas"]
    - df["close"]
)

df["distancia_maximo_pct"] = (
    (
        df["maximo_24_velas"]
        - df["close"]
    )
    / df["maximo_24_velas"]
) * 100


# ==========================================================
# 4. DATOS VÁLIDOS
# ==========================================================

resultado = df.dropna(
    subset=["maximo_24_velas"]
).copy()

print("\nCÁLCULO DE VENTANA MÓVIL")

print(
    f"Velas necesarias para cada ventana: 24"
)

print(
    f"Registros con cálculo disponible: {len(resultado)}"
)

print(
    f"Registros iniciales sin cálculo: "
    f"{df['maximo_24_velas'].isna().sum()}"
)


# ==========================================================
# 5. MAYOR DISTANCIA
# ==========================================================

fila_mayor = resultado.loc[
    resultado["distancia_maximo_pct"].idxmax()
]

print("\nMAYOR DISTANCIA RESPECTO AL MÁXIMO RECIENTE")

print(
    "Fecha: "
    f"{fila_mayor['time'].strftime('%Y-%m-%d %H:%M UTC')}"
)

print(
    f"Cierre: {fila_mayor['close']:.2f} USD"
)

print(
    f"Máximo últimas 24 velas: "
    f"{fila_mayor['maximo_24_velas']:.2f} USD"
)

print(
    f"Distancia: "
    f"{fila_mayor['distancia_maximo_usd']:.2f} USD"
)

print(
    f"Distancia porcentual: "
    f"{fila_mayor['distancia_maximo_pct']:.2f}%"
)


# ==========================================================
# 6. SITUACIÓN AL FINAL DEL PERÍODO
# ==========================================================

ultima = resultado.iloc[-1]

print("\nSITUACIÓN AL FINAL DEL PERÍODO")

print(
    "Fecha: "
    f"{ultima['time'].strftime('%Y-%m-%d %H:%M UTC')}"
)

print(
    f"Cierre actual: "
    f"{ultima['close']:.2f} USD"
)

print(
    f"Máximo de las últimas 24 velas: "
    f"{ultima['maximo_24_velas']:.2f} USD"
)

print(
    f"Distancia actual: "
    f"{ultima['distancia_maximo_usd']:.2f} USD"
)

print(
    f"Distancia porcentual actual: "
    f"{ultima['distancia_maximo_pct']:.2f}%"
)


# ==========================================================
# 7. TOP 10 MAYORES DISTANCIAS
# ==========================================================

top10 = (
    resultado.nlargest(
        10,
        "distancia_maximo_pct"
    )[
        [
            "time",
            "close",
            "maximo_24_velas",
            "distancia_maximo_usd",
            "distancia_maximo_pct"
        ]
    ]
    .copy()
)

print("\nTOP 10 MAYORES DISTANCIAS")

for _, fila in top10.iterrows():

    print(
        f"{fila['time'].strftime('%Y-%m-%d %H:%M UTC')} | "
        f"Cierre: {fila['close']:.2f} | "
        f"Máximo 24: {fila['maximo_24_velas']:.2f} | "
        f"Distancia: {fila['distancia_maximo_pct']:.2f}%"
    )


# ==========================================================
# 8. GUARDAR CSV
# ==========================================================

resultado[
    [
        "time",
        "close",
        "maximo_24_velas",
        "distancia_maximo_usd",
        "distancia_maximo_pct"
    ]
].to_csv(
    "distancia_maximo_24_solana.csv",
    index=False
)

top10.to_csv(
    "top10_distancia_maximo_24_solana.csv",
    index=False
)

print(
    "\nArchivo guardado: distancia_maximo_24_solana.csv"
)

print(
    "Archivo guardado: top10_distancia_maximo_24_solana.csv"
)


# ==========================================================
# 9. GRÁFICA
# ==========================================================

os.makedirs(
    "graficas",
    exist_ok=True
)

ruta_grafica = (
    "graficas/actividad_23_distancia_maximo_24.png"
)

plt.figure(
    figsize=(14, 7)
)

plt.plot(
    resultado["time"],
    resultado["close"],
    label="Precio de cierre"
)

plt.plot(
    resultado["time"],
    resultado["maximo_24_velas"],
    label="Máximo móvil de 24 velas"
)

plt.scatter(
    fila_mayor["time"],
    fila_mayor["close"],
    s=80,
    label="Mayor distancia"
)

plt.title(
    "SOLUSD - Cierre frente al máximo de las últimas 24 velas\n"
    f"{resultado['time'].min().strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{resultado['time'].max().strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel(
    "Fecha y hora (UTC)"
)

plt.ylabel(
    "Precio (USD)"
)

plt.grid(
    alpha=0.3
)

plt.legend()

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    ruta_grafica,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"Gráfica guardada: {ruta_grafica}"
)


# ==========================================================
# 10. INTERPRETACIÓN
# ==========================================================

print("\nINTERPRETACIÓN")

print(
    "La distancia porcentual indica cuánto se encuentra el cierre "
    "de cada vela por debajo del precio máximo observado durante "
    "las últimas 24 velas."
)

print(
    "Una distancia mayor representa una separación más amplia "
    "respecto al máximo reciente, pero no permite por sí sola "
    "predecir movimientos futuros."
)


print("\n" + "=" * 70)
print("ACTIVIDAD 23 FINALIZADA")
print("=" * 70)