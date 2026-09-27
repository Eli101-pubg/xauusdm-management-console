from strategy import (
    calculate_fibonacci,
    ENTRY_LEVELS,
)


def build_signals(
    h12_high,
    h12_low,
    candle_open,
    candle_high,
    candle_low,
    candle_close
):
    """
    Build ALL qualifying Fibonacci signals
    from ONE completed H12 candle.

    Multiple touches are allowed.
    78.6 is never an entry level.

    BUY:
        M15 candle starts above the Fibonacci level
        and touches/crosses down to it.

    SELL:
        M15 candle starts below the Fibonacci level
        and touches/crosses up to it.

    Candles that cross the level from both sides
    without a clear starting direction are rejected.
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

        if candle_open > level_price:

            direction = "BUY"

        elif candle_open < level_price:

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