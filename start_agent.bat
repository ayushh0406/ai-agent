@echo off
echo 🚀 Voice AI Agent Quick Start
echo ================================

echo 📦 Installing dependencies...
python setup.py

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Setup failed! Please check the errors above.
    pause
    exit /b 1
)

echo.
echo ✅ Setup completed!
echo.
echo 🎤 Starting Voice AI Agent...
echo Say "Hello Jarvis" to begin!
echo.

python agents\voice_agent\voice_runner.py

pause
