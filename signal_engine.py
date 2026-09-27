from strategy import (
    calculate_fibonacci,
    ENTRY_LEVELS,
)


def build_signals(
    h12_high,
    h12_low,
    candle_high,
    candle_low
):
    """
    Build ALL qualifying Fibonacci signals
    from ONE completed H12 candle.

    Multiple touches are allowed.
    78.6 is never an entry level.
    """

    fib_levels = calculate_fibonacci(
        h12_high,
        h12_low
    )

    signals = []

    for level_name in ENTRY_LEVELS:

        level_price = fib_levels[level_name]

        touched = (
            candle_low <= level_price <= candle_high
        )

        if not touched:
            continue

        below_level = candle_low < level_price
        above_level = candle_high > level_price

        if below_level and not above_level:
            direction = "BUY"

        elif above_level and not below_level:
            direction = "SELL"

        else:
            continue

        signals.append({
            "signal": True,
            "direction": direction,
            "level": level_name,
            "price": level_price,
            "fib_levels": fib_levels,
        })

    return signals