import MetaTrader5 as mt5
import pandas as pd

from config import SYMBOL


def get_candles(timeframe, count=500):

    rates = mt5.copy_rates_from_pos(
        SYMBOL,
        timeframe,
        0,
        count
    )

    if rates is None or len(rates) == 0:
        raise RuntimeError(
            f"Could not retrieve {SYMBOL} candles: "
            f"{mt5.last_error()}"
        )

    df = pd.DataFrame(rates)

    df["time"] = pd.to_datetime(
        df["time"],
        unit="s",
        utc=True
    )

    return df


def get_completed_h12_candle():

    df = get_candles(
        mt5.TIMEFRAME_H12,
        3
    )

    if len(df) < 2:
        raise RuntimeError(
            "Not enough H12 candles available."
        )

    return df.iloc[-2].copy()


def get_h12_data(count=500):

    return get_candles(
        mt5.TIMEFRAME_H12,
        count
    )


def get_m15_data(count=500):

    return get_candles(
        mt5.TIMEFRAME_M15,
        count
    )


def get_m5_data(count=500):

    return get_candles(
        mt5.TIMEFRAME_M5,
        count
    )