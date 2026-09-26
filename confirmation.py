print("=== LAST TRADE DEBUG ==="); print("SYMBOL:", globals().get("SYMBOL")); print("LAST SIGNAL:", globals().get("last_signal")); print("LAST ENTRY:", globals().get("last_entry")); print("LAST FIB:", globals().get("last_fib")); print("LAST H12:", globals().get("last_h12")); print("LAST SL:", globals().get("last_sl")); print("LAST TP:", globals().get("last_tp"))


print([k for k in globals() if any(x in k.lower() for x in ["signal","fib","order","trade","entry","setup","sl","tp"])])

print("BOT ACTIVE:", "AUTOMATIC BOT RUNNING" in globals().get("__doc__", ""))

print("BOT PROCESS CHECK")

import os; print(os.getcwd())

import os; print("DESKTOP:", os.listdir(os.path.join(os.path.expanduser("~"), "Desktop"))); print("DOCUMENTS:", os.listdir(os.path.join(os.path.expanduser("~"), "Documents")))

import os; print(os.getcwd())

import os; print([os.path.join(r"C:\Users\silvi", f) for f in os.listdir(r"C:\Users\silvi") if f.lower().endswith(".py")])

import os; print([os.path.join(r"C:\Users\silvi", f) for root,dirs,files in os.walk(r"C:\Users\silvi") if "AppData" not in root for f in files if 
f.lower().endswith(".py")][:50])

exec(open(r"C:\Downloads\silvi\xauusd_auto_bot.py", encoding="utf-8").read())

print("BOT FILE TEST:", __import__("os").path.exists(r"C:\Users\silvi\xauusd_auto_bot.py"))

import os; print([repr(os.path.join(root,f)) for root,dirs,files in os.walk(r"C:\Users\silvi") if "AppData" not in root for f in files if f.lower()=="xauusd_auto_bot.py"])

exec(open(r"C:\Users\silvi\Downloads\xauusd_auto_bot.py", encoding="utf-8").read())
