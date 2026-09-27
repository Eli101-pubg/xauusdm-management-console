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

from signal_engine import build_signals

from trade_manager import (
    prepare_trade,
    execute_trade,
)

from order_manager import make_setup_id


SL_DISTANCE = 10.0
MAGIC_NUMBER = 260926


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


def setup_exists(setup_id):

    positions = mt5.positions_get(
        symbol=SYMBOL
    )

    if positions is None:
        return False

    for position in positions:

        if position.magic != MAGIC_NUMBER:
            continue

        if position.symbol != SYMBOL:
            continue

        comment = str(
            getattr(
                position,
                "comment",
                ""
            )
        )

        if setup_id in comment:
            return True

    return False


def process_m15_candle(
    h12_candle,
    m15_candle,
    processed_setups
):

    h12_high = float(
        h12_candle["high"]
    )

    h12_low = float(
        h12_candle["low"]
    )

    h12_time = str(
        h12_candle["time"]
    )

    m15_time = str(
        m15_candle["time"]
    )

    candle_open = float(
        m15_candle["open"]
    )

    candle_high = float(
        m15_candle["high"]
    )

    candle_low = float(
        m15_candle["low"]
    )

    candle_close = float(
        m15_candle["close"]
    )

    signals = build_signals(
        h12_high,
        h12_low,
        candle_open,
        candle_high,
        candle_low,
        candle_close
    )

    if not signals:
        return

    for signal in signals:

        direction = signal["direction"]
        level = signal["level"]

        setup_key = (
            f"{h12_time}|"
            f"{m15_time}|"
            f"{level}|"
            f"{direction}"
        )

        setup_id = make_setup_id(
            setup_key
        )

        if setup_id in processed_setups:
            continue

        if setup_exists(setup_id):

            processed_setups.add(
                setup_id
            )

            print(
                "SETUP ALREADY TRADED:",
                setup_id
            )

            continue

        entry = float(
            signal["price"]
        )

        fib_levels = signal[
            "fib_levels"
        ]

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
        print("Setup ID:", setup_id)

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
                trade,
                setup_key
            )

            if result is not None:

                processed_setups.add(
                    setup_id
                )

                print(
                    "SETUP EXECUTED:",
                    setup_id
                )

        except Exception as trade_error:

            print(
                "TRADE REJECTED:",
                trade_error
            )


def main():

    processed_setups = set()

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

            check_mt5_symbol()

            h12_candle = (
                get_completed_h12_candle()
            )

            h12_time = (
                h12_candle["time"]
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

            for _, m15_candle in (
                completed_m15.iterrows()
            ):

                m15_time = (
                    m15_candle["time"]
                )

                if m15_time <= h12_time:
                    continue

                process_m15_candle(
                    h12_candle,
                    m15_candle,
                    processed_setups
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