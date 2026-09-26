import MetaTrader5 as mt5


def calculate_lot(symbol, entry_price, stop_loss):
    symbol_info = mt5.symbol_info(symbol)

    if symbol_info is None:
        raise RuntimeError(f"Symbol not found: {symbol}")

    risk_amount = 20.0

    price_distance = abs(entry_price - stop_loss)

    if price_distance <= 0:
        raise ValueError("Invalid stop-loss distance")

    tick_size = symbol_info.trade_tick_size
    tick_value = symbol_info.trade_tick_value

    if tick_size <= 0 or tick_value <= 0:
        raise ValueError("Invalid MT5 tick information")

    risk_per_lot = (price_distance / tick_size) * tick_value

    lot = risk_amount / risk_per_lot

    min_lot = symbol_info.volume_min
    max_lot = symbol_info.volume_max
    lot_step = symbol_info.volume_step

    lot = max(min_lot, min(lot, max_lot))

    lot = round(lot / lot_step) * lot_step

    return lot
