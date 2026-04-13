@echo off
REM md-skill-craft automated setup script (Windows)

setlocal enabledelayedexpansion

echo.
echo ╔═════════════════════════════════════╗
echo ║   md-skill-craft Setup Script       ║
echo ╚═════════════════════════════════════╝
echo.

REM Check Python version
echo Checking Python version...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found
    echo Install from: https://www.python.org/downloads
    echo Important: Check "Add Python to PATH"
    pause
    exit /b 1
)

python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist ".venv" (
    python -m venv .venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate
    pause
    exit /b 1
)
echo ✓ Activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo ✓ pip upgraded
echo.

REM Install package
echo Installing md-skill-craft...
pip install -e . >nul 2>&1
if errorlevel 1 (
    echo ERROR: Installation failed
    pause
    exit /b 1
)
echo ✓ Installation complete
echo.

REM Verify installation
echo Verifying installation...
where md-skill-craft >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ md-skill-craft command ready
) else (
    echo ! Command not found. Restart terminal.
)
echo.

echo ╔═════════════════════════════════════╗
echo ║   ✓ Setup Complete!                ║
echo ╚═════════════════════════════════════╝
echo.
echo Next steps:
echo   1. Install your LLM provider:
echo      pip install -e ".[claude]"    (Claude)
echo      pip install -e ".[openai]"    (OpenAI)
echo      pip install -e ".[gemini]"    (Gemini)
echo      pip install -e ".[all]"       (All LLMs)
echo.
echo   2. Run the application:
echo      md-skill-craft
echo.
pause
