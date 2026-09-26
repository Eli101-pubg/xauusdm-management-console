import os
from dotenv import load_dotenv

load_dotenv()

MT5_LOGIN = int(os.getenv("MT5_LOGIN", "0"))
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER = os.getenv("MT5_SERVER", "")

SYMBOL = os.getenv("MT5_SYMBOL", "XAUUSDm")

TIMEFRAME = "M15"

RISK_PER_TRADE = 20.0

MAGIC_NUMBER = 260926

DEVIATION = 20
