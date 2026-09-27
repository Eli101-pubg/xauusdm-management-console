import MetaTrader5 as mt5

from config import (
    FIXED_RISK_USD,
    COMPOUNDING_RISK_PERCENT,
    COMPOUNDING_TRIGGER_PROFIT_PERCENT,
    STARTING_BALANCE,
)


def get_active_risk(account_balance):
    """
    Determine the active risk model.

    Stage 1:
    Fixed $20 risk.

    Stage 2:
    10% of current balance after the account
    exceeds 200% profit from the starting balance.
    """

    account_balance = float(account_balance)

    if account_balance <= 0:
        raise ValueError(
            "Invalid account balance."
        )

    if STARTING_BALANCE <= 0:
        raise ValueError(
            "STARTING_BALANCE must be configured "
            "in the local .env file."
        )

    profit_percent = (
        (
            account_balance - STARTING_BALANCE
        )
        / STARTING_BALANCE
    ) * 100.0

    trigger_reached = (
        profit_percent
        > COMPOUNDING_TRIGGER_PROFIT_PERCENT
    )

    if trigger_reached:

        risk_amount = (
            account_balance
            * COMPOUNDING_RISK_PERCENT
            / 100.0
        )

        return {
            "risk_amount": float(risk_amount),
            "risk_percent": float(
                COMPOUNDING_RISK_PERCENT
            ),
            "profit_percent": float(
                profit_percent
            ),
            "mode": "10_PERCENT_COMPOUNDING",
        }

    return {
        "risk_amount": float(FIXED_RISK_USD),
        "risk_percent": None,
        "profit_percent": float(
            profit_percent
        ),
        "mode": "FIXED_20_USD",
    }


def calculate_trade_risk(
    entry_price,
    stop_loss,
    lot,
    tick_size,
    tick_value
):
    """
    Calculate the monetary risk of a trade.
    """

    if entry_price <= 0:
        raise ValueError(
            "Invalid entry price."
        )

    if stop_loss <= 0:
        raise ValueError(
            "Invalid stop-loss price."
        )

    if lot <= 0:
        raise ValueError(
            "Invalid lot size."
        )

    if tick_size <= 0:
        raise ValueError(
            "Invalid MT5 tick size."
        )

    if tick_value <= 0:
        raise ValueError(
            "Invalid MT5 tick value."
        )

    price_distance = abs(
        entry_price - stop_loss
    )

    if price_distance <= 0:
        raise ValueError(
            "Entry and stop-loss cannot be the same."
        )

    risk = (
        price_distance / tick_size
    ) * tick_value * lot

    return float(risk)


def validate_risk(
    entry_price,
    stop_loss,
    lot,
    tick_size,
    tick_value,
    account_balance
):
    """
    Validate the calculated trade risk against
    the currently active risk model.
    """

    risk = calculate_trade_risk(
        entry_price,
        stop_loss,
        lot,
        tick_size,
        tick_value
    )

    active_risk = get_active_risk(
        account_balance
    )

    maximum_risk = float(
        active_risk["risk_amount"]
    )

    if risk > maximum_risk + 0.01:
        raise ValueError(
            f"RISK LIMIT EXCEEDED: "
            f"${risk:.2f} > "
            f"${maximum_risk:.2f}"
        )

    return risk


def get_candles(
    symbol,
    timeframe,
    count=500
):
    """
    Retrieve candles from MT5.
    """

    rates = mt5.copy_rates_from_pos(
        symbol,
        timeframe,
        0,
        count
    )

    if rates is None or len(rates) == 0:
        raise RuntimeError(
            f"Could not retrieve {symbol} candles: "
            f"{mt5.last_error()}"
        )

    return rates


def get_h12_data(
    symbol,
    count=500
):
    return get_candles(
        symbol,
        mt5.TIMEFRAME_H12,
        count
    )


def get_m15_data(
    symbol,
    count=500
):
    return get_candles(
        symbol,
        mt5.TIMEFRAME_M15,
        count
    )


def get_m5_data(
    symbol,
    count=500
):
    return get_candles(
        symbol,
        mt5.TIMEFRAME_M5,
        count
    )