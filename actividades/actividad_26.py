import pandas as pd
import matplotlib.pyplot as plt
import os


print("=" * 70)
print("ACTIVIDAD 26 - MOVIMIENTO DEL PRECIO VS VOLUMEN DE TICKS")
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
# 2. CALCULAR MOVIMIENTO PORCENTUAL
# ==========================================================

df["variacion_pct"] = (
    df["close"].pct_change() * 100
)

df["movimiento_abs_pct"] = (
    df["variacion_pct"].abs()
)

analisis = df.dropna(
    subset=[
        "movimiento_abs_pct",
        "tick_volume"
    ]
).copy()

print("\nDATOS PARA EL ANÁLISIS")

print(
    f"Observaciones disponibles: {len(analisis)}"
)


# ==========================================================
# 3. CORRELACIÓN
# ==========================================================

correlacion = analisis[
    "tick_volume"
].corr(
    analisis["movimiento_abs_pct"]
)

print("\nCORRELACIÓN")

print(
    "Correlación de Pearson entre volumen de ticks "
    "y magnitud del movimiento:"
)

print(
    f"{correlacion:.4f}"
)


# ==========================================================
# 4. INTERPRETAR INTENSIDAD
# ==========================================================

valor_abs = abs(correlacion)

if valor_abs < 0.20:
    intensidad = "muy débil"

elif valor_abs < 0.40:
    intensidad = "débil"

elif valor_abs < 0.60:
    intensidad = "moderada"

elif valor_abs < 0.80:
    intensidad = "fuerte"

else:
    intensidad = "muy fuerte"


if correlacion > 0:
    direccion = "positiva"

elif correlacion < 0:
    direccion = "negativa"

else:
    direccion = "nula"


print(
    f"Dirección: {direccion}"
)

print(
    f"Intensidad descriptiva: {intensidad}"
)


# ==========================================================
# 5. COMPARAR VOLUMEN ALTO Y RESTO
# ==========================================================

umbral_volumen = analisis[
    "tick_volume"
].quantile(0.90)

volumen_alto = analisis[
    analisis["tick_volume"] >= umbral_volumen
]

resto = analisis[
    analisis["tick_volume"] < umbral_volumen
]


movimiento_alto = volumen_alto[
    "movimiento_abs_pct"
].mean()

movimiento_resto = resto[
    "movimiento_abs_pct"
].mean()


print("\nCOMPARACIÓN DESCRIPTIVA")

print(
    f"Percentil 90 del volumen de ticks: "
    f"{umbral_volumen:.2f}"
)

print(
    f"Velas de volumen alto: "
    f"{len(volumen_alto)}"
)

print(
    f"Movimiento absoluto promedio con volumen alto: "
    f"{movimiento_alto:.4f}%"
)

print(
    f"Movimiento absoluto promedio en el resto: "
    f"{movimiento_resto:.4f}%"
)


# ==========================================================
# 6. TOP 10 MAYOR VOLUMEN
# ==========================================================

top10 = analisis.nlargest(
    10,
    "tick_volume"
)[
    [
        "time",
        "close",
        "tick_volume",
        "variacion_pct",
        "movimiento_abs_pct"
    ]
].copy()


print("\nTOP 10 VELAS POR VOLUMEN DE TICKS")

for _, fila in top10.iterrows():

    print(
        f"{fila['time'].strftime('%Y-%m-%d %H:%M UTC')} | "
        f"Ticks: {int(fila['tick_volume'])} | "
        f"Variación: {fila['variacion_pct']:+.4f}% | "
        f"Magnitud: {fila['movimiento_abs_pct']:.4f}%"
    )


# ==========================================================
# 7. GUARDAR RESULTADOS
# ==========================================================

analisis[
    [
        "time",
        "close",
        "tick_volume",
        "variacion_pct",
        "movimiento_abs_pct"
    ]
].to_csv(
    "movimiento_vs_ticks_solana.csv",
    index=False
)


resumen = pd.DataFrame({
    "Metrica": [
        "Observaciones",
        "Correlacion_Pearson",
        "Percentil_90_ticks",
        "Movimiento_promedio_volumen_alto_pct",
        "Movimiento_promedio_resto_pct"
    ],

    "Valor": [
        len(analisis),
        correlacion,
        umbral_volumen,
        movimiento_alto,
        movimiento_resto
    ]
})

resumen.to_csv(
    "resumen_movimiento_vs_ticks_solana.csv",
    index=False
)


print(
    "\nArchivo guardado: movimiento_vs_ticks_solana.csv"
)

print(
    "Archivo guardado: "
    "resumen_movimiento_vs_ticks_solana.csv"
)


# ==========================================================
# 8. GRÁFICO DE DISPERSIÓN
# ==========================================================

os.makedirs(
    "graficas",
    exist_ok=True
)

ruta_grafica = (
    "graficas/actividad_26_movimiento_vs_ticks.png"
)

plt.figure(
    figsize=(12, 7)
)

plt.scatter(
    analisis["tick_volume"],
    analisis["movimiento_abs_pct"],
    alpha=0.65
)

plt.title(
    "SOLUSD - Volumen de ticks vs magnitud del movimiento horario\n"
    f"{df['time'].min().strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{df['time'].max().strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel(
    "Volumen de ticks"
)

plt.ylabel(
    "Variación absoluta entre cierres (%)"
)

plt.grid(
    alpha=0.3
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
# 9. INTERPRETACIÓN
# ==========================================================

print("\nINTERPRETACIÓN")

print(
    f"En el período analizado se obtuvo una correlación "
    f"de Pearson de {correlacion:.4f}, clasificada de forma "
    f"descriptiva como {intensidad} y {direccion}."
)

print(
    "La correlación permite describir una asociación lineal "
    "entre las variables, pero no demuestra que el volumen "
    "de ticks cause los movimientos del precio."
)

print(
    "Además, el volumen de ticks de MetaTrader 5 representa "
    "la cantidad de actualizaciones o cambios de precio "
    "registrados por la fuente durante la vela."
)

print(
    "Por tanto, no debe interpretarse necesariamente como "
    "el volumen total de SOL negociado en todo el mercado."
)


print("\n" + "=" * 70)
print("ACTIVIDAD 26 FINALIZADA")
print("=" * 70)