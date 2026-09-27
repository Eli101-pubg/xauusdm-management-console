import os
from dotenv import load_dotenv

load_dotenv()


# MT5 connection
MT5_LOGIN = int(
    os.getenv(
        "MT5_LOGIN",
        "0"
    )
)

MT5_PASSWORD = os.getenv(
    "MT5_PASSWORD",
    ""
)

MT5_SERVER = os.getenv(
    "MT5_SERVER",
    ""
)


# Permanent trading symbol
SYMBOL = os.getenv(
    "MT5_SYMBOL",
    "XAUUSDm"
)


# Permanent strategy timeframe
TIMEFRAME = "H12"


# Permanent risk per trade
RISK_PER_TRADE = 20.0


# Permanent stop-loss distance
SL_POINTS = 20000


# Automatic execution
AUTO_EXECUTION = os.getenv(
    "AUTO_EXECUTION",
    "true"
).lower() == "true"


# Demo-only protection
DEMO_ONLY = os.getenv(
    "DEMO_ONLY",
    "true"
).lower() == "true"


# MT5 order settings
MAGIC_NUMBER = 260926
DEVIATION = 20


# Bot loop
LOOP_SECONDS = int(
    os.getenv(
        "LOOP_SECONDS",
        "15"
    )
)