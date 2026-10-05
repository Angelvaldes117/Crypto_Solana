import pandas as pd
import matplotlib.pyplot as plt
import os

# Cargar datos
df = pd.read_csv("datos_solana_7_dias.csv")

# Convertir fecha a UTC
df["time"] = pd.to_datetime(df["time"], utc=True)

# Ordenar cronológicamente
df = df.sort_values("time").copy()

# Detectar continuidad horaria
df["diferencia_horas"] = df["time"].diff()

# Calcular cambio porcentual del cierre
df["cambio_pct"] = df["close"].pct_change(fill_method=None) * 100

# No comparar a través de un intervalo faltante
intervalo_normal = pd.Timedelta(hours=1)

df.loc[
    df["diferencia_horas"] != intervalo_normal,
    "cambio_pct"
] = pd.NA

# Seleccionar las 10 mayores subidas
top_10 = (
    df.dropna(subset=["cambio_pct"])
      .nlargest(10, "cambio_pct")
      .copy()
)

top_10["fecha_etiqueta"] = top_10["time"].dt.strftime(
    "%m-%d %H:%M"
)

inicio = df["time"].min()
fin = df["time"].max()

print("ACTIVIDAD 8 - MAYORES SUBIDAS")
print("-----------------------------")
print("Símbolo: SOLUSD")
print("Temporalidad: H1")
print("Registros analizados:", len(df))

print("\nPeríodo analizado:")
print("Desde:", inicio)
print("Hasta:", fin)

print("\n10 HORAS CON MAYOR AUMENTO PORCENTUAL:")

print(
    top_10[
        ["time", "close", "cambio_pct"]
    ].to_string(index=False)
)

# Mayor subida
mayor = top_10.iloc[0]
indice = mayor.name

cierre_actual = df.loc[indice, "close"]
cierre_anterior = df.loc[indice - 1, "close"]

print("\nMAYOR SUBIDA:")
print("Fecha:", mayor["time"])
print(f"Cierre anterior: {cierre_anterior:.2f} USD")
print(f"Cierre actual: {cierre_actual:.2f} USD")
print(f"Aumento: {mayor['cambio_pct']:.2f}%")

# Crear carpeta
os.makedirs("graficas", exist_ok=True)

# Gráfica
plt.figure(figsize=(13, 7))

plt.bar(
    top_10["fecha_etiqueta"],
    top_10["cambio_pct"]
)

plt.title(
    "10 mayores subidas horarias de SOLUSD\n"
    f"{inicio.strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{fin.strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel("Fecha y hora (UTC)")
plt.ylabel("Aumento del cierre respecto a la hora anterior (%)")

plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", alpha=0.3)

for i, valor in enumerate(top_10["cambio_pct"]):
    plt.text(
        i,
        valor,
        f"{valor:.2f}%",
        ha="center",
        va="bottom"
    )

plt.tight_layout()

ruta = "graficas/actividad_08_mayores_subidas.png"

plt.savefig(
    ruta,
    dpi=300,
    bbox_inches="tight"
)

print("\nGráfica guardada en:")
print(ruta)

plt.show()