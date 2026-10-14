@echo off
cd /d "%~dp0"
py -m pip install -e .
py -m pip install -r requirements-nexora.txt
if not exist .env copy .env.example .env
py nexora_server.py
pause
