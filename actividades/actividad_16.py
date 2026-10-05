import pandas as pd
import matplotlib.pyplot as plt
import os

SIMBOLO = "SOLUSD"
ARCHIVO = "datos_solana_7_dias.csv"

# Cargar los datos
df = pd.read_csv(ARCHIVO)

# Convertir la fecha a formato datetime UTC
df["time"] = pd.to_datetime(df["time"], utc=True)

# Conservar una copia de los datos originales
df_original = df.copy()

# Calcular el cambio porcentual respecto a la hora anterior
df["cambio_pct"] = df["close"].pct_change() * 100

# Variación absoluta
df["variacion_abs_pct"] = df["cambio_pct"].abs()

# Eliminar únicamente la primera fila, que no tiene cambio anterior
df_validos = df.dropna(subset=["variacion_abs_pct"]).copy()

# Seleccionar las 10 horas con mayor variación absoluta
top_10 = (
    df_validos
    .nlargest(10, "variacion_abs_pct")
    [["time", "close", "cambio_pct", "variacion_abs_pct"]]
    .sort_values("variacion_abs_pct", ascending=False)
)

# Período analizado
inicio = df["time"].min()
fin = df["time"].max()

print("ACTIVIDAD 16 - VARIACIÓN RECIENTE")
print("----------------------------------")
print(f"Símbolo: {SIMBOLO}")
print("Temporalidad: H1")
print(f"Registros analizados: {len(df)}")

print("\nPeríodo analizado:")
print(f"Desde: {inicio}")
print(f"Hasta: {fin}")

print("\nCRITERIO UTILIZADO:")
print(
    "Se considera variación elevada a las 10 velas con mayor "
    "cambio porcentual absoluto del precio de cierre respecto "
    "a la vela horaria anterior."
)

print("\n10 HORAS CON MAYOR VARIACIÓN:")
print(
    top_10.to_string(
        index=False,
        formatters={
            "close": "{:.2f}".format,
            "cambio_pct": "{:.4f}".format,
            "variacion_abs_pct": "{:.4f}".format
        }
    )
)

# Guardar resultados
top_10.to_csv(
    "variaciones_elevadas_solana.csv",
    index=False
)

# Crear carpeta de gráficas
os.makedirs("graficas", exist_ok=True)

# Gráfica
plt.figure(figsize=(15, 7))

plt.plot(
    df["time"],
    df["close"],
    label="Precio de cierre"
)

plt.scatter(
    top_10["time"],
    top_10["close"],
    s=80,
    zorder=5,
    label="Variación elevada"
)

# Etiquetas de los puntos
for _, fila in top_10.iterrows():

    signo = "+" if fila["cambio_pct"] > 0 else ""

    plt.annotate(
        f'{signo}{fila["cambio_pct"]:.2f}%',
        (fila["time"], fila["close"]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center",
        fontsize=8
    )

plt.title(
    "Horas con mayor variación porcentual de SOLUSD\n"
    f"{inicio.strftime('%Y-%m-%d %H:%M')} UTC - "
    f"{fin.strftime('%Y-%m-%d %H:%M')} UTC"
)

plt.xlabel("Fecha y hora (UTC)")
plt.ylabel("Precio de cierre (USD)")

plt.grid(alpha=0.3)
plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()

ruta = "graficas/actividad_16_variacion_reciente.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nDatos guardados en:")
print("variaciones_elevadas_solana.csv")

print("\nGráfica guardada en:")
print(ruta)

plt.show()