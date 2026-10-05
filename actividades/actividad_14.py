import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar datos
df = pd.read_csv("datos_solana_7_dias.csv")

# Convertir fecha a UTC
df["time"] = pd.to_datetime(df["time"], utc=True)

# Cambio porcentual de cada vela
df["cambio_pct"] = (
    (df["close"] - df["open"]) / df["open"]
) * 100

# Rango de cada vela
df["rango_usd"] = df["high"] - df["low"]

# Obtener día de la semana
df["dia_num"] = df["time"].dt.dayofweek

dias = {
    0: "Lunes",
    1: "Martes",
    2: "Miércoles",
    3: "Jueves",
    4: "Viernes",
    5: "Sábado",
    6: "Domingo"
}

df["dia_semana"] = df["dia_num"].map(dias)

# Resumen por día
resumen = (
    df.groupby(["dia_num", "dia_semana"])
    .agg(
        cantidad_velas=("time", "count"),
        cambio_promedio_pct=("cambio_pct", "mean"),
        rango_promedio_usd=("rango_usd", "mean"),
        volumen_ticks_promedio=("tick_volume", "mean")
    )
    .reset_index()
    .sort_values("dia_num")
)

# Comprobar fin de semana
datos_sabado = len(df[df["dia_num"] == 5])
datos_domingo = len(df[df["dia_num"] == 6])

# Días destacados
mayor_subida = resumen.loc[
    resumen["cambio_promedio_pct"].idxmax()
]

mayor_caida = resumen.loc[
    resumen["cambio_promedio_pct"].idxmin()
]

mayor_rango = resumen.loc[
    resumen["rango_promedio_usd"].idxmax()
]

print("ACTIVIDAD 14 - COMPORTAMIENTO POR DÍA DE LA SEMANA")
print("---------------------------------------------------")
print("Símbolo: SOLUSD")
print("Temporalidad: H1")
print("Registros analizados:", len(df))

print("\nPeríodo analizado:")
print("Desde:", df["time"].min())
print("Hasta:", df["time"].max())

print("\nRESUMEN POR DÍA DE LA SEMANA:")
print(
    resumen[
        [
            "dia_semana",
            "cantidad_velas",
            "cambio_promedio_pct",
            "rango_promedio_usd",
            "volumen_ticks_promedio"
        ]
    ].to_string(index=False)
)

print("\nCOMPROBACIÓN DEL FIN DE SEMANA:")
print(f"Velas del sábado: {datos_sabado}")
print(f"Velas del domingo: {datos_domingo}")

if datos_sabado > 0:
    print("La fuente SÍ proporcionó datos durante el sábado.")
else:
    print("La fuente NO proporcionó datos durante el sábado.")

if datos_domingo > 0:
    print("La fuente SÍ proporcionó datos durante el domingo.")
else:
    print("La fuente NO proporcionó datos durante el domingo.")

print("\nDÍA CON MAYOR CAMBIO POSITIVO PROMEDIO:")
print(mayor_subida["dia_semana"])
print(
    f"Cambio promedio: "
    f"{mayor_subida['cambio_promedio_pct']:.4f}%"
)

print("\nDÍA CON MAYOR CAMBIO NEGATIVO PROMEDIO:")
print(mayor_caida["dia_semana"])
print(
    f"Cambio promedio: "
    f"{mayor_caida['cambio_promedio_pct']:.4f}%"
)

print("\nDÍA CON MAYOR RANGO PROMEDIO:")
print(mayor_rango["dia_semana"])
print(
    f"Rango promedio: "
    f"{mayor_rango['rango_promedio_usd']:.4f} USD"
)

# Guardar resumen
resumen.to_csv(
    "resumen_dia_semana_solana.csv",
    index=False
)

# Crear carpeta
os.makedirs("graficas", exist_ok=True)

# Gráfica
plt.figure(figsize=(12, 7))

barras = plt.bar(
    resumen["dia_semana"],
    resumen["cambio_promedio_pct"]
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title(
    "Cambio porcentual promedio de SOLUSD por día de la semana\n"
    "2026-09-25 21:00 UTC - 2026-10-02 20:00 UTC"
)

plt.xlabel("Día de la semana (UTC)")
plt.ylabel("Cambio promedio por vela (%)")

plt.grid(
    axis="y",
    alpha=0.3
)

for barra, valor in zip(
    barras,
    resumen["cambio_promedio_pct"]
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
        va=alineacion
    )

plt.tight_layout()

ruta = "graficas/actividad_14_dias_semana.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nResumen guardado en:")
print("resumen_dia_semana_solana.csv")

print("\nGráfica guardada en:")
print(ruta)

plt.show()