"""Read-only adapter for the existing PyTradoWix API."""
import os
from datetime import datetime, timezone
from .models import normalize_candle

class MarketDataError(RuntimeError):
    pass

async def fetch_historical(symbol: str, seconds: int, timeframe: int):
    email = os.getenv("TRADOWIX_EMAIL")
    password = os.getenv("TRADOWIX_PASSWORD")
    if not email or not password:
        raise MarketDataError(
            "API credentials not configured. Set TRADOWIX_EMAIL and TRADOWIX_PASSWORD in .env."
        )
    try:
        from pytradowix import Tradowix
    except Exception as exc:
        raise MarketDataError(f"Could not import local pytradowix package: {exc}") from exc

    client = Tradowix(email=email, password=password, is_demo=True)
    try:
        await client.connect()
        rows = await client.get_historical_candles(
            symbol=symbol, amount_of_seconds=seconds, period=timeframe
        )
        candles = [normalize_candle(row) for row in rows]
        candles.sort(key=lambda c: c.time)
        # Keep the most recent candle per timestamp and validate OHLC values.
        dedup = {int(c.time): c for c in candles if c.time > 0 and
                 min(c.open, c.high, c.low, c.close) > 0 and
                 c.high >= max(c.open, c.close, c.low) and
                 c.low <= min(c.open, c.close, c.high)}
        return [c.to_dict() for c in sorted(dedup.values(), key=lambda c: c.time)]
    except Exception as exc:
        raise MarketDataError(f"Historical data request failed: {exc}") from exc
    finally:
        await client.close()

def utc_now():
    return datetime.now(timezone.utc).isoformat()
