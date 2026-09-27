import os
from dotenv import load_dotenv

load_dotenv()

# MT5 connection
MT5_LOGIN = int(os.getenv("MT5_LOGIN", "0"))
MT5_PASSWORD = os.getenv("MT5_PASSWORD", "")
MT5_SERVER = os.getenv("MT5_SERVER", "")

# Permanent trading symbol
SYMBOL = os.getenv("MT5_SYMBOL", "XAUUSDm")

# Permanent strategy timeframe
TIMEFRAME = "H12"

# --------------------------------------------------
# RISK MODEL
# --------------------------------------------------

# Stage 1:
# Fixed $20 risk until the account exceeds
# 200% profit from the recorded starting balance.
FIXED_RISK_USD = 20.0

# Stage 2:
# 10% of current balance after the trigger.
COMPOUNDING_RISK_PERCENT = 10.0

# Compounding trigger:
# 200% profit means balance is greater than
# 300% of the starting balance.
COMPOUNDING_TRIGGER_PROFIT_PERCENT = 200.0

# Starting balance must be supplied/stored as the
# permanent account baseline.
STARTING_BALANCE = float(
    os.getenv("STARTING_BALANCE", "0")
)

# Automatic execution
AUTO_EXECUTION = os.getenv(
    "AUTO_EXECUTION",
    "true"
).lower() == "true"

# Keep automatic execution restricted to demo
# until deliberately changed.
DEMO_ONLY = os.getenv(
    "DEMO_ONLY",
    "true"
).lower() == "true"

# MT5 order settings
MAGIC_NUMBER = 260926
DEVIATION = 20

# Bot loop
LOOP_SECONDS = int(
    os.getenv("LOOP_SECONDS", "15")
)