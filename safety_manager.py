from datetime import datetime, timezone

from config import SYMBOL, RISK_PER_TRADE


MAX_RISK_USD = float(RISK_PER_TRADE)
ALLOWED_SYMBOL = "XAUUSDm"


def validate_symbol(symbol):
    """
    Only XAUUSDm is permitted.
    """

    if symbol != ALLOWED_SYMBOL:
        raise ValueError(
            f"Trade rejected: only "
            f"{ALLOWED_SYMBOL} is allowed."
        )

    return True


def validate_risk(risk):
    """
    Hard maximum-risk protection.
    """

    if risk <= 0:
        raise ValueError(
            "Trade rejected: invalid risk."
        )

    if risk > MAX_RISK_USD + 0.01:
        raise ValueError(
            f"Trade rejected: calculated risk "
            f"${risk:.2f} exceeds the "
            f"${MAX_RISK_USD:.2f} maximum."
        )

    return True


def validate_prices(
    direction,
    entry,
    stop_loss,
    take_profit
):
    """
    Validate that SL and TP are on the correct
    side of the entry.
    """

    if entry <= 0:
        raise ValueError(
            "Trade rejected: invalid entry price."
        )

    if stop_loss <= 0:
        raise ValueError(
            "Trade rejected: invalid stop-loss."
        )

    if take_profit <= 0:
        raise ValueError(
            "Trade rejected: invalid take-profit."
        )

    if direction == "BUY":

        if stop_loss >= entry:
            raise ValueError(
                "BUY rejected: stop-loss must "
                "be below entry."
            )

        if take_profit <= entry:
            raise ValueError(
                "BUY rejected: take-profit must "
                "be above entry."
            )

    elif direction == "SELL":

        if stop_loss <= entry:
            raise ValueError(
                "SELL rejected: stop-loss must "
                "be above entry."
            )

        if take_profit >= entry:
            raise ValueError(
                "SELL rejected: take-profit must "
                "be below entry."
            )

    else:
        raise ValueError(
            "Trade rejected: invalid direction."
        )

    return True


def weekend_block():
    """
    No trading on Saturday or Sunday.
    """

    weekday = datetime.now(
        timezone.utc
    ).weekday()

    if weekday >= 5:
        return False

    return True


def approve_trade(
    symbol,
    direction,
    risk,
    entry,
    stop_loss,
    take_profit
):
    """
    Final safety gate before an order can be sent.
    """

    validate_symbol(symbol)

    validate_risk(risk)

    validate_prices(
        direction,
        entry,
        stop_loss,
        take_profit
    )

    if not weekend_block():
        raise ValueError(
            "Trade rejected: weekend trading "
            "is blocked."
        )

    return True