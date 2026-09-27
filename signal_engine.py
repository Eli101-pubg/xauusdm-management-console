from strategy import (
    calculate_fibonacci,
    first_touch,
    ENTRY_LEVELS,
)


def build_signal(
    h12_high,
    h12_low,
    confirmation_high,
    confirmation_low
):
    """
    Build a Fibonacci signal from ONE completed H12 candle.

    78.6 is never an entry level.
    """

    fib_levels = calculate_fibonacci(
        h12_high,
        h12_low
    )

    for level_name in ENTRY_LEVELS:

        level_price = fib_levels[level_name]

        touched = first_touch(
            confirmation_high,
            confirmation_low,
            level_price
        )

        if not touched:
            continue

        # Determine direction from the position of the
        # confirmation candle relative to the level.
        if confirmation_low < level_price:
            direction = "BUY"

        elif confirmation_high > level_price:
            direction = "SELL"

        else:
            continue

        return {
            "signal": True,
            "direction": direction,
            "level": level_name,
            "price": level_price,
            "fib_levels": fib_levels,
        }

    return {
        "signal": False,
        "direction": None,
        "level": None,
        "price": None,
        "fib_levels": fib_levels,
    }