#!/bin/bash
# md-skill-craft 자동 설치 스크립트 (macOS/Linux)

set -e  # 에러 발생시 즉시 중단

echo "╭─────────────────────────────────────╮"
echo "│   md-skill-craft 자동 설치 스크립트  │"
echo "╰─────────────────────────────────────╯"
echo ""

# Python 버전 확인
echo "📋 Python 버전 확인 중..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3를 찾을 수 없습니다."
    echo "   설치: brew install python3  (macOS)"
    echo "   또는: sudo apt-get install python3  (Linux)"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "   Python 버전: $PYTHON_VERSION"

if python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 12) else 1)'; then
    echo "   ✅ Python 3.12+ 확인됨"
else
    echo "   ⚠️  Python 3.12 이상이 필요합니다."
    exit 1
fi
echo ""

# 가상환경 생성
echo "🔧 가상환경 생성 중..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
    echo "   ✅ 가상환경 생성 완료"
else
    echo "   ℹ️  기존 가상환경 발견"
fi
echo ""

# 가상환경 활성화
echo "⚡ 가상환경 활성화..."
source .venv/bin/activate
echo "   ✅ 활성화 완료"
echo ""

# pip 업그레이드
echo "📦 pip 업그레이드 중..."
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
echo "   ✅ pip 업그레이드 완료"
echo ""

# 의존성 설치
echo "📥 의존성 설치 중..."
pip install -e . > /dev/null 2>&1
echo "   ✅ 의존성 설치 완료"
echo ""

# 설치 검증
echo "✓ 설치 검증 중..."
if command -v md-skill-craft &> /dev/null; then
    echo "   ✅ md-skill-craft 명령어 사용 가능"
else
    echo "   ⚠️  명령어를 찾을 수 없음. 다시 활성화해주세요:"
    echo "   source .venv/bin/activate"
fi
echo ""

echo "╭─────────────────────────────────────╮"
echo "│   ✅ 설치 완료!                      │"
echo "╰─────────────────────────────────────╯"
echo ""
echo "🚀 시작하기:"
echo "   1. 가상환경 활성화:"
echo "      source .venv/bin/activate"
echo ""
echo "   2. 프로그램 실행:"
echo "      md-skill-craft"
echo ""
echo "📖 테스트:"
echo "   pytest tests/ -v"
echo ""
