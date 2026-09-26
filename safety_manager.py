from datetime import datetime, timezone


MAX_RISK_USD = 20.0
ALLOWED_SYMBOL = "XAUUSDm"


def validate_symbol(symbol):
    if symbol != ALLOWED_SYMBOL:
        raise ValueError(
            f"Trade rejected: only {ALLOWED_SYMBOL} is allowed."
        )

    return True


def validate_risk(risk):
    if risk <= 0:
        raise ValueError("Trade rejected: invalid risk.")

    if risk > MAX_RISK_USD:
        raise ValueError(
            f"Trade rejected: risk ${risk:.2f} exceeds "
            f"the ${MAX_RISK_USD:.2f} limit."
        )

    return True


def validate_prices(entry, stop_loss, take_profit):
    if entry <= 0 or stop_loss <= 0 or take_profit <= 0:
        raise ValueError("Trade rejected: invalid price.")

    return True


def weekend_block():
    today = datetime.now(timezone.utc).weekday()

    if today >= 5:
        return False

    return True


def approve_trade(
    symbol,
    risk,
    entry,
    stop_loss,
    take_profit
):
    validate_symbol(symbol)
    validate_risk(risk)
    validate_prices(entry, stop_loss, take_profit)

    if not weekend_block():
        raise ValueError(
            "Trade rejected: weekend trading is blocked."
        )

    return True
