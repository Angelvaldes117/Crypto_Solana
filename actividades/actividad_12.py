import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar resumen generado en la Actividad 11
df = pd.read_csv("resumen_diario_solana.csv")

df["fecha"] = pd.to_datetime(df["fecha"])

# Calcular rango diario
df["rango_usd"] = df["maximo"] - df["minimo"]

# Localizar los días destacados
dia_mayor_subida = df.loc[df["cambio_pct"].idxmax()]
dia_mayor_caida = df.loc[df["cambio_pct"].idxmin()]
dia_mayor_rango = df.loc[df["rango_usd"].idxmax()]

print("ACTIVIDAD 12 - COMPARACIÓN DE DÍAS")
print("----------------------------------")
print("Símbolo: SOLUSD")
print("Datos derivados de velas H1")

print("\nPeríodo analizado:")
print("Desde:", df["fecha"].min().strftime("%Y-%m-%d"))
print("Hasta:", df["fecha"].max().strftime("%Y-%m-%d"))

print("\nRESUMEN POR DÍA:")

print(
    df[
        [
            "fecha",
            "apertura",
            "maximo",
            "minimo",
            "cierre",
            "cambio_pct",
            "rango_usd",
            "cantidad_velas"
        ]
    ].to_string(index=False)
)

print("\nDÍA CON MAYOR SUBIDA:")
print("Fecha:", dia_mayor_subida["fecha"].strftime("%Y-%m-%d"))
print(f"Cambio: {dia_mayor_subida['cambio_pct']:.2f}%")

print("\nDÍA CON MAYOR CAÍDA:")
print("Fecha:", dia_mayor_caida["fecha"].strftime("%Y-%m-%d"))
print(f"Cambio: {dia_mayor_caida['cambio_pct']:.2f}%")

print("\nDÍA CON MAYOR RANGO:")
print("Fecha:", dia_mayor_rango["fecha"].strftime("%Y-%m-%d"))
print(f"Máximo: {dia_mayor_rango['maximo']:.2f} USD")
print(f"Mínimo: {dia_mayor_rango['minimo']:.2f} USD")
print(f"Rango: {dia_mayor_rango['rango_usd']:.2f} USD")

# Comprobar coincidencias
fecha_subida = dia_mayor_subida["fecha"]
fecha_caida = dia_mayor_caida["fecha"]
fecha_rango = dia_mayor_rango["fecha"]

print("\nCOMPARACIÓN:")

if fecha_subida == fecha_rango:
    print("El día de mayor subida coincide con el día de mayor rango.")
else:
    print("El día de mayor subida NO coincide con el día de mayor rango.")

if fecha_caida == fecha_rango:
    print("El día de mayor caída coincide con el día de mayor rango.")
else:
    print("El día de mayor caída NO coincide con el día de mayor rango.")

# Crear etiquetas
df["fecha_etiqueta"] = df["fecha"].dt.strftime("%m-%d")

# Crear carpeta
os.makedirs("graficas", exist_ok=True)

# Gráfica comparativa del cambio porcentual diario
plt.figure(figsize=(12, 7))

barras = plt.bar(
    df["fecha_etiqueta"],
    df["cambio_pct"]
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title(
    "Cambio porcentual diario de SOLUSD\n"
    "2026-09-25 21:00 UTC - 2026-10-02 20:00 UTC"
)

plt.xlabel("Fecha (UTC)")
plt.ylabel("Cambio diario (%)")

plt.grid(axis="y", alpha=0.3)

# Mostrar porcentajes
for barra, valor in zip(barras, df["cambio_pct"]):
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

ruta = "graficas/actividad_12_comparacion_dias.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nGráfica guardada en:")
print(ruta)

plt.show()