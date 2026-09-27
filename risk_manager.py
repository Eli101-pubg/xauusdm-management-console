import MetaTrader5 as mt5

from config import RISK_PER_TRADE


def calculate_trade_risk(
    entry_price,
    stop_loss,
    lot,
    tick_size,
    tick_value
):
    """
    Calculate the monetary risk of a trade.
    """

    if entry_price <= 0:
        raise ValueError(
            "Invalid entry price."
        )

    if stop_loss <= 0:
        raise ValueError(
            "Invalid stop-loss price."
        )

    if lot <= 0:
        raise ValueError(
            "Invalid lot size."
        )

    if tick_size <= 0:
        raise ValueError(
            "Invalid MT5 tick size."
        )

    if tick_value <= 0:
        raise ValueError(
            "Invalid MT5 tick value."
        )

    price_distance = abs(
        entry_price - stop_loss
    )

    if price_distance <= 0:
        raise ValueError(
            "Entry and stop-loss cannot be the same."
        )

    risk = (
        price_distance / tick_size
    ) * tick_value * lot

    return float(risk)


def validate_risk(
    entry_price,
    stop_loss,
    lot,
    tick_size,
    tick_value
):
    """
    Validate calculated trade risk against
    the permanent $20 risk limit.
    """

    risk = calculate_trade_risk(
        entry_price,
        stop_loss,
        lot,
        tick_size,
        tick_value
    )

    maximum_risk = float(
        RISK_PER_TRADE
    )

    if risk > maximum_risk + 0.01:
        raise ValueError(
            f"RISK LIMIT EXCEEDED: "
            f"${risk:.2f} > "
            f"${maximum_risk:.2f}"
        )

    return risk


def get_candles(
    symbol,
    timeframe,
    count=500
):
    """
    Retrieve candles from MT5.
    """

    rates = mt5.copy_rates_from_pos(
        symbol,
        timeframe,
        0,
        count
    )

    if rates is None or len(rates) == 0:
        raise RuntimeError(
            f"Could not retrieve {symbol} candles: "
            f"{mt5.last_error()}"
        )

    return rates


def get_h12_data(
    symbol,
    count=500
):
    return get_candles(
        symbol,
        mt5.TIMEFRAME_H12,
        count
    )


def get_m15_data(
    symbol,
    count=500
):
    return get_candles(
        symbol,
        mt5.TIMEFRAME_M15,
        count
    )


def get_m5_data(
    symbol,
    count=500
):
    return get_candles(
        symbol,
        mt5.TIMEFRAME_M5,
        count
    )