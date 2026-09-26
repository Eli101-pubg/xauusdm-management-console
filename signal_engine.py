from strategy import calculate_fibonacci, first_touch


ENTRY_LEVELS = [
    "0.0",
    "23.6",
    "38.2",
    "50.0",
    "61.8",
    "100.0",
]


def build_signal(h12_high, h12_low, m15_high, m15_low):
    fib_levels = calculate_fibonacci(
        h12_high,
        h12_low
    )

    for level_name in ENTRY_LEVELS:
        level_price = fib_levels[level_name]

        if first_touch(
            m15_high,
            m15_low,
            level_price
        ):
            return {
                "signal": True,
                "level": level_name,
                "price": level_price,
                "fib_levels": fib_levels
            }

    return {
        "signal": False,
        "level": None,
        "price": None,
        "fib_levels": fib_levels
    }

