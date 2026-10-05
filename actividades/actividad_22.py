import pandas as pd
import matplotlib.pyplot as plt
import os


print("=" * 70)
print("ACTIVIDAD 22 - RACHAS CONSECUTIVAS")
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
print(f"Símbolo: SOLUSD")
print(f"Registros: {len(df)}")
print(f"Forma: {df.shape}")
print(f"Valores faltantes: {df.isnull().sum().sum()}")

print(
    f"Período: {df['time'].min()} "
    f"hasta {df['time'].max()}"
)


# ==========================================================
# 2. CALCULAR CAMBIO ENTRE CIERRES
# ==========================================================

df["cambio"] = df["close"].diff()

df["variacion_pct"] = (
    df["close"].pct_change() * 100
)


def clasificar_movimiento(cambio):
    if pd.isna(cambio):
        return "Inicial"
    elif cambio > 0:
        return "Subida"
    elif cambio < 0:
        return "Bajada"
    else:
        return "Sin cambio"


df["movimiento"] = df["cambio"].apply(
    clasificar_movimiento
)


# ==========================================================
# 3. IDENTIFICAR RACHAS
# ==========================================================

datos_rachas = df[
    df["movimiento"].isin(
        ["Subida", "Bajada"]
    )
].copy()

datos_rachas["grupo"] = (
    datos_rachas["movimiento"]
    != datos_rachas["movimiento"].shift()
).cumsum()


rachas = (
    datos_rachas
    .groupby("grupo")
    .agg(
        tipo=("movimiento", "first"),
        inicio=("time", "first"),
        fin=("time", "last"),
        cantidad=("time", "count"),
        cierre_inicial=("close", "first"),
        cierre_final=("close", "last")
    )
    .reset_index(drop=True)
)


# ==========================================================
# 4. VARIACIÓN DURANTE CADA RACHA
# ==========================================================

rachas["variacion_rango_pct"] = (
    (
        rachas["cierre_final"]
        - rachas["cierre_inicial"]
    )
    / rachas["cierre_inicial"]
) * 100


# ==========================================================
# 5. RACHA MÁS LARGA DE SUBIDAS
# ==========================================================

rachas_subida = rachas[
    rachas["tipo"] == "Subida"
]

racha_subida = rachas_subida.loc[
    rachas_subida["cantidad"].idxmax()
]


# ==========================================================
# 6. RACHA MÁS LARGA DE BAJADAS
# ==========================================================

rachas_bajada = rachas[
    rachas["tipo"] == "Bajada"
]

racha_bajada = rachas_bajada.loc[
    rachas_bajada["cantidad"].idxmax()
]


print("\nRACHA MÁS LARGA DE SUBIDAS")

print(
    f"Cantidad de velas consecutivas: "
    f"{int(racha_subida['cantidad'])}"
)

print(
    "Inicio: "
    f"{racha_subida['inicio'].strftime('%Y-%m-%d %H:%M UTC')}"
)

print(
    "Fin: "
    f"{racha_subida['fin'].strftime('%Y-%m-%d %H:%M UTC')}"
)

print(
    f"Cierre inicial de la racha: "
    f"{racha_subida['cierre_inicial']:.2f} USD"
)

print(
    f"Cierre final de la racha: "
    f"{racha_subida['cierre_final']:.2f} USD"
)

print(
    f"Variación entre esos cierres: "
    f"{racha_subida['variacion_rango_pct']:+.2f}%"
)


print("\nRACHA MÁS LARGA DE BAJADAS")

print(
    f"Cantidad de velas consecutivas: "
    f"{int(racha_bajada['cantidad'])}"
)

print(
    "Inicio: "
    f"{racha_bajada['inicio'].strftime('%Y-%m-%d %H:%M UTC')}"
)

print(
    "Fin: "
    f"{racha_bajada['fin'].strftime('%Y-%m-%d %H:%M UTC')}"
)

print(
    f"Cierre inicial de la racha: "
    f"{racha_bajada['cierre_inicial']:.2f} USD"
)

print(
    f"Cierre final de la racha: "
    f"{racha_bajada['cierre_final']:.2f} USD"
)

print(
    f"Variación entre esos cierres: "
    f"{racha_bajada['variacion_rango_pct']:+.2f}%"
)


# ==========================================================
# 7. RESUMEN
# ==========================================================

print("\nRESUMEN DE RACHAS")

print(
    f"Rachas de subida encontradas: "
    f"{len(rachas_subida)}"
)

print(
    f"Rachas de bajada encontradas: "
    f"{len(rachas_bajada)}"
)


# ==========================================================
# 8. GUARDAR CSV
# ==========================================================

archivo_salida = "rachas_consecutivas_solana.csv"

rachas.to_csv(
    archivo_salida,
    index=False
)

print(
    f"\nArchivo guardado: {archivo_salida}"
)


# ==========================================================
# 9. GRÁFICA
# ==========================================================

os.makedirs(
    "graficas",
    exist_ok=True
)

ruta_grafica = (
    "graficas/actividad_22_rachas_consecutivas.png"
)

plt.figure(
    figsize=(14, 7)
)

plt.plot(
    df["time"],
    df["close"],
    label="Precio de cierre"
)

plt.axvspan(
    racha_subida["inicio"],
    racha_subida["fin"],
    alpha=0.25,
    label="Mayor racha de subidas"
)

plt.axvspan(
    racha_bajada["inicio"],
    racha_bajada["fin"],
    alpha=0.25,
    label="Mayor racha de bajadas"
)

plt.title(
    "SOLUSD - Rachas consecutivas de cambios de cierre\n"
    f"{df['time'].min().strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{df['time'].max().strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel(
    "Fecha y hora (UTC)"
)

plt.ylabel(
    "Precio de cierre (USD)"
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
    "Las rachas representan períodos en los que el precio de cierre "
    "subió o bajó consecutivamente respecto al cierre de la vela anterior."
)

print(
    "Estas secuencias describen el comportamiento observado durante "
    "el período analizado y no implican que el movimiento continuará."
)


print("\n" + "=" * 70)
print("ACTIVIDAD 22 FINALIZADA")
print("=" * 70)