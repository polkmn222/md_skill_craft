"""Localization strings for Korean and English."""

from typing import Literal

# Translation strings
STRINGS = {
    # Onboarding - Section titles
    "section.language_select": {
        "ko": "[1/4] Language 선택",
        "en": "[1/4] Select Language",
    },
    "section.llm_select": {
        "ko": "[2/4] LLM 도구 선택",
        "en": "[2/4] Select LLM Provider",
    },
    "section.api_key": {
        "ko": "[3/4] API 키 설정",
        "en": "[3/4] API Key Setup",
    },
    "section.select_mode": {
        "ko": "[4/4] Select mode:",
        "en": "[4/4] Select mode:",
    },
    "section.intervention_method": {
        "ko": "Intervention method (Mode 2):",
        "en": "Intervention method (Mode 2):",
    },

    # Prompts
    "prompt.select_language": {
        "ko": "언어를 선택하세요:",
        "en": "Select language:",
    },
    "prompt.select_llm": {
        "ko": "어떤 LLM을 사용할까요?",
        "en": "Which LLM provider?",
    },
    "prompt.select_mode_purpose": {
        "ko": "어떤 목적으로 사용할까요?",
        "en": "What is your purpose?",
    },
    "prompt.select_intervention": {
        "ko": "어떤 방식으로 실행할까요?",
        "en": "Select intervention:",
    },
    "prompt.change_language": {
        "ko": "Language를 선택하세요:",
        "en": "Select language:",
    },
    "prompt.change_llm": {
        "ko": "어떤 LLM을 선택하세요:",
        "en": "Select LLM:",
    },
    "prompt.change_mode": {
        "ko": "모드를 선택하세요:",
        "en": "Select mode:",
    },
    "prompt.change_intervention": {
        "ko": "Intervention을 선택하세요:",
        "en": "Select intervention:",
    },

    # Success messages
    "success.settings_saved": {
        "ko": "✅ 설정이 저장되었습니다! (/setup으로 변경 가능)",
        "en": "✅ Settings saved! (Use /setup to change anytime)",
    },
    "success.language_changed": {
        "ko": "Language가 변경되었습니다.",
        "en": "Language changed.",
    },
    "success.llm_changed": {
        "ko": "LLM이 변경되었습니다.",
        "en": "LLM changed.",
    },
    "success.mode_changed": {
        "ko": "모드가 변경되었습니다.",
        "en": "Mode changed.",
    },
    "success.intervention_changed": {
        "ko": "Intervention이 변경되었습니다.",
        "en": "Intervention changed.",
    },
    "success.api_key_saved": {
        "ko": "{provider} API 키가 안전하게 저장되었습니다.",
        "en": "{provider} API key saved securely",
    },

    # Help menu
    "help.help_command": {
        "ko": "도움말 표시",
        "en": "Show help",
    },
    "help.setup_command": {
        "ko": "설정 변경 또는 보기",
        "en": "Change or view settings",
    },
    "help.cost_command": {
        "ko": "API 사용량 및 비용 보기",
        "en": "View API usage and costs",
    },
    "help.mode_command": {
        "ko": "모드 전환 (1 ↔ 2)",
        "en": "Switch mode (1 ↔ 2)",
    },
    "help.exit_command": {
        "ko": "프로그램 종료",
        "en": "Exit program",
    },

    # Settings menu
    "menu.select_to_change": {
        "ko": "변경할 항목을 선택하세요:",
        "en": "Select what to change:",
    },
    "menu.option_language": {
        "ko": "Language",
        "en": "Language",
    },
    "menu.option_llm": {
        "ko": "LLM & API Key",
        "en": "LLM & API Key",
    },
    "menu.option_mode": {
        "ko": "Mode (1 ↔ 2)",
        "en": "Mode (1 ↔ 2)",
    },
    "menu.option_intervention": {
        "ko": "Intervention",
        "en": "Intervention",
    },
    "menu.mode2_only": {
        "ko": "(Mode 2 전용)",
        "en": "(Mode 2 only)",
    },
    "menu.back": {
        "ko": "돌아가기",
        "en": "Back",
    },

    # Mode descriptions
    "mode.generate_guide": {
        "ko": "새 프로젝트 — 설정 파일을 대화형으로 생성",
        "en": "New project — Generate config files interactively",
    },
    "mode.analyze_project": {
        "ko": "프로젝트 분석 — 프로젝트 설정 검증",
        "en": "Analyze project — Validate project configuration",
    },
    "mode.generate_guide_description": {
        "ko": "설정 파일 대화형 생성",
        "en": "Generate config files interactively",
    },
    "mode.analyze_project_description": {
        "ko": "프로젝트 설정 검증",
        "en": "Validate project configuration",
    },

    # Intervention options
    "intervention.active": {
        "ko": "Active",
        "en": "Active",
    },
    "intervention.active_description": {
        "ko": "자동으로 제안 적용",
        "en": "Auto-apply suggestions",
    },
    "intervention.passive": {
        "ko": "Passive",
        "en": "Passive",
    },
    "intervention.passive_description": {
        "ko": "제안만 표시",
        "en": "Show suggestions only",
    },

    # Main REPL
    "repl.mode_info": {
        "ko": "Mode 1 - 설정 파일 생성\nMode 2 - 프로젝트 분석\n(/help로 명령어 확인)",
        "en": "Mode 1 - Generate Guide\nMode 2 - Analyze project\n(Use /help for commands)",
    },
    "repl.exiting": {
        "ko": "프로그램을 종료합니다...",
        "en": "Exiting...",
    },
    "repl.unknown_command": {
        "ko": "알 수 없는 명령어: {cmd}",
        "en": "Unknown command: {cmd}",
    },

    # Mode 2 Analysis
    "analysis.select_depth": {
        "ko": "어떤 깊이로 분석할까요?",
        "en": "What depth of analysis?",
    },
    "analysis.depth_fast": {
        "ko": "Fast",
        "en": "Fast",
    },
    "analysis.depth_fast_desc": {
        "ko": "README, 설정 파일만",
        "en": "README, config files only",
    },
    "analysis.depth_standard": {
        "ko": "Standard",
        "en": "Standard",
    },
    "analysis.depth_standard_desc": {
        "ko": "최상위 소스 구조",
        "en": "Top-level source structure",
    },
    "analysis.depth_deep": {
        "ko": "Deep",
        "en": "Deep",
    },
    "analysis.depth_deep_desc": {
        "ko": "모든 소스 파일",
        "en": "All source files",
    },
    "analysis.scanning": {
        "ko": "스캔 중: {root}",
        "en": "Scanning: {root}",
    },
    "analysis.analyzing": {
        "ko": "프로젝트 분석 중...",
        "en": "Analyzing with LLM...",
    },
    "analysis.no_info_found": {
        "ko": "프로젝트 정보를 찾을 수 없습니다.",
        "en": "No project information found",
    },
    "analysis.update_config": {
        "ko": "설정 파일을 업데이트할까요?",
        "en": "Update configuration file?",
    },
    "analysis.config_updated": {
        "ko": "설정 파일이 업데이트되었습니다.",
        "en": "Configuration file updated",
    },
    "analysis.what_to_do": {
        "ko": "어떻게 하시겠습니까?",
        "en": "What would you like to do?",
    },
    "analysis.save_as_suggested": {
        "ko": "{file_type}.md.suggested로 저장",
        "en": "Save as {file_type}.md.suggested",
    },
    "analysis.terminal_output_only": {
        "ko": "터미널 출력만",
        "en": "Terminal output only",
    },
    "analysis.skip": {
        "ko": "건너뛰기",
        "en": "Skip",
    },
    "analysis.file_saved": {
        "ko": "{filename}이(가) 저장되었습니다.",
        "en": "{filename} saved",
    },
    "analysis.no_results": {
        "ko": "분석 결과가 없습니다.",
        "en": "No analysis results",
    },

    # Misc
    "misc.yes": {
        "ko": "예",
        "en": "Yes",
    },
    "misc.no": {
        "ko": "아니오",
        "en": "No",
    },
    "misc.press_enter": {
        "ko": "Enter를 누르거나 텍스트를 입력하세요.",
        "en": "Press Enter or type text",
    },
}


def get_string(key: str, lang: str = "en", **kwargs) -> str:
    """Get localized string.

    Args:
        key: String key (e.g., "section.language_select")
        lang: Language code ("ko" or "en")
        **kwargs: Format parameters

    Returns:
        Localized string
    """
    if key not in STRINGS:
        return f"[MISSING: {key}]"

    translation = STRINGS[key]
    text = translation.get(lang, translation.get("en", f"[MISSING: {key}]"))

    if kwargs:
        return text.format(**kwargs)
    return text


def get_text(key: str, lang: str = "en") -> str:
    """Alias for get_string without format parameters."""
    return get_string(key, lang)
