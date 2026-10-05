import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timezone
import time
import os


print("=" * 70)
print("ACTIVIDAD 27 - OBSERVACIÓN PERIÓDICA DE BID, ASK Y SPREAD")
print("=" * 70)


# ==========================================================
# 1. CONFIGURACIÓN
# ==========================================================

SIMBOLO = "SOLUSD"

NUM_OBSERVACIONES = 10

INTERVALO_SEGUNDOS = 30


print("\nCONFIGURACIÓN")
print(f"Símbolo: {SIMBOLO}")
print(f"Observaciones: {NUM_OBSERVACIONES}")
print(
    f"Intervalo entre observaciones: "
    f"{INTERVALO_SEGUNDOS} segundos"
)

duracion_aproximada = (
    (NUM_OBSERVACIONES - 1)
    * INTERVALO_SEGUNDOS
)

print(
    f"Duración aproximada: "
    f"{duracion_aproximada / 60:.1f} minutos"
)


# ==========================================================
# 2. INICIAR METATRADER 5
# ==========================================================

if not mt5.initialize():

    raise RuntimeError(
        f"No se pudo iniciar MetaTrader 5: "
        f"{mt5.last_error()}"
    )


if not mt5.symbol_select(
    SIMBOLO,
    True
):

    mt5.shutdown()

    raise RuntimeError(
        f"No se pudo seleccionar {SIMBOLO}"
    )


print("\nMetaTrader 5 conectado correctamente.")


# ==========================================================
# 3. REALIZAR OBSERVACIONES
# ==========================================================

observaciones = []

print("\nINICIANDO OBSERVACIONES")
print("-" * 70)


try:

    for numero in range(
        1,
        NUM_OBSERVACIONES + 1
    ):

        tick = mt5.symbol_info_tick(
            SIMBOLO
        )

        if tick is None:

            print(
                f"Observación {numero}: "
                "no se pudo obtener el tick."
            )

        else:

            fecha_utc = datetime.now(
                timezone.utc
            )

            bid = tick.bid
            ask = tick.ask

            spread_usd = (
                ask - bid
            )

            if bid != 0:

                spread_pct = (
                    spread_usd / bid
                ) * 100

            else:

                spread_pct = None

            observaciones.append({
                "numero": numero,
                "fecha_utc": fecha_utc,
                "bid": bid,
                "ask": ask,
                "spread_usd": spread_usd,
                "spread_pct": spread_pct
            })

            print(
                f"Observación {numero:02d} | "
                f"{fecha_utc.strftime('%Y-%m-%d %H:%M:%S UTC')} | "
                f"Bid: {bid:.2f} | "
                f"Ask: {ask:.2f} | "
                f"Spread: {spread_usd:.2f} USD | "
                f"{spread_pct:.4f}%"
            )

        if numero < NUM_OBSERVACIONES:

            time.sleep(
                INTERVALO_SEGUNDOS
            )

finally:

    mt5.shutdown()


# ==========================================================
# 4. CREAR DATAFRAME
# ==========================================================

df = pd.DataFrame(
    observaciones
)

if df.empty:

    raise RuntimeError(
        "No se obtuvo ninguna observación válida."
    )


print("\n" + "=" * 70)
print("RESUMEN DE LA SESIÓN")
print("=" * 70)

print(
    f"Observaciones válidas: {len(df)}"
)

print(
    "Inicio: "
    f"{df['fecha_utc'].min().strftime('%Y-%m-%d %H:%M:%S UTC')}"
)

print(
    "Fin: "
    f"{df['fecha_utc'].max().strftime('%Y-%m-%d %H:%M:%S UTC')}"
)


# ==========================================================
# 5. ESTADÍSTICAS DEL SPREAD
# ==========================================================

spread_promedio = (
    df["spread_usd"].mean()
)

spread_minimo = (
    df["spread_usd"].min()
)

spread_maximo = (
    df["spread_usd"].max()
)

spread_pct_promedio = (
    df["spread_pct"].mean()
)


print("\nESTADÍSTICAS DEL SPREAD")

print(
    f"Spread promedio: "
    f"{spread_promedio:.4f} USD"
)

print(
    f"Spread mínimo: "
    f"{spread_minimo:.4f} USD"
)

print(
    f"Spread máximo: "
    f"{spread_maximo:.4f} USD"
)

print(
    f"Spread porcentual promedio: "
    f"{spread_pct_promedio:.4f}%"
)


# ==========================================================
# 6. VARIACIÓN DEL SPREAD
# ==========================================================

rango_spread = (
    spread_maximo
    - spread_minimo
)

print(
    f"Rango del spread: "
    f"{rango_spread:.4f} USD"
)

if rango_spread == 0:

    print(
        "El spread permaneció constante "
        "durante las observaciones."
    )

else:

    print(
        "El spread presentó variaciones "
        "durante la sesión observada."
    )


# ==========================================================
# 7. GUARDAR CSV
# ==========================================================

archivo_salida = (
    "observaciones_bid_ask_solana.csv"
)

df.to_csv(
    archivo_salida,
    index=False
)

print(
    f"\nArchivo guardado: {archivo_salida}"
)


# ==========================================================
# 8. GRÁFICA BID Y ASK
# ==========================================================

os.makedirs(
    "graficas",
    exist_ok=True
)

ruta_bid_ask = (
    "graficas/actividad_27_bid_ask.png"
)

plt.figure(
    figsize=(12, 6)
)

plt.plot(
    df["fecha_utc"],
    df["bid"],
    marker="o",
    label="Bid"
)

plt.plot(
    df["fecha_utc"],
    df["ask"],
    marker="o",
    label="Ask"
)

plt.title(
    "SOLUSD - Observaciones actuales de Bid y Ask\n"
    f"{df['fecha_utc'].min().strftime('%Y-%m-%d %H:%M:%S UTC')} - "
    f"{df['fecha_utc'].max().strftime('%Y-%m-%d %H:%M:%S UTC')}"
)

plt.xlabel(
    "Fecha y hora (UTC)"
)

plt.ylabel(
    "Precio (USD)"
)

plt.grid(
    alpha=0.3
)

plt.legend()

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    ruta_bid_ask,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ==========================================================
# 9. GRÁFICA DEL SPREAD
# ==========================================================

ruta_spread = (
    "graficas/actividad_27_spread.png"
)

plt.figure(
    figsize=(12, 6)
)

plt.plot(
    df["fecha_utc"],
    df["spread_usd"],
    marker="o"
)

plt.axhline(
    spread_promedio,
    linestyle="--",
    label=(
        f"Promedio: "
        f"{spread_promedio:.4f} USD"
    )
)

plt.title(
    "SOLUSD - Evolución del spread durante la sesión\n"
    f"{df['fecha_utc'].min().strftime('%Y-%m-%d %H:%M:%S UTC')} - "
    f"{df['fecha_utc'].max().strftime('%Y-%m-%d %H:%M:%S UTC')}"
)

plt.xlabel(
    "Fecha y hora (UTC)"
)

plt.ylabel(
    "Spread Ask - Bid (USD)"
)

plt.grid(
    alpha=0.3
)

plt.legend()

plt.xticks(
    rotation=45
)

plt.tight_layout()

plt.savefig(
    ruta_spread,
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print(
    f"Gráfica guardada: {ruta_bid_ask}"
)

print(
    f"Gráfica guardada: {ruta_spread}"
)


# ==========================================================
# 10. INTERPRETACIÓN
# ==========================================================

print("\nINTERPRETACIÓN")

print(
    "Las observaciones fueron obtenidas directamente "
    "de MetaTrader 5 durante la sesión actual."
)

print(
    "El spread se calculó como la diferencia entre "
    "el precio Ask y el precio Bid."
)

print(
    "Estas observaciones son nuevas y no fueron "
    "sustituidas por datos históricos de velas."
)

print(
    "Los valores observados corresponden únicamente "
    "al símbolo SOLUSD y a la fuente utilizada en "
    "MetaTrader 5 durante este período de observación."
)


print("\n" + "=" * 70)
print("ACTIVIDAD 27 FINALIZADA")
print("=" * 70)