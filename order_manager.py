import hashlib

import MetaTrader5 as mt5

from config import (
    SYMBOL,
    MAGIC_NUMBER,
    DEVIATION,
)


def make_setup_id(setup_key):

    if not setup_key:
        raise ValueError(
            "Setup key cannot be empty."
        )

    return hashlib.sha256(
        setup_key.encode("utf-8")
    ).hexdigest()[:16]


def place_order(
    direction,
    lot,
    entry,
    stop_loss,
    take_profit,
    setup_key
):

    if direction not in ("BUY", "SELL"):
        raise ValueError(
            "Invalid trade direction."
        )

    if lot <= 0:
        raise ValueError(
            "Invalid lot size."
        )

    if entry <= 0:
        raise ValueError(
            "Invalid entry price."
        )

    if stop_loss <= 0:
        raise ValueError(
            "Invalid stop-loss."
        )

    if take_profit <= 0:
        raise ValueError(
            "Invalid take-profit."
        )

    if not setup_key:
        raise ValueError(
            "Missing setup key."
        )

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

    tick = mt5.symbol_info_tick(
        SYMBOL
    )

    if tick is None:
        raise RuntimeError(
            f"Could not retrieve {SYMBOL} price."
        )

    if direction == "BUY":

        execution_price = float(
            tick.ask
        )

        order_type = mt5.ORDER_TYPE_BUY

        if stop_loss >= execution_price:
            raise ValueError(
                "BUY rejected: stop-loss "
                "must be below execution price."
            )

        if take_profit <= execution_price:
            raise ValueError(
                "BUY rejected: take-profit "
                "must be above execution price."
            )

    else:

        execution_price = float(
            tick.bid
        )

        order_type = mt5.ORDER_TYPE_SELL

        if stop_loss <= execution_price:
            raise ValueError(
                "SELL rejected: stop-loss "
                "must be above execution price."
            )

        if take_profit >= execution_price:
            raise ValueError(
                "SELL rejected: take-profit "
                "must be below execution price."
            )

    setup_id = make_setup_id(
        setup_key
    )

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": float(lot),
        "type": order_type,
        "price": execution_price,
        "sl": float(stop_loss),
        "tp": float(take_profit),
        "deviation": DEVIATION,
        "magic": MAGIC_NUMBER,
        "comment": setup_id,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(
        request
    )

    if result is None:
        raise RuntimeError(
            f"Order send failed: "
            f"{mt5.last_error()}"
        )

    if result.retcode != mt5.TRADE_RETCODE_DONE:

        raise RuntimeError(
            f"Order rejected by MT5. "
            f"Retcode: {result.retcode}, "
            f"Comment: {result.comment}"
        )

    print("")
    print("==============================")
    print("ORDER EXECUTED")
    print("==============================")
    print("Symbol:", SYMBOL)
    print("Direction:", direction)
    print("Lot:", lot)
    print("Execution price:", execution_price)
    print("Stop loss:", stop_loss)
    print("Take profit:", take_profit)
    print("Setup ID:", setup_id)
    print("Ticket:", result.order)
    print("==============================")

    return result