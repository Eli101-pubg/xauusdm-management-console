import time
import MetaTrader5 as mt5

from config import (
    SYMBOL,
    AUTO_EXECUTION,
    DEMO_ONLY,
    LOOP_SECONDS,
)

from mt5_connection import (
    connect_mt5,
    disconnect_mt5,
)

from data_manager import (
    get_completed_h12_candle,
    get_m15_data,
)


def check_mt5_symbol():
    symbol_info = mt5.symbol_info(
        SYMBOL
    )

    if symbol_info is None:
        raise RuntimeError(
            f"{SYMBOL} was not found in MT5."
        )

    if not symbol_info.visible:

        if not mt5.symbol_select(
            SYMBOL,
            True
        ):
            raise RuntimeError(
                f"Could not select {SYMBOL}."
            )

    return symbol_info


def print_bot_status(account):
    print("")
    print("==============================")
    print("XAUUSDm PYTHON BOT")
    print("==============================")
    print("Account:", account.login)
    print("Server:", account.server)
    print("Balance:", account.balance)
    print("Symbol:", SYMBOL)
    print("Automatic execution:", AUTO_EXECUTION)
    print("Demo only:", DEMO_ONLY)
    print("Loop seconds:", LOOP_SECONDS)
    print("==============================")
    print("")


def main():

    account = None

    try:

        account = connect_mt5()

        check_mt5_symbol()

        print_bot_status(account)

        print(
            "BOT RUNNING - "
            "waiting for signal engine..."
        )

        while True:

            # Verify MT5 connection.
            terminal = mt5.terminal_info()

            if terminal is None:
                raise RuntimeError(
                    "MT5 terminal connection lost."
                )

            # Verify the account is still available.
            current_account = mt5.account_info()

            if current_account is None:
                raise RuntimeError(
                    "MT5 account connection lost."
                )

            # Load the latest completed H12 candle.
            h12_candle = (
                get_completed_h12_candle()
            )

            # Load recent M15 data.
            m15_data = get_m15_data(
                10
            )

            print(
                "Monitoring | "
                "H12:",
                h12_candle["time"],
                "| M15 candles:",
                len(m15_data)
            )

            time.sleep(
                LOOP_SECONDS
            )

    except KeyboardInterrupt:

        print(
            "BOT STOPPED BY USER"
        )

    except Exception as error:

        print(
            "BOT ERROR:",
            error
        )

    finally:

        disconnect_mt5()

        print(
            "MT5 DISCONNECTED"
        )


if __name__ == "__main__":
    main()