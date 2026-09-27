import MetaTrader5 as mt5

from config import SYMBOL, MAGIC_NUMBER, DEVIATION


def make_setup_id(setup_key):

    parts = str(setup_key).split("|")

    if len(parts) != 4:
        raise ValueError(
            "Invalid setup key."
        )

    h12_time = parts[0]
    m15_time = parts[1]
    level = parts[2]
    direction = parts[3]

    h12_compact = (
        h12_time.replace("-", "")
        .replace(":", "")
        .replace(" ", "")
    )

    m15_compact = (
        m15_time.replace("-", "")
        .replace(":", "")
        .replace(" ", "")
    )

    level_code = {
        "23.6": "236",
        "38.2": "382",
        "50.0": "500",
        "61.8": "618",
    }.get(level)

    if level_code is None:
        raise ValueError(
            "Invalid Fibonacci entry level."
        )

    direction_code = {
        "BUY": "B",
        "SELL": "S",
    }.get(direction)

    if direction_code is None:
        raise ValueError(
            "Invalid trade direction."
        )

    return (
        "XAU"
        + h12_compact[-8:]
        + m15_compact[-8:]
        + level_code
        + direction_code
    )


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

    if lot <= 0:
        raise ValueError(
            "Invalid lot size."
        )

    if entry_price <= 0:
        raise ValueError(
            "Invalid signal entry price."
        )

    if stop_loss <= 0:
        raise ValueError(
            "Invalid stop-loss."
        )

    if take_profit <= 0:
        raise ValueError(
            "Invalid take-profit."
        )

    # Verify the signal's intended direction
    # against the actual market price.

    if direction == "BUY":

        if stop_loss >= market_price:
            raise ValueError(
                "BUY rejected: stop-loss must "
                "be below actual execution price."
            )

        if take_profit <= market_price:
            raise ValueError(
                "BUY rejected: take-profit must "
                "be above actual execution price."
            )

    else:

        if stop_loss <= market_price:
            raise ValueError(
                "SELL rejected: stop-loss must "
                "be above actual execution price."
            )

        if take_profit >= market_price:
            raise ValueError(
                "SELL rejected: take-profit must "
                "