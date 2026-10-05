import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Cargar datos
df = pd.read_csv("datos_solana_7_dias.csv")

# Convertir fecha a UTC
df["time"] = pd.to_datetime(df["time"], utc=True)

inicio = df["time"].min()
fin = df["time"].max()

# Clasificar cada vela
condiciones = [
    df["close"] > df["open"],
    df["close"] < df["open"]
]

categorias = [
    "Alcista",
    "Bajista"
]

df["tipo_vela"] = np.select(
    condiciones,
    categorias,
    default="Sin cambio"
)

# Orden deseado
orden = ["Alcista", "Bajista", "Sin cambio"]

# Cantidades
cantidades = (
    df["tipo_vela"]
    .value_counts()
    .reindex(orden, fill_value=0)
)

# Proporciones
proporciones = cantidades / len(df) * 100

# Crear tabla resumen
resumen = pd.DataFrame({
    "Cantidad": cantidades,
    "Proporcion_pct": proporciones
})

print("ACTIVIDAD 10 - VELAS ALCISTAS Y BAJISTAS")
print("-----------------------------------------")
print("Símbolo: SOLUSD")
print("Temporalidad: H1")
print("Registros analizados:", len(df))

print("\nPeríodo analizado:")
print("Desde:", inicio)
print("Hasta:", fin)

print("\nRESUMEN:")
print(resumen)

print("\nCOMPROBACIÓN:")
print("Total clasificado:", cantidades.sum())
print("Total de registros:", len(df))
print(f"Suma de proporciones: {proporciones.sum():.2f}%")

# Crear carpeta
os.makedirs("graficas", exist_ok=True)

# Gráfica
plt.figure(figsize=(10, 7))

barras = plt.bar(
    resumen.index,
    resumen["Cantidad"]
)

plt.title(
    "Clasificación de velas horarias de SOLUSD\n"
    f"{inicio.strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{fin.strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel("Tipo de vela")
plt.ylabel("Cantidad de velas")
plt.grid(axis="y", alpha=0.3)

# Mostrar cantidad y porcentaje encima de cada barra
for barra, cantidad, porcentaje in zip(
    barras,
    resumen["Cantidad"],
    resumen["Proporcion_pct"]
):
    plt.text(
        barra.get_x() + barra.get_width() / 2,
        barra.get_height(),
        f"{cantidad}\n({porcentaje:.2f}%)",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

ruta = "graficas/actividad_10_velas_alcistas_bajistas.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nGráfica guardada en:")
print(ruta)

plt.show()