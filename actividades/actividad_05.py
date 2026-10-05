import pandas as pd

archivo = "datos_solana_7_dias.csv"

df = pd.read_csv(archivo)

# Convertir la columna time nuevamente a fecha UTC
df["time"] = pd.to_datetime(df["time"], utc=True)

print("ACTIVIDAD 5 - CALIDAD DE LOS DATOS")
print("----------------------------------")

print("\nCantidad de registros:", len(df))
print("Cantidad de columnas:", len(df.columns))

# 1. VALORES VACÍOS
print("\n1. VALORES VACÍOS")
nulos = df.isnull().sum()
print(nulos)

total_nulos = nulos.sum()

print("\nTotal de valores vacíos:", total_nulos)

# 2. FECHAS DUPLICADAS
print("\n2. FECHAS DUPLICADAS")

duplicados = df["time"].duplicated().sum()

print("Cantidad de fechas duplicadas:", duplicados)

if duplicados > 0:
    print("\nRegistros duplicados:")
    print(df[df["time"].duplicated(keep=False)])
else:
    print("No se encontraron fechas duplicadas.")

# 3. INTERVALOS HORARIOS SIN REGISTROS
print("\n3. INTERVALOS HORARIOS SIN REGISTROS")

inicio = df["time"].min()
fin = df["time"].max()

horas_esperadas = pd.date_range(
    start=inicio,
    end=fin,
    freq="h",
    tz="UTC"
)

horas_faltantes = horas_esperadas.difference(df["time"])

print("Primera vela:", inicio)
print("Última vela:", fin)

print("Horas esperadas entre ambas:", len(horas_esperadas))
print("Horas realmente obtenidas:", len(df))
print("Intervalos faltantes:", len(horas_faltantes))

if len(horas_faltantes) > 0:
    print("\nHoras sin registros:")

    for hora in horas_faltantes:
        print(hora)
else:
    print("No existen intervalos horarios faltantes.")

# 4. COMPROBACIÓN DE PRECIOS
print("\n4. COMPROBACIÓN DE PRECIOS")

columnas_precio = ["open", "high", "low", "close"]

precios_cero = (df[columnas_precio] == 0).sum()

print("Valores iguales a cero:")
print(precios_cero)

# 5. RESUMEN
print("\nRESUMEN DE CALIDAD")
print("------------------")
print("Registros analizados:", len(df))
print("Valores vacíos:", total_nulos)
print("Fechas duplicadas:", duplicados)
print("Intervalos horarios faltantes:", len(horas_faltantes))
print("Precios iguales a cero:", precios_cero.sum())