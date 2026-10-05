import pandas as pd
import matplotlib.pyplot as plt
import os


print("=" * 70)
print("ACTIVIDAD 21 - VARIACIÓN ACUMULADA")
print("=" * 70)


# ==========================================================
# 1. CARGAR LOS DATOS
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
print(f"Símbolo: SOLUSD")
print(f"Registros: {len(df)}")
print(f"Forma: {df.shape}")
print(f"Valores faltantes: {df.isnull().sum().sum()}")

print(
    f"Período: {df['time'].min()} "
    f"hasta {df['time'].max()}"
)


# ==========================================================
# 2. PRECIO INICIAL
# ==========================================================

precio_inicial = df["close"].iloc[0]

fecha_inicial = df["time"].iloc[0]

print("\nPRECIO DE REFERENCIA")

print(
    f"Fecha inicial: "
    f"{fecha_inicial.strftime('%Y-%m-%d %H:%M UTC')}"
)

print(
    f"Precio de cierre inicial: "
    f"{precio_inicial:.2f} USD"
)


# ==========================================================
# 3. CALCULAR VARIACIÓN ACUMULADA
# ==========================================================

df["variacion_acumulada_pct"] = (
    (
        df["close"] - precio_inicial
    )
    / precio_inicial
) * 100


# ==========================================================
# 4. RESULTADOS
# ==========================================================

precio_final = df["close"].iloc[-1]

fecha_final = df["time"].iloc[-1]

variacion_final = (
    df["variacion_acumulada_pct"].iloc[-1]
)

max_variacion = (
    df["variacion_acumulada_pct"].max()
)

min_variacion = (
    df["variacion_acumulada_pct"].min()
)

fila_max = df.loc[
    df["variacion_acumulada_pct"].idxmax()
]

fila_min = df.loc[
    df["variacion_acumulada_pct"].idxmin()
]


print("\nRESULTADOS")

print(
    f"Precio final: "
    f"{precio_final:.2f} USD"
)

print(
    f"Fecha final: "
    f"{fecha_final.strftime('%Y-%m-%d %H:%M UTC')}"
)

print(
    f"Variación acumulada final: "
    f"{variacion_final:+.2f}%"
)

print(
    f"\nMayor variación acumulada: "
    f"{max_variacion:+.2f}%"
)

print(
    "Fecha de la mayor variación: "
    f"{fila_max['time'].strftime('%Y-%m-%d %H:%M UTC')}"
)

print(
    f"Precio: {fila_max['close']:.2f} USD"
)

print(
    f"\nMenor variación acumulada: "
    f"{min_variacion:+.2f}%"
)

print(
    "Fecha de la menor variación: "
    f"{fila_min['time'].strftime('%Y-%m-%d %H:%M UTC')}"
)

print(
    f"Precio: {fila_min['close']:.2f} USD"
)


# ==========================================================
# 5. GUARDAR RESULTADOS
# ==========================================================

resultado = df[
    [
        "time",
        "close",
        "variacion_acumulada_pct"
    ]
].copy()

resultado.to_csv(
    "variacion_acumulada_solana.csv",
    index=False
)

print(
    "\nArchivo guardado: "
    "variacion_acumulada_solana.csv"
)


# ==========================================================
# 6. GENERAR GRÁFICA
# ==========================================================

os.makedirs(
    "graficas",
    exist_ok=True
)

ruta_grafica = (
    "graficas/actividad_21_variacion_acumulada.png"
)

plt.figure(
    figsize=(14, 7)
)

plt.plot(
    df["time"],
    df["variacion_acumulada_pct"],
    label="Variación acumulada"
)

plt.axhline(
    y=0,
    linestyle="--",
    linewidth=1,
    label="Nivel inicial (0%)"
)

plt.scatter(
    fila_max["time"],
    fila_max["variacion_acumulada_pct"],
    s=70,
    label="Máximo"
)

plt.scatter(
    fila_min["time"],
    fila_min["variacion_acumulada_pct"],
    s=70,
    label="Mínimo"
)

plt.title(
    "SOLUSD - Variación acumulada respecto al cierre inicial\n"
    f"{df['time'].min().strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{df['time'].max().strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel(
    "Fecha y hora (UTC)"
)

plt.ylabel(
    "Variación acumulada (%)"
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
# 7. INTERPRETACIÓN
# ==========================================================

print("\nINTERPRETACIÓN")

if variacion_final > 0:
    print(
        "Al finalizar el período, SOLUSD se encontraba "
        f"{variacion_final:.2f}% por encima del cierre inicial."
    )

elif variacion_final < 0:
    print(
        "Al finalizar el período, SOLUSD se encontraba "
        f"{abs(variacion_final):.2f}% por debajo del cierre inicial."
    )

else:
    print(
        "Al finalizar el período, SOLUSD se encontraba "
        "en el mismo nivel que el cierre inicial."
    )


print("\n" + "=" * 70)
print("ACTIVIDAD 21 FINALIZADA")
print("=" * 70)