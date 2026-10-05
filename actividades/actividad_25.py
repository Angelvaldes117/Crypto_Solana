import pandas as pd
import matplotlib.pyplot as plt
import os


print("=" * 70)
print("ACTIVIDAD 25 - HISTOGRAMA DE VARIACIONES HORARIAS")
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
# 2. CALCULAR VARIACIÓN HORARIA
# ==========================================================

df["variacion_pct"] = (
    df["close"].pct_change() * 100
)

variaciones = df["variacion_pct"].dropna()

print("\nVARIACIONES CALCULADAS")
print(
    f"Cantidad de variaciones: {len(variaciones)}"
)


# ==========================================================
# 3. ESTADÍSTICAS
# ==========================================================

media = variaciones.mean()
mediana = variaciones.median()
minimo = variaciones.min()
maximo = variaciones.max()
desviacion = variaciones.std()

positivas = (variaciones > 0).sum()
negativas = (variaciones < 0).sum()
cero = (variaciones == 0).sum()


print("\nESTADÍSTICAS DE LAS VARIACIONES HORARIAS")

print(
    f"Media: {media:+.4f}%"
)

print(
    f"Mediana: {mediana:+.4f}%"
)

print(
    f"Desviación estándar: {desviacion:.4f}%"
)

print(
    f"Mínimo: {minimo:+.4f}%"
)

print(
    f"Máximo: {maximo:+.4f}%"
)


print("\nCLASIFICACIÓN")

print(
    f"Variaciones positivas: {positivas}"
)

print(
    f"Variaciones negativas: {negativas}"
)

print(
    f"Variaciones iguales a cero: {cero}"
)


# ==========================================================
# 4. COMPARAR MEDIA Y MEDIANA
# ==========================================================

print("\nCOMPARACIÓN ENTRE MEDIA Y MEDIANA")

diferencia = media - mediana

print(
    f"Diferencia media - mediana: "
    f"{diferencia:+.4f} puntos porcentuales"
)

if abs(diferencia) < 0.01:

    print(
        "La media y la mediana son muy similares."
    )

elif media > mediana:

    print(
        "La media es mayor que la mediana."
    )

else:

    print(
        "La media es menor que la mediana."
    )


# ==========================================================
# 5. GUARDAR RESULTADOS
# ==========================================================

resultado = df[
    [
        "time",
        "close",
        "variacion_pct"
    ]
].dropna().copy()

resultado.to_csv(
    "variaciones_horarias_solana.csv",
    index=False
)


resumen = pd.DataFrame({
    "Estadística": [
        "Cantidad",
        "Media (%)",
        "Mediana (%)",
        "Desviación estándar (%)",
        "Mínimo (%)",
        "Máximo (%)",
        "Variaciones positivas",
        "Variaciones negativas",
        "Variaciones iguales a cero"
    ],

    "Valor": [
        len(variaciones),
        media,
        mediana,
        desviacion,
        minimo,
        maximo,
        positivas,
        negativas,
        cero
    ]
})

resumen.to_csv(
    "resumen_variaciones_horarias_solana.csv",
    index=False
)

print(
    "\nArchivo guardado: variaciones_horarias_solana.csv"
)

print(
    "Archivo guardado: "
    "resumen_variaciones_horarias_solana.csv"
)


# ==========================================================
# 6. HISTOGRAMA
# ==========================================================

os.makedirs(
    "graficas",
    exist_ok=True
)

ruta_grafica = (
    "graficas/actividad_25_histograma_variaciones.png"
)

plt.figure(
    figsize=(12, 7)
)

plt.hist(
    variaciones,
    bins=20,
    edgecolor="black",
    alpha=0.75
)

plt.axvline(
    media,
    linestyle="--",
    linewidth=2,
    label=f"Media: {media:.4f}%"
)

plt.axvline(
    mediana,
    linestyle=":",
    linewidth=2,
    label=f"Mediana: {mediana:.4f}%"
)

plt.axvline(
    0,
    linewidth=1,
    label="0%"
)

plt.title(
    "SOLUSD - Distribución de las variaciones horarias\n"
    f"{df['time'].min().strftime('%Y-%m-%d %H:%M UTC')} - "
    f"{df['time'].max().strftime('%Y-%m-%d %H:%M UTC')}"
)

plt.xlabel(
    "Variación entre cierres consecutivos (%)"
)

plt.ylabel(
    "Frecuencia"
)

plt.grid(
    axis="y",
    alpha=0.3
)

plt.legend()

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
# 7. INTERPRETACIÓN
# ==========================================================

print("\nINTERPRETACIÓN")

print(
    "El histograma muestra la distribución de los cambios "
    "porcentuales entre cierres horarios consecutivos."
)

print(
    "La mediana representa el valor central de las variaciones "
    "y es menos sensible que la media a movimientos extremos."
)

print(
    "La forma de la distribución corresponde únicamente al "
    "período y al instrumento analizados."
)


print("\n" + "=" * 70)
print("ACTIVIDAD 25 FINALIZADA")
print("=" * 70)