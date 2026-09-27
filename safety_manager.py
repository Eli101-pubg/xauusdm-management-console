from datetime import datetime, timezone

import MetaTrader5 as mt5

from config import SYMBOL, RISK_PER_TRADE


MAX_RISK_USD = float(RISK_PER_TRADE)
ALLOWED_SYMBOL = "XAUUSDm"
MAX_CONSECUTIVE_LOSSES = 3
MAGIC_NUMBER = 260926


def validate_symbol(symbol):

    if symbol != ALLOWED_SYMBOL:
        raise ValueError(
            f"Trade rejected: only "
            f"{ALLOWED_SYMBOL} is allowed."
        )

    return True


def validate_risk(risk):

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

    weekday = datetime.now(
        timezone.utc
    ).weekday()

    if weekday >= 5:
        return False

    return True


def get_consecutive_losses():

    now = datetime.now(
        timezone.utc
    )

    history = mt5.history_deals_get(
        datetime(
            2020,
            1,
            1,
            tzinfo=timezone.utc
        ),
        now
    )

    if history is None:
        return 0

    closed_deals = []

    for deal in history:

        if deal.symbol != ALLOWED_SYMBOL:
            continue

        if deal.magic != MAGIC_NUMBER:
            continue

        if deal.entry != mt5.DEAL_ENTRY_OUT:
            continue

        profit = (
            float(deal.profit)
            + float(deal.swap)
            + float(deal.commission)
        )

        closed_deals.append(
            (
                int(deal.time),
                profit
            )
        )

    closed_deals.sort(
        key=lambda item: item[0],
        reverse=True
    )

    consecutive_losses = 0

    for _, profit in closed_deals:

        if profit < 0:
            consecutive_losses += 1

        else:
            break

    return consecutive_losses


def validate_consecutive_losses():

    losses = get_consecutive_losses()

    if losses >= MAX_CONSECUTIVE_LOSSES:
        raise ValueError(
            f"Trade rejected: "
            f"{losses} consecutive losses reached "
            f"the maximum of "
            f"{MAX_CONSECUTIVE_LOSSES}."
        )

    return True


def approve_trade(
    symbol,
    direction,
    risk,
    entry,
    stop_loss,
    take_profit
):

    validate_symbol(symbol)

    validate_risk(risk)

    validate_prices(
        direction,
        entry,
        stop_loss,
        take_profit
    )

    validate_consecutive_losses()

    if not weekend_block():
        raise ValueError(
            "Trade rejected: weekend trading "
            "is blocked."
        )

    return True