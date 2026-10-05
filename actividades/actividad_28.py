import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import os


print("=" * 70)
print("ACTIVIDAD 28 - ANÁLISIS DE CUATRO SEMANAS")
print("=" * 70)


# ==========================================================
# 1. CONFIGURACIÓN
# ==========================================================

SIMBOLO = "SOLUSD"

INICIO = datetime(
    2026, 9, 4, 21, 0,
    tzinfo=timezone.utc
)

FIN = datetime(
    2026, 10, 2, 21, 0,
    tzinfo=timezone.utc
)

print("\nCONFIGURACIÓN")
print(f"Símbolo: {SIMBOLO}")

print(
    "Período solicitado: "
    f"{INICIO.strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{FIN.strftime('%Y-%m-%d %H:%M UTC')}"
)

print("Temporalidad: H1")


# ==========================================================
# 2. CONECTAR CON METATRADER 5
# ==========================================================

if not mt5.initialize():

    raise RuntimeError(
        f"No se pudo iniciar MetaTrader 5: "
        f"{mt5.last_error()}"
    )


try:

    if not mt5.symbol_select(
        SIMBOLO,
        True
    ):

        raise RuntimeError(
            f"No se pudo seleccionar {SIMBOLO}"
        )


    # ======================================================
    # 3. CONSULTAR DATOS
    # ======================================================

    datos = mt5.copy_rates_range(
        SIMBOLO,
        mt5.TIMEFRAME_H1,
        INICIO,
        FIN
    )

finally:

    mt5.shutdown()


if datos is None or len(datos) == 0:

    raise RuntimeError(
        "MetaTrader 5 no devolvió datos "
        "para el período solicitado."
    )


# ==========================================================
# 4. CREAR DATAFRAME
# ==========================================================

df = pd.DataFrame(
    datos
)

df["time"] = pd.to_datetime(
    df["time"],
    unit="s",
    utc=True
)

df = df[
    (df["time"] >= INICIO)
    & (df["time"] <= FIN)
].copy()

df = df.sort_values(
    "time"
).reset_index(
    drop=True
)


print("\nDATOS OBTENIDOS")

print(
    f"Registros: {len(df)}"
)

print(
    f"Forma: {df.shape}"
)

print(
    f"Valores faltantes: "
    f"{df.isnull().sum().sum()}"
)

print(
    "Primer registro: "
    f"{df['time'].min()}"
)

print(
    "Último registro: "
    f"{df['time'].max()}"
)


# ==========================================================
# 5. DIVIDIR EN CUATRO SEMANAS
# ==========================================================

# Cada bloque representa 7 días desde el inicio solicitado.

segundos_desde_inicio = (
    df["time"] - INICIO
).dt.total_seconds()

df["semana_numero"] = (
    segundos_desde_inicio
    // (7 * 24 * 60 * 60)
).astype(int) + 1


# El registro exactamente en FIN pertenece al cierre del
# período y se mantiene dentro de la semana 4.

df.loc[
    df["semana_numero"] > 4,
    "semana_numero"
] = 4


df["semana"] = (
    "Semana "
    + df["semana_numero"].astype(str)
)


# ==========================================================
# 6. RESUMEN POR SEMANA
# ==========================================================

resumen = (
    df.groupby(
        [
            "semana_numero",
            "semana"
        ]
    )
    .agg(
        inicio=("time", "min"),
        fin=("time", "max"),
        registros=("time", "count"),
        apertura=("open", "first"),
        cierre=("close", "last"),
        maximo=("high", "max"),
        minimo=("low", "min"),
        desviacion_cierre=("close", "std"),
        volumen_ticks=("tick_volume", "sum"),
        promedio_ticks=("tick_volume", "mean")
    )
    .reset_index()
)


# ==========================================================
# 7. MÉTRICAS SEMANALES
# ==========================================================

resumen["variacion_precio_pct"] = (
    (
        resumen["cierre"]
        - resumen["apertura"]
    )
    / resumen["apertura"]
) * 100


resumen["rango_usd"] = (
    resumen["maximo"]
    - resumen["minimo"]
)


# ==========================================================
# 8. MOSTRAR COMPARACIÓN
# ==========================================================

print("\n" + "=" * 70)
print("COMPARACIÓN SEMANAL")
print("=" * 70)


for _, fila in resumen.iterrows():

    print(
        f"\n{fila['semana']}"
    )

    print(
        "Período observado: "
        f"{fila['inicio'].strftime('%Y-%m-%d %H:%M UTC')} - "
        f"{fila['fin'].strftime('%Y-%m-%d %H:%M UTC')}"
    )

    print(
        f"Registros: "
        f"{int(fila['registros'])}"
    )

    print(
        f"Apertura: "
        f"{fila['apertura']:.2f} USD"
    )

    print(
        f"Cierre: "
        f"{fila['cierre']:.2f} USD"
    )

    print(
        f"Variación del precio: "
        f"{fila['variacion_precio_pct']:+.2f}%"
    )

    print(
        f"Máximo: "
        f"{fila['maximo']:.2f} USD"
    )

    print(
        f"Mínimo: "
        f"{fila['minimo']:.2f} USD"
    )

    print(
        f"Rango: "
        f"{fila['rango_usd']:.2f} USD"
    )

    print(
        f"Desviación estándar del cierre: "
        f"{fila['desviacion_cierre']:.4f} USD"
    )

    print(
        f"Volumen total de ticks: "
        f"{int(fila['volumen_ticks'])}"
    )

    print(
        f"Promedio de ticks por vela: "
        f"{fila['promedio_ticks']:.2f}"
    )


# ==========================================================
# 9. IDENTIFICAR EXTREMOS
# ==========================================================

mayor_subida = resumen.loc[
    resumen["variacion_precio_pct"].idxmax()
]

mayor_caida = resumen.loc[
    resumen["variacion_precio_pct"].idxmin()
]

mayor_rango = resumen.loc[
    resumen["rango_usd"].idxmax()
]

mayor_variabilidad = resumen.loc[
    resumen["desviacion_cierre"].idxmax()
]

mayor_volumen = resumen.loc[
    resumen["volumen_ticks"].idxmax()
]


print("\n" + "=" * 70)
print("RESULTADOS DESTACADOS")
print("=" * 70)

print(
    "Mayor variación semanal: "
    f"{mayor_subida['semana']} "
    f"({mayor_subida['variacion_precio_pct']:+.2f}%)"
)

print(
    "Menor variación semanal: "
    f"{mayor_caida['semana']} "
    f"({mayor_caida['variacion_precio_pct']:+.2f}%)"
)

print(
    "Mayor rango semanal: "
    f"{mayor_rango['semana']} "
    f"({mayor_rango['rango_usd']:.2f} USD)"
)

print(
    "Mayor variabilidad del cierre: "
    f"{mayor_variabilidad['semana']} "
    f"({mayor_variabilidad['desviacion_cierre']:.4f} USD)"
)

print(
    "Mayor volumen total de ticks: "
    f"{mayor_volumen['semana']} "
    f"({int(mayor_volumen['volumen_ticks'])} ticks)"
)


# ==========================================================
# 10. GUARDAR CSV
# ==========================================================

df.to_csv(
    "solana_4_semanas.csv",
    index=False
)

resumen.to_csv(
    "comparacion_semanal_solana.csv",
    index=False
)

print(
    "\nArchivo guardado: solana_4_semanas.csv"
)

print(
    "Archivo guardado: comparacion_semanal_solana.csv"
)


# ==========================================================
# 11. GRÁFICA DE PRECIO DE LAS 4 SEMANAS
# ==========================================================

os.makedirs(
    "graficas",
    exist_ok=True
)

ruta_precio = (
    "graficas/actividad_28_precio_4_semanas.png"
)

plt.figure(
    figsize=(14, 7)
)

plt.plot(
    df["time"],
    df["close"]
)

plt.title(
    "SOLUSD - Precio de cierre durante cuatro semanas\n"
    f"{INICIO.strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{FIN.strftime('%Y-%m-%d %H:%M UTC')}"
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

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    ruta_precio,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================================
# 12. GRÁFICA DE VARIACIÓN SEMANAL
# ==========================================================

ruta_variacion = (
    "graficas/actividad_28_variacion_semanal.png"
)

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    resumen["semana"],
    resumen["variacion_precio_pct"]
)

plt.axhline(
    0,
    linewidth=1
)

plt.title(
    "SOLUSD - Variación del precio por semana"
)

plt.xlabel(
    "Semana"
)

plt.ylabel(
    "Variación del precio (%)"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    ruta_variacion,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================================
# 13. GRÁFICA DE RANGO SEMANAL
# ==========================================================

ruta_rango = (
    "graficas/actividad_28_rango_semanal.png"
)

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    resumen["semana"],
    resumen["rango_usd"]
)

plt.title(
    "SOLUSD - Rango de precios por semana"
)

plt.xlabel(
    "Semana"
)

plt.ylabel(
    "Rango máximo - mínimo (USD)"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    ruta_rango,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================================
# 14. GRÁFICA DE VARIABILIDAD
# ==========================================================

ruta_variabilidad = (
    "graficas/actividad_28_variabilidad_semanal.png"
)

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    resumen["semana"],
    resumen["desviacion_cierre"]
)

plt.title(
    "SOLUSD - Variabilidad del cierre por semana"
)

plt.xlabel(
    "Semana"
)

plt.ylabel(
    "Desviación estándar del cierre (USD)"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    ruta_variabilidad,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================================
# 15. GRÁFICA DE VOLUMEN DE TICKS
# ==========================================================

ruta_volumen = (
    "graficas/actividad_28_volumen_semanal.png"
)

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    resumen["semana"],
    resumen["volumen_ticks"]
)

plt.title(
    "SOLUSD - Volumen de ticks por semana"
)

plt.xlabel(
    "Semana"
)

plt.ylabel(
    "Volumen total de ticks"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    ruta_volumen,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print("\nGRÁFICAS GUARDADAS")

print(
    ruta_precio
)

print(
    ruta_variacion
)

print(
    ruta_rango
)

print(
    ruta_variabilidad
)

print(
    ruta_volumen
)


# ==========================================================
# 16. INTERPRETACIÓN
# ==========================================================

print("\nINTERPRETACIÓN")

print(
    "La comparación semanal permite observar cómo cambiaron "
    "el precio, el rango, la variabilidad del cierre y el volumen "
    "de ticks durante las cuatro semanas analizadas."
)

print(
    "La desviación estándar del cierre se utiliza como una medida "
    "descriptiva de la dispersión de los precios dentro de cada semana."
)

print(
    "El volumen de ticks corresponde a las actualizaciones registradas "
    "por la fuente de MetaTrader 5 y no necesariamente representa "
    "el volumen total de SOL negociado en todo el mercado."
)

print(
    "Las diferencias observadas describen este período concreto "
    "y no constituyen una predicción del comportamiento futuro."
)


print("\n" + "=" * 70)
print("ACTIVIDAD 28 FINALIZADA")
print("=" * 70)