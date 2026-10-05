import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar los datos horarios
df = pd.read_csv("datos_solana_7_dias.csv")

# Convertir la fecha
df["time"] = pd.to_datetime(df["time"], utc=True)

# Extraer la hora UTC
df["hora_utc"] = df["time"].dt.hour

# Calcular cambio porcentual dentro de cada vela
df["cambio_vela_pct"] = (
    (df["close"] - df["open"]) / df["open"]
) * 100

# Agrupar por hora UTC
resumen_horas = (
    df.groupby("hora_utc")
    .agg(
        cambio_promedio_pct=("cambio_vela_pct", "mean"),
        rango_promedio_usd=("high", lambda x: 0),
        cantidad_velas=("time", "count")
    )
    .reset_index()
)

# Calcular correctamente el rango promedio por hora
df["rango_usd"] = df["high"] - df["low"]

rangos = (
    df.groupby("hora_utc")["rango_usd"]
    .mean()
    .reset_index(name="rango_promedio_usd")
)

resumen_horas = resumen_horas.drop(
    columns=["rango_promedio_usd"]
).merge(
    rangos,
    on="hora_utc"
)

# Ordenar
resumen_horas = resumen_horas.sort_values("hora_utc")

# Encontrar horas destacadas
hora_mayor_subida = resumen_horas.loc[
    resumen_horas["cambio_promedio_pct"].idxmax()
]

hora_mayor_caida = resumen_horas.loc[
    resumen_horas["cambio_promedio_pct"].idxmin()
]

hora_mayor_rango = resumen_horas.loc[
    resumen_horas["rango_promedio_usd"].idxmax()
]

print("ACTIVIDAD 13 - COMPORTAMIENTO SEGÚN LA HORA")
print("---------------------------------------------")
print("Símbolo: SOLUSD")
print("Temporalidad: H1")
print("Registros analizados:", len(df))

print("\nPeríodo analizado:")
print("Desde:", df["time"].min())
print("Hasta:", df["time"].max())

print("\nRESUMEN POR HORA UTC:")
print(
    resumen_horas[
        [
            "hora_utc",
            "cantidad_velas",
            "cambio_promedio_pct",
            "rango_promedio_usd"
        ]
    ].to_string(index=False)
)

print("\nHORA CON MAYOR SUBIDA PROMEDIO:")
print(
    f"{int(hora_mayor_subida['hora_utc']):02d}:00 UTC"
)
print(
    f"Cambio promedio: "
    f"{hora_mayor_subida['cambio_promedio_pct']:.4f}%"
)

print("\nHORA CON MAYOR CAÍDA PROMEDIO:")
print(
    f"{int(hora_mayor_caida['hora_utc']):02d}:00 UTC"
)
print(
    f"Cambio promedio: "
    f"{hora_mayor_caida['cambio_promedio_pct']:.4f}%"
)

print("\nHORA CON MAYOR RANGO PROMEDIO:")
print(
    f"{int(hora_mayor_rango['hora_utc']):02d}:00 UTC"
)
print(
    f"Rango promedio: "
    f"{hora_mayor_rango['rango_promedio_usd']:.4f} USD"
)

# Guardar resultados
resumen_horas.to_csv(
    "resumen_horario_solana.csv",
    index=False
)

# Crear carpeta para gráficas
os.makedirs("graficas", exist_ok=True)

# Gráfica
plt.figure(figsize=(13, 7))

barras = plt.bar(
    resumen_horas["hora_utc"],
    resumen_horas["cambio_promedio_pct"]
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title(
    "Cambio porcentual promedio de SOLUSD según hora del día\n"
    "2026-09-25 21:00 UTC - 2026-10-02 20:00 UTC"
)

plt.xlabel("Hora del día (UTC)")
plt.ylabel("Cambio promedio por vela (%)")

plt.xticks(range(24))

plt.grid(
    axis="y",
    alpha=0.3
)

for barra, valor in zip(
    barras,
    resumen_horas["cambio_promedio_pct"]
):
    if valor >= 0:
        desplazamiento = 3
        alineacion = "bottom"
    else:
        desplazamiento = -3
        alineacion = "top"

    plt.annotate(
        f"{valor:.2f}%",
        (
            barra.get_x() + barra.get_width() / 2,
            barra.get_height()
        ),
        textcoords="offset points",
        xytext=(0, desplazamiento),
        ha="center",
        va=alineacion,
        fontsize=8
    )

plt.tight_layout()

ruta = "graficas/actividad_13_comportamiento_horario.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nResumen guardado en:")
print("resumen_horario_solana.csv")

print("\nGráfica guardada en:")
print(ruta)

plt.show()