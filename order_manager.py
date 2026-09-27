import MetaTrader5 as mt5

from config import SYMBOL, MAGIC_NUMBER, DEVIATION


def place_order(
    direction,
    lot,
    entry_price,
    stop_loss,
    take_profit,
    setup_key
):

    if direction not in ("BUY", "SELL"):
        raise ValueError(
            "Direction must be BUY or SELL."
        )

    if not setup_key:
        raise ValueError(
            "Missing qualifying setup key."
        )

    symbol_info = mt5.symbol_info(SYMBOL)

    if symbol_info is None:
        raise RuntimeError(
            f"Symbol not found: {SYMBOL}"
        )

    if not symbol_info.visible:

        if not mt5.symbol_select(
            SYMBOL,
            True
        ):
            raise RuntimeError(
                f"Could not select {SYMBOL}"
            )

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        raise RuntimeError(
            f"Could not retrieve current "
            f"{SYMBOL} price: {mt5.last_error()}"
        )

    if direction == "BUY":

        order_type = mt5.ORDER_TYPE_BUY
        market_price = float(tick.ask)

    else:

        order_type = mt5.ORDER_TYPE_SELL
        market_price = float(tick.bid)

    if market_price <= 0:
        raise RuntimeError(
            "Invalid current market price."
        )

    if stop_loss <= 0:
        raise ValueError(
            "Invalid stop-loss."
        )

    if take_profit <= 0:
        raise ValueError(
            "Invalid take-profit."
        )

    if direction == "BUY":

        if stop_loss >= market_price:
            raise ValueError(
                "BUY rejected: stop-loss must "
                "be below current market price."
            )

        if take_profit <= market_price:
            raise ValueError(
                "BUY rejected: take-profit must "
                "be above current market price."
            )

    else:

        if stop_loss <= market_price:
            raise ValueError(
                "SELL rejected: stop-loss must "
                "be above current market price."
            )

        if take_profit >= market_price:
            raise ValueError(
                "SELL rejected: take-profit must "
                "be below current market price."
            )

    comment = (
        "XAUUSDm Fibonacci Bot | "
        + str(setup_key)
    )

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": float(lot),
        "type": order_type,
        "price": market_price,
        "sl": float(stop_loss),
        "tp": float(take_profit),
        "deviation": DEVIATION,
        "magic": MAGIC_NUMBER,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result is None:
        raise RuntimeError(
            f"MT5 order_send failed: "
            f"{mt5.last_error()}"
        )

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise RuntimeError(
            f"Order rejected. "
            f"Retcode: {result.retcode}, "
            f"Comment: {result.comment}"
        )

    print("ORDER EXECUTED")
    print("Symbol:", SYMBOL)
    print("Direction:", direction)
    print("Lot:", lot)
    print("Entry:", market_price)
    print("Stop Loss:", stop_loss)
    print("Take Profit:", take_profit)
    print("Setup:", setup_key)

    return result