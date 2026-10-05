import pandas as pd
import os
from datetime import datetime, timezone


print("=" * 70)
print("ACTIVIDAD 20 - REPORTE INICIAL Y COMPROBACIÓN")
print("=" * 70)


# ==========================================================
# 1. CARGAR DATOS
# ==========================================================

archivo_velas = "celery_velas_solana.csv"

if not os.path.exists(archivo_velas):
    raise FileNotFoundError(
        f"No se encontró el archivo {archivo_velas}"
    )

df = pd.read_csv(archivo_velas)

df["time"] = pd.to_datetime(
    df["time"],
    utc=True
)

print("\nDATOS CARGADOS")
print(f"Símbolo: SOLUSD")
print(f"Registros: {len(df)}")
print(f"Columnas: {len(df.columns)}")
print(f"Forma: {df.shape}")
print(f"Valores faltantes: {df.isnull().sum().sum()}")

print(
    f"Período: {df['time'].min()} "
    f"hasta {df['time'].max()}"
)


# ==========================================================
# 2. RESUMEN DIARIO
# ==========================================================

df["fecha"] = df["time"].dt.date

resumen_diario = (
    df.groupby("fecha")
    .agg(
        apertura=("open", "first"),
        maximo=("high", "max"),
        minimo=("low", "min"),
        cierre=("close", "last"),
        volumen_ticks=("tick_volume", "sum"),
        cantidad_velas=("time", "count")
    )
    .reset_index()
)

resumen_diario["variacion_porcentual"] = (
    (
        resumen_diario["cierre"]
        - resumen_diario["apertura"]
    )
    / resumen_diario["apertura"]
) * 100

resumen_diario["rango_usd"] = (
    resumen_diario["maximo"]
    - resumen_diario["minimo"]
)


# ==========================================================
# 3. MAYORES MOVIMIENTOS
# ==========================================================

df["variacion_porcentual"] = (
    df["close"].pct_change() * 100
)

df["variacion_absoluta"] = (
    df["variacion_porcentual"].abs()
)

mayores_movimientos = (
    df.nlargest(
        10,
        "variacion_absoluta"
    )[
        [
            "time",
            "open",
            "high",
            "low",
            "close",
            "tick_volume",
            "variacion_porcentual",
            "variacion_absoluta"
        ]
    ]
    .copy()
)


# ==========================================================
# 4. CALIDAD DE LOS DATOS
# ==========================================================

duplicados = df["time"].duplicated().sum()

nulos = df.isnull().sum().sum()

precios_cero = (
    (df[["open", "high", "low", "close"]] == 0)
    .any(axis=1)
    .sum()
)

indice_esperado = pd.date_range(
    start=df["time"].min(),
    end=df["time"].max(),
    freq="h",
    tz="UTC"
)

fechas_faltantes = indice_esperado.difference(
    pd.DatetimeIndex(df["time"])
)

calidad = pd.DataFrame({
    "Comprobación": [
        "Cantidad de registros",
        "Valores faltantes",
        "Fechas duplicadas",
        "Precios OHLC iguales a cero",
        "Intervalos horarios esperados",
        "Intervalos horarios faltantes"
    ],
    "Resultado": [
        len(df),
        nulos,
        duplicados,
        precios_cero,
        len(indice_esperado),
        len(fechas_faltantes)
    ]
})


# ==========================================================
# 5. METADATOS
# ==========================================================

fecha_generacion = datetime.now(
    timezone.utc
).strftime("%Y-%m-%d %H:%M:%S UTC")

metadatos = pd.DataFrame({
    "Campo": [
        "Instrumento analizado",
        "Descripción",
        "Temporalidad",
        "Período inicial",
        "Período final",
        "Zona horaria",
        "Cantidad de registros",
        "Fuente",
        "Procesamiento",
        "Fecha de generación"
    ],

    "Valor": [
        "SOLUSD",
        "Solana frente al dólar estadounidense",
        "H1",
        str(df["time"].min()),
        str(df["time"].max()),
        "UTC",
        len(df),
        "MetaTrader 5 - TIO Markets Demo",
        "Python, Pandas y Celery",
        fecha_generacion
    ]
})


# ==========================================================
# 6. PREPARAR FECHAS PARA EXCEL
# ==========================================================

df_excel = df.copy()

df_excel["time"] = (
    df_excel["time"]
    .dt.tz_convert("UTC")
    .dt.tz_localize(None)
)

mayores_excel = mayores_movimientos.copy()

mayores_excel["time"] = (
    mayores_excel["time"]
    .dt.tz_convert("UTC")
    .dt.tz_localize(None)
)


# ==========================================================
# 7. CREAR REPORTE EXCEL
# ==========================================================

os.makedirs(
    "reportes",
    exist_ok=True
)

archivo_reporte = (
    "reportes/actividad_20_reporte_inicial.xlsx"
)

with pd.ExcelWriter(
    archivo_reporte,
    engine="openpyxl"
) as writer:

    # El nombre Velas_BTC se conserva porque es el nombre
    # solicitado literalmente en el enunciado.
    # Los metadatos indican que los datos corresponden a SOLUSD.

    df_excel.to_excel(
        writer,
        sheet_name="Velas_BTC",
        index=False
    )

    resumen_diario.to_excel(
        writer,
        sheet_name="Resumen_diario",
        index=False
    )

    mayores_excel.to_excel(
        writer,
        sheet_name="Mayores_movimientos",
        index=False
    )

    calidad.to_excel(
        writer,
        sheet_name="Calidad",
        index=False
    )

    metadatos.to_excel(
        writer,
        sheet_name="Metadatos",
        index=False
    )


print("\nREPORTE GENERADO")
print(f"Archivo: {archivo_reporte}")


# ==========================================================
# 8. VOLVER A LEER EL EXCEL CON PANDAS
# ==========================================================

print("\n" + "=" * 70)
print("COMPROBACIÓN DEL ARCHIVO EXCEL")
print("=" * 70)

excel = pd.ExcelFile(
    archivo_reporte,
    engine="openpyxl"
)

print("\nHojas encontradas:")

for hoja in excel.sheet_names:
    print(f" - {hoja}")


# ==========================================================
# 9. COMPROBAR HOJAS OBLIGATORIAS
# ==========================================================

hojas_esperadas = [
    "Velas_BTC",
    "Resumen_diario",
    "Mayores_movimientos",
    "Calidad",
    "Metadatos"
]

faltantes = [
    hoja
    for hoja in hojas_esperadas
    if hoja not in excel.sheet_names
]

if len(faltantes) == 0:
    print(
        "\nOK - Todas las hojas obligatorias están presentes."
    )
else:
    print(
        "\nERROR - Faltan las siguientes hojas:"
    )

    for hoja in faltantes:
        print(f" - {hoja}")


# ==========================================================
# 10. COMPROBAR CANTIDAD DE REGISTROS
# ==========================================================

print("\nREGISTROS POR HOJA")

for hoja in hojas_esperadas:

    datos_hoja = pd.read_excel(
        archivo_reporte,
        sheet_name=hoja
    )

    print(
        f"{hoja}: {len(datos_hoja)} registros"
    )


velas_verificacion = pd.read_excel(
    archivo_reporte,
    sheet_name="Velas_BTC"
)

print("\nCOMPROBACIÓN DE VELAS")

print(
    f"Registros originales: {len(df)}"
)

print(
    f"Registros recuperados del Excel: "
    f"{len(velas_verificacion)}"
)

if len(df) == len(velas_verificacion):
    print(
        "OK - La cantidad de velas coincide."
    )
else:
    print(
        "ERROR - La cantidad de velas no coincide."
    )


print("\n" + "=" * 70)
print("ACTIVIDAD 20 FINALIZADA")
print("=" * 70)