"""Dependency-free technical indicators for OHLC candle sequences."""
from math import sqrt

def ema(values, period):
    if len(values) < period:
        return None
    alpha = 2 / (period + 1)
    current = sum(values[:period]) / period
    for value in values[period:]:
        current = alpha * value + (1 - alpha) * current
    return current

def rsi(values, period=14):
    if len(values) <= period:
        return None
    changes = [values[i] - values[i-1] for i in range(1, len(values))]
    gains = [max(x, 0) for x in changes]
    losses = [max(-x, 0) for x in changes]
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    for i in range(period, len(changes)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
    if avg_loss == 0:
        return 100.0 if avg_gain else 50.0
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def atr(candles, period=14):
    if len(candles) <= period:
        return None
    tr = []
    for i, c in enumerate(candles):
        high, low = c["high"], c["low"]
        if i == 0:
            tr.append(high - low)
        else:
            prev = candles[i-1]["close"]
            tr.append(max(high-low, abs(high-prev), abs(low-prev)))
    return sum(tr[-period:]) / period

def bollinger(values, period=20, multiplier=2):
    if len(values) < period:
        return None
    sample = values[-period:]
    mean = sum(sample) / period
    sd = sqrt(sum((x-mean)**2 for x in sample) / period)
    return {"middle": mean, "upper": mean + multiplier*sd, "lower": mean - multiplier*sd}
