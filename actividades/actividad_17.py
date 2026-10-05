import pandas as pd
import matplotlib.pyplot as plt
import os

SIMBOLO = "SOLUSD"
ARCHIVO = "datos_solana_7_dias.csv"

# Cargar datos
df = pd.read_csv(ARCHIVO)

# Convertir fecha a datetime UTC
df["time"] = pd.to_datetime(df["time"], utc=True)

# Conservar copia original
df_original = df.copy()

# Calcular cambio porcentual horario
df["cambio_pct"] = df["close"].pct_change() * 100

# Magnitud absoluta del movimiento
df["movimiento_abs_pct"] = df["cambio_pct"].abs()

# Seleccionar las 10 velas con mayor volumen de ticks
top_10_volumen = (
    df.nlargest(10, "tick_volume")
    [["time", "close", "tick_volume", "cambio_pct", "movimiento_abs_pct"]]
    .sort_values("tick_volume", ascending=False)
)

# Período
inicio = df["time"].min()
fin = df["time"].max()

print("ACTIVIDAD 17 - VOLUMEN DE TICKS")
print("--------------------------------")
print(f"Símbolo: {SIMBOLO}")
print("Temporalidad: H1")
print(f"Registros analizados: {len(df)}")

print("\nPeríodo analizado:")
print(f"Desde: {inicio}")
print(f"Hasta: {fin}")

print("\n10 VELAS CON MAYOR VOLUMEN DE TICKS:")
print(
    top_10_volumen.to_string(
        index=False,
        formatters={
            "close": "{:.2f}".format,
            "cambio_pct": "{:.4f}".format,
            "movimiento_abs_pct": "{:.4f}".format
        }
    )
)

# Estadísticas para examinar la relación
promedio_movimiento_general = df["movimiento_abs_pct"].mean()

promedio_movimiento_top = (
    top_10_volumen["movimiento_abs_pct"].mean()
)

print("\nCOMPARACIÓN DE MOVIMIENTOS:")
print(
    f"Movimiento absoluto promedio de todas las velas: "
    f"{promedio_movimiento_general:.4f}%"
)

print(
    f"Movimiento absoluto promedio de las 10 velas "
    f"con mayor volumen: {promedio_movimiento_top:.4f}%"
)

if promedio_movimiento_top > promedio_movimiento_general:
    print(
        "En este período, las velas con mayor volumen de ticks "
        "presentaron en promedio movimientos mayores que el conjunto total."
    )
else:
    print(
        "En este período, un volumen de ticks elevado no estuvo acompañado "
        "necesariamente por movimientos mayores del precio."
    )

print("\nACLARACIÓN:")
print(
    "El volumen de ticks representa la cantidad de cambios o actualizaciones "
    "de precio registrados por la fuente de MetaTrader 5. No representa "
    "necesariamente todo el volumen de SOL negociado en el mercado."
)

# Guardar tabla
top_10_volumen.to_csv(
    "mayor_volumen_ticks_solana.csv",
    index=False
)

# Crear carpeta
os.makedirs("graficas", exist_ok=True)

# Gráfica
fig, ax1 = plt.subplots(figsize=(15, 7))

# Precio
ax1.plot(
    df["time"],
    df["close"],
    label="Precio de cierre"
)

ax1.set_xlabel("Fecha y hora (UTC)")
ax1.set_ylabel("Precio de cierre (USD)")

# Segundo eje para volumen
ax2 = ax1.twinx()

ax2.bar(
    df["time"],
    df["tick_volume"],
    width=0.025,
    alpha=0.25,
    label="Volumen de ticks"
)

ax2.set_ylabel("Volumen de ticks")

# Destacar top 10 sobre la línea del precio
ax1.scatter(
    top_10_volumen["time"],
    top_10_volumen["close"],
    s=80,
    zorder=5,
    label="Top 10 volumen"
)

# Etiquetas
for _, fila in top_10_volumen.iterrows():
    ax1.annotate(
        f'{int(fila["tick_volume"])}',
        (fila["time"], fila["close"]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=8
    )

plt.title(
    "Precio de SOLUSD y volumen de ticks\n"
    f"{inicio.strftime('%Y-%m-%d %H:%M')} UTC - "
    f"{fin.strftime('%Y-%m-%d %H:%M')} UTC"
)

# Combinar leyendas
lineas1, etiquetas1 = ax1.get_legend_handles_labels()
lineas2, etiquetas2 = ax2.get_legend_handles_labels()

ax1.legend(
    lineas1 + lineas2,
    etiquetas1 + etiquetas2,
    loc="upper right"
)

ax1.grid(alpha=0.3)

fig.autofmt_xdate()
fig.tight_layout()

ruta = "graficas/actividad_17_volumen_ticks.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nDatos guardados en:")
print("mayor_volumen_ticks_solana.csv")

print("\nGráfica guardada en:")
print(ruta)

plt.show()