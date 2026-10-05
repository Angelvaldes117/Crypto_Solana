import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta, timezone

if not mt5.initialize():
    print("Error al conectar con MetaTrader 5")
    print("Error:", mt5.last_error())
    quit()

simbolo = "SOLUSD"

if not mt5.symbol_select(simbolo, True):
    print(f"No se pudo seleccionar {simbolo}")
    mt5.shutdown()
    quit()

# Definir el final del período como el inicio de la hora UTC actual.
# De esta forma evitamos incluir una vela que todavía esté abierta.
ahora_utc = datetime.now(timezone.utc)
fin = ahora_utc.replace(minute=0, second=0, microsecond=0)

# Intervalo solicitado de siete días
inicio = fin - timedelta(days=7)

velas = mt5.copy_rates_range(
    simbolo,
    mt5.TIMEFRAME_H1,
    inicio,
    fin
)

if velas is None or len(velas) == 0:
    print("No se encontraron datos para el período solicitado.")
    print("Error:", mt5.last_error())
    mt5.shutdown()
    quit()

df = pd.DataFrame(velas)

df["time"] = pd.to_datetime(
    df["time"],
    unit="s",
    utc=True
)

# Excluir cualquier vela ubicada exactamente en 'fin',
# ya que podría corresponder a la vela actual.
fin_pd = pd.Timestamp(fin)

df = df[df["time"] < fin_pd].copy()

print("ACTIVIDAD 4 - CONSULTA POR FECHAS")
print("---------------------------------")
print("Símbolo:", simbolo)
print("Temporalidad: H1")

print("\nPERÍODO SOLICITADO")
print("Desde:", inicio.strftime("%Y-%m-%d %H:%M:%S UTC"))
print("Hasta:", fin.strftime("%Y-%m-%d %H:%M:%S UTC"))

print("\nPERÍODO REALMENTE OBTENIDO")
print("Desde:", df["time"].min())
print("Hasta:", df["time"].max())

print("\nCantidad de registros:", len(df))

print("\nPrimeras 5 filas:")
print(df.head())

print("\nÚltimas 5 filas:")
print(df.tail())

# Guardar datos para las siguientes actividades
df.to_csv("datos_solana_7_dias.csv", index=False)

print("\nDatos guardados correctamente en:")
print("datos_solana_7_dias.csv")

mt5.shutdown()