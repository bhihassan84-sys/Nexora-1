"""NEXORA local dashboard server. Read-only signal analysis; no trade execution."""
import asyncio
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv
from nexora_engine.config import settings
from nexora_engine.market_data import fetch_historical, MarketDataError, utc_now
from nexora_engine.signal_engine import analyze
from nexora_engine.backtest import evaluate

ROOT = Path(__file__).resolve().parent
WEB = ROOT / "nexora_web"
app = Flask(__name__, static_folder=str(WEB), static_url_path="/static")
_last = {"signal":"NO SIGNAL","confidence":0,"reason":"Click Refresh to request historical candles.",
         "symbol":settings.symbol,"candles":0,"updated_at":None,"indicators":{}}

@app.get("/")
def index():
    return send_from_directory(WEB, "index.html")

@app.get("/health")
def health():
    return jsonify({"status":"ok","app":"NEXORA","mode":"signal-only"})

@app.get("/api/status")
def status():
    return jsonify(_last)

@app.post("/api/analyze")
def run_analysis():
    global _last
    symbol = (request.json or {}).get("symbol", settings.symbol)
    allowed = symbol.strip()
    if not allowed or len(allowed) > 40:
        return jsonify({"error":"Invalid symbol."}), 400
    try:
        candles = asyncio.run(fetch_historical(allowed, settings.history_seconds, settings.timeframe_seconds))
        if len(candles) < settings.min_candles:
            return jsonify({"error":f"Only {len(candles)} candles received; need at least {settings.min_candles}.",
                            "signal":"NO SIGNAL"}), 422
        result = analyze(candles)
        _last = {**result,"symbol":allowed,"candles":len(candles),"updated_at":utc_now(),
                 "backtest":evaluate(candles)}
        return jsonify(_last)
    except MarketDataError as exc:
        return jsonify({"error":str(exc),"signal":"NO SIGNAL"}), 503
    except Exception:
        app.logger.exception("Unexpected analysis error")
        return jsonify({"error":"Unexpected server error. Check terminal logs.","signal":"NO SIGNAL"}), 500

if __name__ == "__main__":
    load_dotenv()
    app.run(host="0.0.0.0", port=int(__import__("os").getenv("PORT", "5000")), debug=False)
