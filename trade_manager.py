import MetaTrader5 as mt5

from config import SYMBOL
from lot_manager import calculate_lot
from risk_manager import validate_risk
from safety_manager import approve_trade
from order_manager import place_order
from strategy import get_tp_level


MAX_RISK_USD = 20.0


def prepare_trade(
    direction,
    entry_price,
    stop_loss,
    entry_level_name,
    fib_levels
):
    if direction not in ("BUY", "SELL"):
        raise ValueError("Invalid trade direction")

    symbol_info = mt5.symbol_info(SYMBOL)

    if symbol_info is None:
        raise RuntimeError(f"{SYMBOL} not found")

    lot = calculate_lot(
        SYMBOL,
        entry_price,
        stop_loss
    )

    tick_size = symbol_info.trade_tick_size
    tick_value = symbol_info.trade_tick_value

    validate_risk(
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

    risk = (
        abs(entry_price - stop_loss)
        / tick_size
    ) * tick_value * lot

    approve_trade(
        SYMBOL,
        risk,
        entry_price,
        stop_loss,
        take_profit
    )

    return {
        "symbol": SYMBOL,
        "direction": direction,
        "lot": lot,
        "entry": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "risk": risk
    }


def execute_trade(trade):
    return place_order(
        trade["direction"],
        trade["lot"],
        trade["entry"],
        trade["stop_loss"],
        trade["take_profit"]
    )
