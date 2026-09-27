import MetaTrader5 as mt5

from config import SYMBOL, RISK_PER_TRADE
from lot_manager import calculate_lot
from risk_manager import validate_risk
from safety_manager import approve_trade
from order_manager import place_order
from strategy import get_tp_level


MAX_RISK_USD = float(RISK_PER_TRADE)
SL_POINTS = 20000


def calculate_stop_loss(
    direction,
    entry_price,
    point
):

    sl_distance = (
        SL_POINTS * point
    )

    if direction == "BUY":

        return (
            float(entry_price)
            - sl_distance
        )

    if direction == "SELL":

        return (
            float(entry_price)
            + sl_distance
        )

    raise ValueError(
        "Invalid trade direction."
    )


def prepare_trade(
    direction,
    entry_price,
    entry_level_name,
    fib_levels
):

    if direction not in (
        "BUY",
        "SELL"
    ):
        raise ValueError(
            "Invalid trade direction."
        )

    symbol_info = mt5.symbol_info(
        SYMBOL
    )

    if symbol_info is None:
        raise RuntimeError(
            f"{SYMBOL} not found in MT5."
        )

    point = float(
        symbol_info.point
    )

    if point <= 0:
        raise ValueError(
            "Invalid MT5 point size."
        )

    stop_loss = calculate_stop_loss(
        direction,
        entry_price,
        point
    )

    lot = calculate_lot(
        SYMBOL,
        entry_price,
        stop_loss
    )

    tick_size = float(
        symbol_info.trade_tick_size
    )

    tick_value = float(
        symbol_info.trade_tick_value
    )

    risk = validate_risk(
        entry_price,
        stop_loss,
        lot,
        tick_size,
        tick_value
    )

    take_profit = get_tp_level(
        direction,
        entry_level_name,
        fib_levels
    )

    approve_trade(
        SYMBOL,
        direction,
        risk,
        entry_price,
        stop_loss,
        take_profit
    )

    if risk > MAX_RISK_USD + 0.01:

        raise ValueError(
            f"Trade blocked: risk "
            f"${risk:.2f} exceeds "
            f"${MAX_RISK_USD:.2f}."
        )

    return {
        "symbol": SYMBOL,
        "direction": direction,
        "lot": lot,
        "entry": float(entry_price),
        "stop_loss": float(stop_loss),
        "take_profit": float(take_profit),
        "risk": float(risk),
        "entry_level": entry_level_name,
        "sl_points": SL_POINTS,
    }


def execute_trade(
    trade,
    setup