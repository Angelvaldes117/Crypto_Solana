import pandas as pd
import matplotlib.pyplot as plt
import os


print("=" * 70)
print("ACTIVIDAD 24 - RECUPERACIÓN DESPUÉS DE LAS 5 MAYORES CAÍDAS")
print("=" * 70)


# ==========================================================
# 1. CARGAR DATOS
# ==========================================================

archivo = "celery_velas_solana.csv"

if not os.path.exists(archivo):
    raise FileNotFoundError(
        f"No se encontró el archivo {archivo}"
    )

df = pd.read_csv(archivo)

df["time"] = pd.to_datetime(
    df["time"],
    utc=True
)

print("\nDATOS CARGADOS")
print("Símbolo: SOLUSD")
print(f"Registros: {len(df)}")
print(f"Forma: {df.shape}")
print(f"Valores faltantes: {df.isnull().sum().sum()}")

print(
    f"Período: {df['time'].min()} "
    f"hasta {df['time'].max()}"
)


# ==========================================================
# 2. CALCULAR CAMBIO HORARIO
# ==========================================================

df["variacion_pct"] = (
    df["close"].pct_change() * 100
)

caidas = (
    df[df["variacion_pct"] < 0]
    .nsmallest(
        5,
        "variacion_pct"
    )
    .copy()
)

print("\n5 MAYORES CAÍDAS HORARIAS")

for numero, (indice, fila) in enumerate(
    caidas.iterrows(),
    start=1
):
    print(
        f"{numero}. "
        f"{fila['time'].strftime('%Y-%m-%d %H:%M UTC')} | "
        f"Cierre: {fila['close']:.2f} USD | "
        f"Caída: {fila['variacion_pct']:.2f}%"
    )


# ==========================================================
# 3. CALCULAR RECUPERACIÓN
# ==========================================================

resultados = []

for numero, (indice, fila) in enumerate(
    caidas.iterrows(),
    start=1
):

    precio_caida = fila["close"]

    registro = {
        "numero": numero,
        "fecha_caida": fila["time"],
        "precio_caida": precio_caida,
        "caida_pct": fila["variacion_pct"]
    }

    for horas in [1, 6, 24]:

        indice_futuro = indice + horas

        if indice_futuro < len(df):

            precio_futuro = df.loc[
                indice_futuro,
                "close"
            ]

            fecha_futura = df.loc[
                indice_futuro,
                "time"
            ]

            recuperacion = (
                (
                    precio_futuro
                    - precio_caida
                )
                / precio_caida
            ) * 100

            registro[f"precio_{horas}h"] = (
                precio_futuro
            )

            registro[f"fecha_{horas}h"] = (
                fecha_futura
            )

            registro[f"recuperacion_{horas}h_pct"] = (
                recuperacion
            )

        else:

            registro[f"precio_{horas}h"] = None
            registro[f"fecha_{horas}h"] = None
            registro[f"recuperacion_{horas}h_pct"] = None

    resultados.append(registro)


resultado = pd.DataFrame(resultados)


# ==========================================================
# 4. MOSTRAR RESULTADOS
# ==========================================================

print("\nRECUPERACIÓN POSTERIOR")

for _, fila in resultado.iterrows():

    print("\n" + "-" * 60)

    print(
        f"Caída #{int(fila['numero'])}"
    )

    print(
        "Fecha: "
        f"{fila['fecha_caida'].strftime('%Y-%m-%d %H:%M UTC')}"
    )

    print(
        f"Caída original: "
        f"{fila['caida_pct']:.2f}%"
    )

    print(
        f"Precio después de la caída: "
        f"{fila['precio_caida']:.2f} USD"
    )

    for horas in [1, 6, 24]:

        recuperacion = fila[
            f"recuperacion_{horas}h_pct"
        ]

        if pd.notna(recuperacion):

            print(
                f"{horas}h después: "
                f"{recuperacion:+.2f}%"
            )

        else:

            print(
                f"{horas}h después: "
                "sin datos suficientes"
            )


# ==========================================================
# 5. PROMEDIOS
# ==========================================================

print("\n" + "=" * 70)
print("PROMEDIO DESPUÉS DE LAS 5 MAYORES CAÍDAS")
print("=" * 70)

promedios = {}

for horas in [1, 6, 24]:

    columna = (
        f"recuperacion_{horas}h_pct"
    )

    promedio = resultado[
        columna
    ].mean()

    promedios[horas] = promedio

    disponibles = resultado[
        columna
    ].notna().sum()

    print(
        f"{horas}h después: "
        f"{promedio:+.2f}% "
        f"({disponibles} casos disponibles)"
    )


# ==========================================================
# 6. CONTAR RECUPERACIONES POSITIVAS
# ==========================================================

print("\nCASOS CON RECUPERACIÓN POSITIVA")

for horas in [1, 6, 24]:

    columna = (
        f"recuperacion_{horas}h_pct"
    )

    disponibles = resultado[
        columna
    ].notna().sum()

    positivos = (
        resultado[columna] > 0
    ).sum()

    print(
        f"{horas}h: "
        f"{positivos} de {disponibles}"
    )


# ==========================================================
# 7. GUARDAR CSV
# ==========================================================

archivo_salida = (
    "recuperacion_mayores_caidas_solana.csv"
)

resultado.to_csv(
    archivo_salida,
    index=False
)

print(
    f"\nArchivo guardado: {archivo_salida}"
)


# ==========================================================
# 8. GRÁFICA
# ==========================================================

os.makedirs(
    "graficas",
    exist_ok=True
)

ruta_grafica = (
    "graficas/actividad_24_recuperacion_caidas.png"
)

etiquetas = [
    "1 hora",
    "6 horas",
    "24 horas"
]

valores = [
    promedios[1],
    promedios[6],
    promedios[24]
]

plt.figure(
    figsize=(10, 6)
)

plt.bar(
    etiquetas,
    valores
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title(
    "SOLUSD - Variación promedio después de las 5 mayores caídas\n"
    f"{df['time'].min().strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{df['time'].max().strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel(
    "Tiempo después de la caída"
)

plt.ylabel(
    "Variación respecto al cierre de la caída (%)"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.tight_layout()

plt.savefig(
    ruta_grafica,
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print(
    f"Gráfica guardada: {ruta_grafica}"
)


# ==========================================================
# 9. INTERPRETACIÓN
# ==========================================================

print("\nINTERPRETACIÓN")

print(
    "Los porcentajes comparan el cierre posterior con el cierre "
    "de la vela en la que ocurrió cada una de las cinco mayores caídas."
)

print(
    "Un resultado positivo indica que el precio estaba por encima "
    "del cierre de la caída en ese horizonte; un resultado negativo "
    "indica que se encontraba por debajo."
)

print(
    "Los resultados describen únicamente el período analizado "
    "y no implican que una caída provoque una recuperación posterior."
)


print("\n" + "=" * 70)
print("ACTIVIDAD 24 FINALIZADA")
print("=" * 70)