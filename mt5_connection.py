import MetaTrader5 as mt5

from config import (
    MT5_LOGIN,
    MT5_PASSWORD,
    MT5_SERVER,
    SYMBOL,
)


def connect_mt5():

    if not MT5_LOGIN:

        raise RuntimeError(
            "MT5_LOGIN is not configured."
        )

    if not MT5_PASSWORD:

        raise RuntimeError(
            "MT5_PASSWORD is not configured."
        )

    if not MT5_SERVER:

        raise RuntimeError(
            "MT5_SERVER is not configured."
        )

    if not mt5.initialize():

        raise RuntimeError(
            f"MT5 initialization failed: "
            f"{mt5.last_error()}"
        )

    authorized = mt5.login(
        login=MT5_LOGIN,
        password=MT5_PASSWORD,
        server=MT5_SERVER
    )

    if not authorized:

        error = mt5.last_error()

        mt5.shutdown()

        raise RuntimeError(
            f"MT5 login failed: {error}"
        )

    account = mt5.account_info()

    if account is None:

        mt5.shutdown()

        raise RuntimeError(
            "Could not retrieve MT5 "
            "account information."
        )

    symbol_info = mt5.symbol_info(
        SYMBOL
    )

    if symbol_info is None:

        mt5.shutdown()

        raise RuntimeError(
            f"{SYMBOL} was not found in MT5."
        )

    if not symbol_info.visible:

        if not mt5.symbol_select(
            SYMBOL,
            True
        ):

            mt5.shutdown()

            raise RuntimeError(
                f"Could not select {SYMBOL}."
            )

    print("MT5 CONNECTED")
    print("Account:", account.login)
    print("Server:", account.server)
    print("Balance:", account.balance)
    print("Symbol:", SYMBOL)

    return account


def disconnect_mt5():

    mt5.shutdown()

    print(
        "MT5 CONNECTION CLOSED"
    )