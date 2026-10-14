"""Shared data models and normalization helpers."""
from dataclasses import dataclass, asdict
from typing import Any

@dataclass
class Candle:
    time: float
    open: float
    high: float
    low: float
    close: float
    volume: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return asdict(self)

def normalize_candle(raw: Any) -> Candle:
    """Normalize a PyTradoWix Candle or a dict into NEXORA's Candle."""
    if isinstance(raw, dict):
        get = raw.get
        return Candle(
            time=float(get("time", get("timestamp", 0))),
            open=float(get("open", 0)), high=float(get("high", 0)),
            low=float(get("low", 0)), close=float(get("close", 0)),
            volume=float(get("volume", 0) or 0),
        )
    return Candle(
        time=float(raw.time), open=float(raw.open), high=float(raw.high),
        low=float(raw.low), close=float(raw.close),
        volume=float(getattr(raw, "volume", 0) or 0),
    )
