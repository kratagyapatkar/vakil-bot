@echo off
echo.
echo =============================================
echo    VakilBot - Indian Legal Help Bot
echo =============================================
echo.

cd /d "%~dp0backend"

echo Checking dependencies...
py -3 -m pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Starting VakilBot server...
echo Open your browser: http://localhost:8000
echo Press Ctrl+C to stop
echo.
py -3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
pause
