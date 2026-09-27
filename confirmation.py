def validate_confirmation(
    direction,
    confirmation_high,
    confirmation_low,
    entry_price
):
    """
    Validate that the confirmation candle actually
    interacted with the intended entry price.

    This module does not create a signal.
    It only validates confirmation data supplied
    by the signal engine.
    """

    if direction not in ("BUY", "SELL"):
        raise ValueError(
            "Invalid confirmation direction."
        )

    if entry_price <= 0:
        raise ValueError(
            "Invalid entry price."
        )

    if confirmation_high <= 0:
        raise ValueError(
            "Invalid confirmation high."
        )

    if confirmation_low <= 0:
        raise ValueError(
            "Invalid confirmation low."
        )

    if confirmation_low > confirmation_high:
        raise ValueError(
            "Confirmation low cannot be above high."
        )

    # The confirmation candle must actually
    # contain/interact with the entry price.
    if not (
        confirmation_low
        <= entry_price
        <= confirmation_high
    ):
        return False

    return True


def confirmation_result(
    direction,
    confirmation_high,
    confirmation_low,
    entry_price
):
    """
    Return a structured confirmation result.
    """

    confirmed = validate_confirmation(
        direction,
        confirmation_high,
        confirmation_low,
        entry_price
    )

    return {
        "confirmed": confirmed,
        "direction": direction,
        "entry_price": float(entry_price),
    }