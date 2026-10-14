"""Simple next-candle directional evaluation; educational, not a profit simulator."""
from .signal_engine import analyze

def evaluate(candles, warmup=60):
    if len(candles) <= warmup + 1:
        return {"samples":0,"signals":0,"wins":0,"win_rate_pct":None,
                "message":"Not enough candles for an evaluation."}
    signals = wins = 0
    for i in range(warmup, len(candles)-1):
        result = analyze(candles[:i+1])
        side = result["signal"]
        if side not in ("BUY","SELL"):
            continue
        signals += 1
        next_close = candles[i+1]["close"]
        current_close = candles[i]["close"]
        if (side == "BUY" and next_close > current_close) or (side == "SELL" and next_close < current_close):
            wins += 1
    return {"samples":len(candles)-warmup-1,"signals":signals,"wins":wins,
            "win_rate_pct":round(wins/signals*100,2) if signals else None,
            "message":"Simple next-candle direction only; excludes payout, spread, execution, and expiry rules."}
