import math
import MetaTrader5 as mt5

from config import RISK_PER_TRADE


def calculate_lot(symbol, entry_price, stop_loss):
    """
    Calculate the maximum lot size that keeps the trade
    at or below the permanent $20 risk limit.
    """

    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        raise RuntimeError(
            f"Symbol not found: {symbol}"
        )

    risk_amount = float(RISK_PER_TRADE)

    price_distance = abs(
        float(entry_price) - float(stop_loss)
    )

    if price_distance <= 0:
        raise ValueError(
            "Invalid stop-loss distance."
        )

    tick_size = float(
        symbol_info.trade_tick_size
    )

    tick_value = float(
        symbol_info.trade_tick_value
    )

    if tick_size <= 0:
        raise ValueError(
            "Invalid MT5 tick size."
        )

    if tick_value <= 0:
        raise ValueError(
            "Invalid MT5 tick value."
        )

    # Risk for one full lot
    risk_per_lot = (
        price_distance / tick_size
    ) * tick_value

    if risk_per_lot <= 0:
        raise ValueError(
            "Could not calculate risk per lot."
        )

    # Maximum theoretical lot size
    raw_lot = risk_amount / risk_per_lot

    min_lot = float(
        symbol_info.volume_min
    )

    max_lot = float(
        symbol_info.volume_max
    )

    lot_step = float(
        symbol_info.volume_step
    )

    if min_lot <= 0:
        raise ValueError(
            "Invalid broker minimum lot."
        )

    if max_lot <= 0:
        raise ValueError(
            "Invalid broker maximum lot."
        )

    if lot_step <= 0:
        raise ValueError(
            "Invalid broker lot step."
        )

    # Never round upward.
    # Always round DOWN to protect the $20 risk limit.
    lot = (
        math.floor(raw_lot / lot_step)
        * lot_step
    )

    # Normalize floating-point precision
    lot = round(lot, 8)

    # If the broker minimum lot itself would exceed
    # the $20 risk limit, reject the trade.
    if lot < min_lot:
        minimum_lot_risk = (
            risk_per_lot * min_lot
        )

        raise ValueError(
            f"Trade rejected: broker minimum lot "
            f"would risk approximately "
            f"${minimum_lot_risk:.2f}, exceeding "
            f"the ${risk_amount:.2f} limit."
        )

    lot = min(lot, max_lot)

    return lot