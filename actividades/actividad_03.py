import MetaTrader5 as mt5
import pandas as pd

if not mt5.initialize():
    print("Error al conectar con MetaTrader 5")
    print("Error:", mt5.last_error())
    quit()

simbolo = "SOLUSD"

if not mt5.symbol_select(simbolo, True):
    print(f"No se pudo seleccionar {simbolo}")
    mt5.shutdown()
    quit()

# position=1 evita incluir la vela actual que todavía está abierta
velas = mt5.copy_rates_from_pos(
    simbolo,
    mt5.TIMEFRAME_H1,
    1,
    100
)

if velas is None or len(velas) == 0:
    print("No se pudieron obtener datos históricos.")
    print("Error:", mt5.last_error())
    mt5.shutdown()
    quit()

df = pd.DataFrame(velas)

# Convertir timestamp de MetaTrader 5 a fecha/hora UTC
df["time"] = pd.to_datetime(df["time"], unit="s", utc=True)

print("ACTIVIDAD 3 - LECTURA INICIAL DE DATOS HISTÓRICOS")
print("--------------------------------------------------")
print("Símbolo:", simbolo)
print("Temporalidad: H1")
print("Número de velas cerradas:", len(df))

print("\nPeríodo realmente obtenido:")
print("Desde:", df["time"].min())
print("Hasta:", df["time"].max())

print("\nColumnas disponibles:")
print(df.columns.tolist())

print("\nForma del DataFrame:")
print(df.shape)

print("\nTipos de datos:")
print(df.dtypes)

print("\nPRIMERAS 5 FILAS:")
print(df.head())

print("\nÚLTIMAS 5 FILAS:")
print(df.tail())

mt5.shutdown()