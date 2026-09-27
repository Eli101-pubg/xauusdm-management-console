def check_m5_failure(
    direction,
    entry_price,
    m5_low,
    m5_high,
    stop_loss
):
    """
    Check whether M5 price action has already reached
    the trade's stop-loss level.

    There is NO 15-point adverse-movement threshold.
    """

    if direction not in ("BUY", "SELL"):
        raise ValueError(
            "Direction must be BUY or SELL."
        )

    if entry_price <= 0:
        raise ValueError(
            "Invalid entry price."
        )

    if stop_loss <= 0:
        raise ValueError(
            "Invalid stop-loss."
        )

    if m5_low <= 0 or m5_high <= 0:
        raise ValueError(
            "Invalid M5 prices."
        )

    if m5_low > m5_high:
        raise ValueError(
            "M5 low cannot be above M5 high."
        )

    if direction == "BUY":

        # A BUY is invalid if M5 has already
        # reached or crossed the BUY stop.
        if m5_low <= stop_loss:
            return True

    else:

        # A SELL is invalid if M5 has already
        # reached or crossed the SELL stop.
        if m5_high >= stop_loss:
            return True

    return False