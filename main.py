import MetaTrader5 as mt5

from config import SYMBOL
from mt5_connection import connect_mt5, disconnect_mt5


def main():
    try:
        account = connect_mt5()

        symbol_info = mt5.symbol_info(SYMBOL)

        if symbol_info is None:
            raise RuntimeError(f"{SYMBOL} was not found in MT5")

        if not symbol_info.visible:
            if not mt5.symbol_select(SYMBOL, True):
                raise RuntimeError(f"Could not select {SYMBOL}")

        print("BOT STARTED")
        print("Symbol:", SYMBOL)
        print("Trading mode: DEMO TESTING")
        print("Automatic execution: NOT ENABLED")

    except Exception as error:
        print("BOT ERROR:", error)

    finally:
        disconnect_mt5()
        print("MT5 DISCONNECTED")


if __name__ == "__main__":
    main()
