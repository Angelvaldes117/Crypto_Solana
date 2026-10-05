import MetaTrader5 as mt5
from datetime import datetime, timezone

if not mt5.initialize():
    print("Error al conectar con MetaTrader 5")
    print("Error:", mt5.last_error())
    quit()

simbolo = "SOLUSD"

mt5.symbol_select(simbolo, True)

tick = mt5.symbol_info_tick(simbolo)

if tick is None or tick.time == 0 or tick.bid == 0 or tick.ask == 0:
    print("No hay una cotización válida disponible para SOLUSD.")
else:
    bid = tick.bid
    ask = tick.ask
    diferencia = ask - bid

    hora_utc = datetime.fromtimestamp(
        tick.time,
        tz=timezone.utc
    )

    print("ACTIVIDAD 2 - PRECIO ACTUAL DE SOLANA")
    print("-------------------------------------")
    print("Símbolo:", simbolo)
    print(f"Precio de venta (Bid): {bid:.2f} USD")
    print(f"Precio de compra (Ask): {ask:.2f} USD")
    print(f"Diferencia Ask-Bid: {diferencia:.2f} USD")
    print(
        "Hora de cotización UTC:",
        hora_utc.strftime("%Y-%m-%d %H:%M:%S UTC")
    )

mt5.shutdown()