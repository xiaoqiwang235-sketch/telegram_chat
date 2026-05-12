@echo off
REM Telegram Bot Startup Script with Proxy Support
REM
REM This script starts the Telegram bot with optimized settings for China users.
REM
REM Configuration:
REM 1. If you need a proxy to access Telegram, uncomment and configure the proxy lines below
REM 2. Make sure your .env file has the correct BOT_TOKEN and other settings

echo ========================================
echo  Telegram Bot Starting...
echo ========================================
echo.

REM Set HuggingFace mirror for faster model downloads in China
set HF_ENDPOINT=https://hf-mirror.com
echo [INFO] HuggingFace mirror: %HF_ENDPOINT%

REM Proxy Configuration (UNCOMMENT if you need proxy to access Telegram)
REM Common proxy formats:
REM - HTTP/HTTPS proxy: http://127.0.0.1:7890
REM - SOCKS5 proxy: socks5://127.0.0.1:1080
REM
REM set HTTP_PROXY=http://127.0.0.1:7890
REM set HTTPS_PROXY=http://127.0.0.1:7890
REM
if defined HTTP_PROXY (
    echo [INFO] Using proxy: %HTTP_PROXY%
) else (
    echo [INFO] No proxy configured (direct connection)
)

echo.
echo [INFO] Starting bot...
echo.

REM Run the bot
uv run python -m src.main

REM Pause if there's an error
if errorlevel 1 (
    echo.
    echo ========================================
    echo [ERROR] Bot startup failed!
    echo ========================================
    echo.
    echo Common issues:
    echo 1. Network timeout - Configure proxy in this script
    echo 2. Database not running - Start MySQL service
    echo 3. Wrong credentials - Check .env file
    echo.
    pause
)
