import MetaTrader5 as mt5

from config import MT5_LOGIN, MT5_PASSWORD, MT5_SERVER


def connect_mt5():
    if not mt5.initialize():
        raise RuntimeError(f"MT5 initialization failed: {mt5.last_error()}")

    authorized = mt5.login(
        login=MT5_LOGIN,
        password=MT5_PASSWORD,
        server=MT5_SERVER
    )

    if not authorized:
        error = mt5.last_error()
        mt5.shutdown()
        raise RuntimeError(f"MT5 login failed: {error}")

    account = mt5.account_info()

    if account is None:
        mt5.shutdown()
        raise RuntimeError("Could not retrieve MT5 account information")

    print("MT5 CONNECTED")
    print("Account:", account.login)
    print("Server:", account.server)
    print("Balance:", account.balance)

    return account


def disconnect_mt5():
    mt5.shutdown()
