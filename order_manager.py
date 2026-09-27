import hashlib

import MetaTrader5 as mt5

from config import (
    SYMBOL,
    MAGIC_NUMBER,
    DEVIATION,
    RISK_PER_TRADE,
    SL_POINTS,
)

from lot_manager import calculate_lot
from risk_manager import validate_risk


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

    point = float(
        symbol_info.point
    )

    if point <= 0:
        raise ValueError(
            "Invalid MT5 point size."
        )

    sl_distance = (
        SL_POINTS * point
    )

    if direction == "BUY":

        execution_price = float(
            tick.ask
        )

        order_type = mt5.ORDER_TYPE_BUY

        actual_stop_loss = (
            execution_price
            - sl_distance
        )

        if take_profit <= execution_price:

            raise ValueError(
                "BUY rejected: take-profit "
                "is no longer above the "
                "actual execution price."
            )

    else:

        execution_price = float(
            tick.bid
        )

        order_type = mt5.ORDER_TYPE_SELL

        actual_stop_loss = (
            execution_price
            + sl_distance
        )

        if take_profit >= execution_price:

            raise ValueError(
                "SELL rejected: take-profit "
                "is no longer below the "
                "actual execution price."
            )

    actual_lot = calculate_lot(
        SYMBOL,
        execution_price,
        actual_stop_loss
    )

    tick_size = float(
        symbol_info.trade_tick_size
    )

    tick_value = float(
        symbol_info.trade_tick_value
    )

    actual_risk = validate_risk(
        execution_price,
        actual_stop_loss,
        actual_lot,
        tick_size,
        tick_value
    )

    if actual_risk > float(
        RISK_PER_TRADE
    ) + 0.01:

        raise ValueError(
            f"Trade blocked: actual risk "
            f"${actual_risk:.2f} exceeds "
            f"${RISK_PER_TRADE:.2f}."
        )

    setup_id = make_setup_id(
        setup_key
    )

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": float(actual_lot),
        "type": order_type,
        "price": execution_price,
        "sl": float(actual_stop_loss),
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
    print("Lot:", actual_lot)
    print("Execution price:", execution_price)
    print("Stop loss:", actual_stop_loss)
    print("Take profit:", take_profit)
    print("SL points:", SL_POINTS)
    print("Risk:", actual_risk)
    print("Setup ID:", setup_id)
    print("Ticket:", result.order)
    print("==============================")

    return result