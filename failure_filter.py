def check_m5_failure(
    direction,
    entry_price,
    m5_low,
    m5_high,
    stop_loss
):
    if direction == "BUY":
        adverse_move = entry_price - m5_low

    elif direction == "SELL":
        adverse_move = m5_high - entry_price

    else:
        raise ValueError("Direction must be BUY or SELL")

    if adverse_move <= 0:
        return False

    if direction == "BUY" and m5_low <= stop_loss:
        return True

    if direction == "SELL" and m5_high >= stop_loss:
        return True

    return False
