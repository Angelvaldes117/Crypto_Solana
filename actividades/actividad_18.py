import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import os

SIMBOLO = "SOLUSD"

# Mismo período utilizado en las actividades anteriores
INICIO = datetime(2026, 9, 25, 21, 0, tzinfo=timezone.utc)
FIN = datetime(2026, 10, 2, 21, 0, tzinfo=timezone.utc)

# -----------------------------------------
# CONECTAR CON METATRADER 5
# -----------------------------------------

if not mt5.initialize():
    print("Error al iniciar MetaTrader 5:")
    print(mt5.last_error())
    quit()

# Seleccionar SOLUSD
if not mt5.symbol_select(SIMBOLO, True):
    print(f"No se pudo seleccionar {SIMBOLO}")
    mt5.shutdown()
    quit()

# -----------------------------------------
# CONSULTAR H1 Y D1
# -----------------------------------------

datos_h1 = mt5.copy_rates_range(
    SIMBOLO,
    mt5.TIMEFRAME_H1,
    INICIO,
    FIN
)

datos_d1 = mt5.copy_rates_range(
    SIMBOLO,
    mt5.TIMEFRAME_D1,
    INICIO,
    FIN
)

mt5.shutdown()

# -----------------------------------------
# COMPROBAR DATOS
# -----------------------------------------

if datos_h1 is None or len(datos_h1) == 0:
    print("No se obtuvieron datos H1.")
    quit()

if datos_d1 is None or len(datos_d1) == 0:
    print("No se obtuvieron datos D1.")
    quit()

# -----------------------------------------
# DATAFRAMES
# -----------------------------------------

df_h1 = pd.DataFrame(datos_h1)
df_d1 = pd.DataFrame(datos_d1)

df_h1["time"] = pd.to_datetime(
    df_h1["time"],
    unit="s",
    utc=True
)

df_d1["time"] = pd.to_datetime(
    df_d1["time"],
    unit="s",
    utc=True
)

# Copias originales
df_h1_original = df_h1.copy()
df_d1_original = df_d1.copy()

# -----------------------------------------
# COMPROBACIONES
# -----------------------------------------

print("ACTIVIDAD 18 - DOS ESCALAS DE TIEMPO")
print("-------------------------------------")
print(f"Símbolo: {SIMBOLO}")

print("\nPERÍODO SOLICITADO:")
print(f"Desde: {INICIO}")
print(f"Hasta: {FIN}")

print("\nDATOS H1:")
print(f"Registros: {len(df_h1)}")
print(f"Desde: {df_h1['time'].min()}")
print(f"Hasta: {df_h1['time'].max()}")
print(f"Forma: {df_h1.shape}")
print(f"Valores faltantes: {df_h1.isna().sum().sum()}")

print("\nDATOS D1:")
print(f"Registros: {len(df_d1)}")
print(f"Desde: {df_d1['time'].min()}")
print(f"Hasta: {df_d1['time'].max()}")
print(f"Forma: {df_d1.shape}")
print(f"Valores faltantes: {df_d1.isna().sum().sum()}")

# -----------------------------------------
# ESTADÍSTICAS
# -----------------------------------------

rango_h1 = df_h1["high"].max() - df_h1["low"].min()
rango_d1 = df_d1["high"].max() - df_d1["low"].min()

cambio_h1 = (
    (df_h1["close"].iloc[-1] - df_h1["close"].iloc[0])
    / df_h1["close"].iloc[0]
) * 100

cambio_d1 = (
    (df_d1["close"].iloc[-1] - df_d1["close"].iloc[0])
    / df_d1["close"].iloc[0]
) * 100

print("\nCOMPARACIÓN:")

print(f"Cantidad de registros H1: {len(df_h1)}")
print(f"Cantidad de registros D1: {len(df_d1)}")

print(f"\nRango total H1: {rango_h1:.2f} USD")
print(f"Rango total D1: {rango_d1:.2f} USD")

print(f"\nCambio entre primer y último cierre H1: {cambio_h1:.2f}%")
print(f"Cambio entre primer y último cierre D1: {cambio_d1:.2f}%")

# Interpretación automática básica

print("\nTENDENCIA OBSERVADA:")

if cambio_h1 > 0:
    print("H1: aumento entre el primer y último cierre.")
elif cambio_h1 < 0:
    print("H1: disminución entre el primer y último cierre.")
else:
    print("H1: sin cambio entre el primer y último cierre.")

if cambio_d1 > 0:
    print("D1: aumento entre el primer y último cierre.")
elif cambio_d1 < 0:
    print("D1: disminución entre el primer y último cierre.")
else:
    print("D1: sin cambio entre el primer y último cierre.")

print(
    "\nLa escala H1 ofrece mayor detalle sobre las fluctuaciones "
    "dentro de cada día, mientras que D1 resume el comportamiento "
    "general mediante una vela por día."
)

# -----------------------------------------
# GUARDAR DATOS
# -----------------------------------------

df_h1.to_csv(
    "solana_escala_H1.csv",
    index=False
)

df_d1.to_csv(
    "solana_escala_D1.csv",
    index=False
)

os.makedirs("graficas", exist_ok=True)

# -----------------------------------------
# GRÁFICA H1
# -----------------------------------------

plt.figure(figsize=(15, 7))

plt.plot(
    df_h1["time"],
    df_h1["close"],
    marker=".",
    label="Cierre H1"
)

plt.title(
    "SOLUSD - Escala horaria (H1)\n"
    f"{INICIO.strftime('%Y-%m-%d %H:%M')} UTC - "
    f"{FIN.strftime('%Y-%m-%d %H:%M')} UTC"
)

plt.xlabel("Fecha y hora (UTC)")
plt.ylabel("Precio de cierre (USD)")

plt.grid(alpha=0.3)
plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "graficas/actividad_18_escala_H1.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# -----------------------------------------
# GRÁFICA D1
# -----------------------------------------

plt.figure(figsize=(15, 7))

plt.plot(
    df_d1["time"],
    df_d1["close"],
    marker="o",
    label="Cierre D1"
)

# Mostrar precio encima de cada punto
for _, fila in df_d1.iterrows():

    plt.annotate(
        f'{fila["close"]:.2f}',
        (fila["time"], fila["close"]),
        xytext=(0, 10),
        textcoords="offset points",
        ha="center"
    )

plt.title(
    "SOLUSD - Escala diaria (D1)\n"
    f"{INICIO.strftime('%Y-%m-%d %H:%M')} UTC - "
    f"{FIN.strftime('%Y-%m-%d %H:%M')} UTC"
)

plt.xlabel("Fecha (UTC)")
plt.ylabel("Precio de cierre (USD)")

plt.grid(alpha=0.3)
plt.legend()
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "graficas/actividad_18_escala_D1.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nArchivos guardados:")
print("solana_escala_H1.csv")
print("solana_escala_D1.csv")

print("\nGráficas guardadas:")
print("graficas/actividad_18_escala_H1.png")
print("graficas/actividad_18_escala_D1.png")

plt.show()