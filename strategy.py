FIB_LEVELS = {
    "0.0": 0.000,
    "23.6": 0.236,
    "38.2": 0.382,
    "50.0": 0.500,
    "61.8": 0.618,
    "78.6": 0.786,
    "100.0": 1.000,
}


ENTRY_LEVELS = [
    "0.0",
    "23.6",
    "38.2",
    "50.0",
    "61.8",
    "100.0",
]


TP_ONLY_LEVELS = [
    "78.6",
]


def calculate_fibonacci(high, low):
    """
    Build Fibonacci levels from exactly ONE completed
    H12 candle.
    """

    high = float(high)
    low = float(low)

    price_range = high - low

    if price_range <= 0:
        raise ValueError(
            "Invalid H12 candle range."
        )

    levels = {}

    for name, ratio in FIB_LEVELS.items():
        levels[name] = (
            high - (price_range * ratio)
        )

    return levels


def first_touch(
    candle_high,
    candle_low,
    level
):
    """
    Determine whether the candle touched the
    Fibonacci price.
    """

    return (
        candle_low
        <= level
        <= candle_high
    )


def get_entry_levels(fib_levels):
    """
    Return only levels that are allowed to generate
    entries.

    78.6 is TP-only.
    """

    return {
        name: fib_levels[name]
        for name in ENTRY_LEVELS
    }


def get_tp_level(
    direction,
    entry_level_name,
    fib_levels
):
    """
    TP uses the next Fibonacci target in the
    direction of the trade.

    78.6 is allowed as a TP level only.
    """

    if direction not in ("BUY", "SELL"):
        raise ValueError(
            "Direction must be BUY or SELL."
        )

    if entry_level_name not in ENTRY_LEVELS:
        raise ValueError(
            f"Invalid entry level: "
            f"{entry_level_name}"
        )

    # BUY:
    # TP must be ABOVE the entry.
    if direction == "BUY":

        if entry_level_name == "61.8":
            return fib_levels["78.6"]

        if entry_level_name == "50.0":
            return fib_levels["61.8"]

        if entry_level_name == "38.2":
            return fib_levels["50.0"]

        if entry_level_name == "23.6":
            return fib_levels["38.2"]

        if entry_level_name == "0.0":
            return fib_levels["23.6"]

        if entry_level_name == "100.0":
            raise ValueError(
                "BUY from 100.0 has no higher "
                "Fibonacci target."
            )

    # SELL:
    # TP must be BELOW the entry.
    if direction == "SELL":

        if entry_level_name == "100.0":
            return fib_levels["78.6"]

        if entry_level_name == "78.6":
            raise ValueError(
                "78.6 cannot generate an entry."
            )

        if entry_level_name == "61.8":
            return fib_levels["50.0"]

        if entry_level_name == "50.0":
            return fib_levels["38.2"]

        if entry_level_name == "38.2":
            return fib_levels["23.6"]