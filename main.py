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

from signal_engine import (
    build_signals,
)

from trade_manager import (
    prepare_trade,
    execute_trade,
)


SL_DISTANCE = 10.0


def check_mt5_symbol():

    symbol_info = mt5.symbol_info(SYMBOL)

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
    print("Risk per trade: $20")
    print("SL distance:", SL_DISTANCE)
    print("Loop seconds:", LOOP_SECONDS)
    print("==============================")
    print("")


def process_m15_candle(
    h12_candle,
    m15_candle
):

    h12_high = float(
        h12_candle["high"]
    )

    h12_low = float(
        h12_candle["low"]
    )

    candle_high = float(
        m15_candle["high"]
    )

    candle_low = float(
        m15_candle["low"]
    )

    signals = build_signals(
        h12_high,
        h12_low,
        candle_high,
        candle_low
    )

    print("")
    print(
        "M15:",
        m15_candle["time"],
        "| H12:",
        h12_candle["time"]
    )

    if not signals:

        print(
            "No qualifying Fibonacci signal."
        )

        return

    for signal in signals:

        direction = signal["direction"]

        entry = float(
            signal["price"]
        )

        level = signal["level"]

        fib_levels = signal["fib_levels"]

        if direction == "BUY":

            stop_loss = (
                entry - SL_DISTANCE
            )

        elif direction == "SELL":

            stop_loss = (
                entry + SL_DISTANCE
            )

        else:

            print(
                "Invalid signal direction:",
                direction
            )

            continue

        print("")
        print("==============================")
        print("QUALIFYING SIGNAL")
        print("==============================")
        print("Symbol:", SYMBOL)
        print("Direction:", direction)
        print("Entry level:", level)
        print("Signal entry:", entry)
        print("Stop loss:", stop_loss)

        try:

            trade = prepare_trade(
                direction,
                entry,
                stop_loss,
                level,
                fib_levels
            )

            print(
                "Lot:",
                trade["lot"]
            )

            print(
                "Take profit:",
                trade["take_profit"]
            )

            print(
                "Risk:",
                trade["risk"]
            )

            if not AUTO_EXECUTION:

                print(
                    "AUTO EXECUTION DISABLED - "
                    "signal not sent."
                )

                continue

            result = execute_trade(
                trade
            )

            print(
                "ORDER RESULT:",
                result
            )

        except Exception as trade_error:

            print(
                "TRADE REJECTED:",
                trade_error
            )


def main():

    account = None

    processed_m15 = set()

    try:

        account = connect_mt5()

        check_mt5_symbol()

        print_bot_status(account)

        print(
            "BOT RUNNING - "
            "automatic signal monitoring active"
        )

        while True:

            terminal = mt5.terminal_info()

            if terminal is None:
                raise RuntimeError(
                    "MT5 terminal connection lost."
                )

            current_account = (
                mt5.account_info()
            )

            if current_account is None:
                raise RuntimeError(
                    "MT5 account connection lost."
                )

            h12_candle = (
                get_completed_h12_candle()
            )

            m15_data = get_m15_data(100)

            if m15_data.empty:

                print(
                    "No M15 data available."
                )

                time.sleep(
                    LOOP_SECONDS
                )

                continue

            completed_m15 = (
                m15_data.iloc[:-1]
            )

            for index, m15_candle in (
                completed_m15.iterrows()
            ):

                candle_time = (
                    m15_candle["time"]
                )

                if candle_time in processed_m15:
                    continue

                processed_m15.add(
                    candle_time
                )

                process_m15_candle(
                    h12_candle,
                    m15_candle
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