@echo off
REM Telegram Bot Startup Script

REM Set HuggingFace mirror for faster downloads in China
set HF_ENDPOINT=https://hf-mirror.com

REM Activate virtual environment and run bot
.\.venv\Scripts\python.exe -m src.main

pause
