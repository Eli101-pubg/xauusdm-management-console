FIB_LEVELS = {
    "0.0": 0.000,
    "23.6": 0.236,
    "38.2": 0.382,
    "50.0": 0.500,
    "61.8": 0.618,
    "78.6": 0.786,
    "100.0": 1.000,
}


def calculate_fibonacci(high, low):
    price_range = high - low

    if price_range <= 0:
        raise ValueError("Invalid H12 candle range")

    levels = {}

    for name, ratio in FIB_LEVELS.items():
        levels[name] = high - (price_range * ratio)

    return levels


def first_touch(candle_high, candle_low, level):
    return candle_low <= level <= candle_high


def get_entry_levels(fib_levels):
    return {
        "0.0": fib_levels["0.0"],
        "23.6": fib_levels["23.6"],
        "38.2": fib_levels["38.2"],
        "50.0": fib_levels["50.0"],
        "61.8": fib_levels["61.8"],
        "100.0": fib_levels["100.0"],
    }


def get_tp_level(direction, entry_level_name, fib_levels):
    entry_index = list(FIB_LEVELS.keys()).index(entry_level_name)

    if direction == "BUY":
        for name in list(FIB_LEVELS.keys())[entry_index + 1:]:
            if name != "78.6":
                return fib_levels[name]

        return fib_levels["78.6"]

    if direction == "SELL":
        for name in reversed(list(FIB_LEVELS.keys())[:entry_index]):
            if name != "78.6":
                return fib_levels[name]

        return fib_levels["78.6"]

    raise ValueError("Direction must be BUY or SELL")
