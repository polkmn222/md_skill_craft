@echo off
REM md-skill-craft 자동 설치 스크립트 (Windows)

setlocal enabledelayedexpansion

echo.
echo ╔═════════════════════════════════════╗
echo ║   md-skill-craft 자동 설치 스크립트  ║
echo ╚═════════════════════════════════════╝
echo.

REM Python 버전 확인
echo 📋 Python 버전 확인 중...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python을 찾을 수 없습니다.
    echo    https://www.python.org/downloads 에서 설치하세요.
    echo    설치 시 "Add Python to PATH" 옵션을 반드시 체크하세요.
    pause
    exit /b 1
)

python --version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo    ✅ Python 설치 확인됨
echo.

REM 가상환경 생성
echo 🔧 가상환경 생성 중...
if not exist ".venv" (
    python -m venv .venv
    echo    ✅ 가상환경 생성 완료
) else (
    echo    ℹ️  기존 가상환경 발견
)
echo.

REM 가상환경 활성화
echo ⚡ 가상환경 활성화...
call .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ 가상환경 활성화 실패
    pause
    exit /b 1
)
echo    ✅ 활성화 완료
echo.

REM pip 업그레이드
echo 📦 pip 업그레이드 중...
python -m pip install --upgrade pip setuptools wheel >nul 2>&1
echo    ✅ pip 업그레이드 완료
echo.

REM 의존성 설치
echo 📥 의존성 설치 중...
pip install -e . >nul 2>&1
if errorlevel 1 (
    echo ❌ 의존성 설치 실패
    pause
    exit /b 1
)
echo    ✅ 의존성 설치 완료
echo.

REM 설치 검증
echo ✓ 설치 검증 중...
where md-skill-craft >nul 2>&1
if %errorlevel% equ 0 (
    echo    ✅ md-skill-craft 명령어 사용 가능
) else (
    echo    ⚠️  명령어를 찾을 수 없음. 터미널을 다시 열어주세요.
)
echo.

echo ╔═════════════════════════════════════╗
echo ║   ✅ 설치 완료!                      ║
echo ╚═════════════════════════════════════╝
echo.
echo 🚀 시작하기:
echo    1. 가상환경이 활성화되었습니다.
echo.
echo    2. 프로그램 실행:
echo       md-skill-craft
echo.
echo 📖 테스트:
echo    pytest tests/ -v
echo.
pause
