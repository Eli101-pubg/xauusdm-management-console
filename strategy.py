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
    "23.6",
    "38.2",
    "50.0",
    "61.8",
]

TP_ONLY_LEVELS = [
    "78.6"
]


def calculate_fibonacci(high, low):

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
            low + (
                price_range * ratio
            )
        )

    return levels


def get_entry_levels(fib_levels):

    return {
        name: fib_levels[name]
        for name in ENTRY_LEVELS
    }


def get_tp_level(
    direction,
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

    if entry_level_name not in ENTRY_LEVELS:
        raise ValueError(
            f"{entry_level_name} is not "
            "an allowed entry level."
        )

    level_order = [
        "0.0",
        "23.6",
        "38.2",
        "50.0",
        "61.8",
        "78.6",
        "100.0",
    ]

    entry_index = level_order.index(
        entry_level_name
    )

    if direction == "BUY":

        for level_name in level_order[
            entry_index + 1:
        ]:

            if level_name == "78.6":

                return fib_levels[
                    "78.6"
                ]

        raise ValueError(
            "BUY has no valid higher "
            "Fibonacci TP."
        )

    if direction == "SELL":

        lower_levels = list(
            reversed(
                level_order[
                    :entry_index
                ]
            )
        )

        for level_name in lower_levels:

            return fib_levels[
                level_name
            ]

        raise ValueError(
            "SELL has no valid lower "
            "Fibonacci TP."
        )

    raise ValueError(
        "Could not determine "
        "Fibonacci TP."
    )