# NEXORA Signal Lab

NEXORA is a local, signal-only dashboard built on top of the included PyTradoWix project. The original `pytradowix/` source files are retained. The NEXORA additions live in `nexora_engine/`, `nexora_web/`, and `nexora_server.py`.

## Requirements
- Windows with Python 3.11+ recommended
- Internet connection for the existing TradoWix client
- A TradoWix account you are authorized to use

## Quick start (Windows / VS Code)
1. Extract the ZIP.
2. Open the extracted `pytradowix-main` folder in VS Code.
3. Open Terminal > New Terminal.
4. Run `py -m pip install -e .`
5. Run `py -m pip install -r requirements-nexora.txt`
6. Copy `.env.example` to `.env`, then enter your own account email/password in `.env`. Never send that file to anyone.
7. Run `py nexora_server.py`
8. Open `http://127.0.0.1:5000` in your browser.

Alternatively double-click `run_nexora.bat`. If the `py` command is unavailable, install Python and enable the Python Launcher.

## What it currently does
- Uses the existing `pytradowix.Tradowix` client for historical candle requests.
- Normalizes and validates OHLC candle records.
- Calculates EMA 9/21/50, RSI 14, ATR 14, and Bollinger Bands.
- Emits conservative BUY / SELL / NO SIGNAL rule-based analysis.
- Provides a simple next-candle directional backtest summary.
- Shows a responsive dark dashboard.

## Important limitations
- The signal engine is a starter baseline, not an advanced or trained AI model.
- The displayed “rule strength” is not a calibrated probability or guaranteed win rate.
- The included backtest is a simple next-candle direction check. It is not a complete binary-options profitability simulation; it excludes payout, spread, execution delay, expiry rules, and slippage.
- API login, history access, OTC symbol availability, and live stream behavior must be verified against the account and current platform behavior.
- This version does **not** place trades automatically. Trading methods from the original library are not called by NEXORA.
- No API credentials are bundled. Configure your own `.env` locally.
- If your local API wrapper has connection incompatibilities, the UI reports the error rather than inventing market data.

## API
- `GET /health` — local server health
- `GET /api/status` — last analysis state
- `POST /api/analyze` with `{"symbol":"USDJPY-OTC"}` — fetch history and analyze

## Troubleshooting
- `ModuleNotFoundError`: repeat the install commands from the project root.
- Credentials error: set `TRADOWIX_EMAIL` and `TRADOWIX_PASSWORD` in `.env`.
- API timeout or auth error: check your account access and the original library's README; NEXORA will show NO SIGNAL instead of fabricating data.


## Mobile website / install-to-home-screen
The dashboard layout is responsive for phone screens. On the same Wi-Fi network, you may be able to open it from another device using your computer's local network IP and port 5000, provided the server is configured to listen on the network and your firewall allows it. For safety, the current server binds to `127.0.0.1`, so it is local to the computer by default.

To install the website like an app, deploy it behind HTTPS and open it in a supported mobile browser. Use the browser menu's "Add to Home Screen" / "Install app" option. The service worker caches the dashboard shell, but market analysis still requires the server and API connection to be available. The manifest has no custom icon yet.


## Run from your phone without a PC (cloud deployment)
This app needs a Python server, so it cannot run the full signal engine only by opening the ZIP on a phone. Deploy the project to a Python hosting service:
1. Upload this folder to a private GitHub repository (do not upload `.env`, passwords, or account credentials).
2. In Render, create a new Web Service connected to that repository.
3. Render can use `render.yaml`; set `TRADOWIX_EMAIL` and `TRADOWIX_PASSWORD` in the service environment settings, never in source code.
4. After deployment, open the HTTPS URL on your phone.
5. In the mobile browser menu, choose “Add to Home Screen” or “Install app” if available.

Important: verify the hosting provider permits this API's connection pattern and that the provider's network/location is compatible with the account. Do not use a real-money account for initial testing. Keep credentials private and restrict access to the deployment. A public URL can expose account-connected features if access control is not added; this starter project currently has no user login/authentication. Do not deploy it publicly with real credentials until access control is implemented.
