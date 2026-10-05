import MetaTrader5 as mt5

if not mt5.initialize():
    print("Error al conectar con MetaTrader 5")
    print("Error:", mt5.last_error())
    quit()

simbolo = "SOLUSD"

info = mt5.symbol_info(simbolo)

if info is None:
    print(f"No se encontró el símbolo {simbolo}.")
else:
    print("ACTIVIDAD 1 - IDENTIFICACIÓN DE SOLANA")
    print("--------------------------------------")
    print("Nombre exacto:", info.name)
    print("Descripción:", info.description)
    print("Moneda base:", info.currency_base)
    print("Moneda de cotización:", info.currency_profit)
    print("Categoría:", info.path)

mt5.shutdown()