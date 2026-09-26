import MetaTrader5 as mt5

from config import SYMBOL, MAGIC_NUMBER, DEVIATION


def place_order(direction, lot, entry_price, stop_loss, take_profit):
    if direction not in ("BUY", "SELL"):
        raise ValueError("Direction must be BUY or SELL")

    symbol_info = mt5.symbol_info(SYMBOL)

    if symbol_info is None:
        raise RuntimeError(f"Symbol not found: {SYMBOL}")

    if not symbol_info.visible:
        if not mt5.symbol_select(SYMBOL, True):
            raise RuntimeError(f"Could not select {SYMBOL}")

    if direction == "BUY":
        order_type = mt5.ORDER_TYPE_BUY
    else:
        order_type = mt5.ORDER_TYPE_SELL

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": float(lot),
        "type": order_type,
        "price": float(entry_price),
        "sl": float(stop_loss),
        "tp": float(take_profit),
        "deviation": DEVIATION,
        "magic": MAGIC_NUMBER,
        "comment": "XAUUSDm Fibonacci Bot",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result is None:
        raise RuntimeError(f"MT5 order_send failed: {mt5.last_error()}")

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        raise RuntimeError(
            f"Order rejected. Retcode: {result.retcode}, "
            f"Comment: {result.comment}"
        )

    return result
