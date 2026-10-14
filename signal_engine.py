"""Transparent rule-based signal engine; no guaranteed win-rate claims."""
from .indicators import ema, rsi, atr, bollinger

def analyze(candles):
    closes = [float(c["close"]) for c in candles]
    if len(closes) < 60:
        return {"signal":"NO SIGNAL", "confidence":0, "reason":"At least 60 valid candles are required.", "indicators":{}}
    e9, e21, e50 = ema(closes,9), ema(closes,21), ema(closes,50)
    rv, av, bb = rsi(closes), atr(candles), bollinger(closes)
    if None in (e9,e21,e50,rv,av) or bb is None:
        return {"signal":"NO SIGNAL","confidence":0,"reason":"Indicator warm-up is incomplete.","indicators":{}}
    score = 0
    reasons = []
    if e9 > e21 > e50:
        score += 2; reasons.append("EMA trend is bullish")
    elif e9 < e21 < e50:
        score -= 2; reasons.append("EMA trend is bearish")
    else:
        reasons.append("EMA trend is mixed")
    if rv >= 55:
        score += 1; reasons.append("RSI momentum is bullish")
    elif rv <= 45:
        score -= 1; reasons.append("RSI momentum is bearish")
    else:
        reasons.append("RSI momentum is neutral")
    last = closes[-1]
    if last > bb["middle"]:
        score += 1
    elif last < bb["middle"]:
        score -= 1
    # Conservative decision: contradictory or weak readings become NO SIGNAL.
    if score >= 3:
        signal = "BUY"
    elif score <= -3:
        signal = "SELL"
    else:
        signal = "NO SIGNAL"
    strength = min(95, round(abs(score) / 4 * 100)) if signal != "NO SIGNAL" else 0
    return {
        "signal":signal, "confidence":strength,
        "reason":"; ".join(reasons) if reasons else "No clear setup.",
        "indicators":{"ema9":round(e9,6),"ema21":round(e21,6),"ema50":round(e50,6),
                      "rsi14":round(rv,2),"atr14":round(av,6),
                      "bollinger_middle":round(bb["middle"],6),"last_close":round(last,6)},
        "note":"Rule score only; this is not a calibrated win probability or a guarantee."
    }
