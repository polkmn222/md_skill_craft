"""Main CLI entry point and REPL loop."""

import sys
import os
from pathlib import Path
from typing import Optional

from md_skill_craft.config.settings import settings, usage_tracker
from md_skill_craft.config.keystore import KeyStore
from md_skill_craft.core.provider_factory import ProviderFactory
from md_skill_craft.modes.mode1_guide import Mode1Guide
from md_skill_craft.modes.mode2_analysis import Mode2Analysis
from md_skill_craft.ui.formatter import print_header, print_section, print_success, print_error, print_info, print_option
from md_skill_craft.ui.menu import Menu


def detect_env_var(provider: str) -> Optional[str]:
    """Detect API key from environment variables.

    Args:
        provider: Provider name ("claude", "gpt", "gemini")

    Returns:
        API key if found in environment, None otherwise
    """
    env_map = {
        "claude": "ANTHROPIC_API_KEY",
        "gpt": "OPENAI_API_KEY",
        "gemini": "GOOGLE_API_KEY",
    }

    if provider not in env_map:
        return None

    env_var = env_map[provider]
    return os.getenv(env_var)


def get_api_key(provider: str, use_env: bool = True) -> str:
    """Get API key for provider (from env var or keystore or user input).

    Args:
        provider: Provider name
        use_env: Whether to prefer environment variables

    Returns:
        API key

    Raises:
        ValueError: If no API key found and user cancels
    """
    # Try environment variable first if enabled
    if use_env:
        env_key = detect_env_var(provider)
        if env_key:
            print_info(f"환경변수에서 {provider.upper()} API 키를 감지했습니다.")
            choice = Menu.select(
                "사용하시겠어요?",
                options=[
                    (1, "환경변수 사용"),
                    (2, "새로 입력 (암호화 저장)"),
                ],
            )

            if choice == 1:
                return env_key

    # Try keystore
    stored_key = KeyStore.get(provider)
    if stored_key:
        print_info(f"저장된 {provider.upper()} API 키를 발견했습니다.")
        choice = Menu.select(
            "사용하시겠어요?",
            options=[
                (1, "저장된 키 사용"),
                (2, "새로 입력 (암호화 저장)"),
            ],
        )

        if choice == 1:
            return stored_key

    # Get new key from user
    print_section(f"{provider.upper()} API 키 입력")
    api_key = Menu.prompt(f"{provider.upper()} API 키를 입력하세요:")

    if not api_key:
        raise ValueError(f"No API key provided for {provider}")

    # Save to keystore
    KeyStore.save(provider, api_key)
    print_success(f"{provider.upper()} API 키가 안전하게 저장되었습니다.")

    return api_key


def run_onboarding() -> None:
    """Run first-time setup onboarding."""
    print_header("md-skill-craft v0.1.0", "LLM 프로젝트 설정 파일 생성기")
    print_info("처음 실행이에요. 간단한 설정을 진행할게요.\n")

    # Step 1: Language
    print_section("[1/4] 언어 선택")
    lang_choice = Menu.select(
        "언어를 선택하세요 / Select language:",
        options=[
            (1, "한국어"),
            (2, "English"),
        ],
    )
    settings.language = "ko" if lang_choice == 1 else "en"

    # Step 2: LLM Provider
    print_section("[2/4] LLM 도구 선택")
    llm_choice = Menu.select(
        "어떤 LLM 도구로 개발하시나요?",
        options=[
            (1, "Claude (Anthropic)", "CLAUDE.md 생성"),
            (2, "GPT / Codex (OpenAI)", "AGENT.md 생성"),
            (3, "Gemini (Google)", "GEMINI.md 생성"),
        ],
    )

    llm_map = {1: "claude", 2: "gpt", 3: "gemini"}
    selected_llm = llm_map[llm_choice]
    settings.llm = selected_llm

    # Step 3: API Key
    print_section("[3/4] API 키 설정")
    api_key = get_api_key(selected_llm, use_env=True)
    settings.use_env_var = True  # Remember user prefers env vars

    # Get default model for this LLM
    provider = ProviderFactory.create(selected_llm, api_key)
    default_model = provider.available_models[0] if provider.available_models else "unknown"
    settings.llm_model = default_model

    # Step 4: Mode
    print_section("[4/4] 사용 목적 선택")
    mode_choice = Menu.select(
        "어떤 목적으로 사용할까요?",
        options=[
            (1, "새 프로젝트 생성", "LLM과 대화하며 설정 파일 생성"),
            (2, "기존 프로젝트 분석", "현재 코드를 분석하고 설정 파일 검증"),
        ],
    )
    settings.mode = mode_choice

    # Step 4-B: Mode 2 additional question
    if mode_choice == 2:
        print_section("개입 방식 선택 (모드 2)")
        active_choice = Menu.select(
            "변경 방식을 선택하세요:",
            options=[
                (1, "능동적", "제안 후 승인하면 자동 적용"),
                (2, "수동적", "제안만 보여주고 직접 수정"),
            ],
        )
        settings.active_mode = active_choice == 1

    # Save settings
    settings.save()
    print_success("✅ 설정이 저장되었습니다! (/setup으로 언제든 변경 가능합니다.)")


def show_help() -> None:
    """Show help information."""
    print_header("md-skill-craft 도움말")

    print_section("내장 명령어")
    print_option(1, "/help", "도움말 표시")
    print_option(2, "/setup", "설정 변경 또는 확인")
    print_option(3, "/cost", "API 사용량 및 비용 조회")
    print_option(4, "/mode", "모드 전환 (1 ↔ 2)")
    print_option(5, "/exit", "프로그램 종료")

    print_section("현재 설정")
    print_info(f"언어: {settings.language}")
    print_info(f"LLM: {settings.llm}")
    print_info(f"모드: {settings.mode}")

    if settings.mode == 2:
        mode_str = "능동적" if settings.active_mode else "수동적"
        print_info(f"개입 방식: {mode_str}")


def show_cost() -> None:
    """Show API usage and costs."""
    from md_skill_craft.config.pricing import calculate_cost

    print_header("📊 API 사용량 및 비용")

    all_usage = usage_tracker.get_all()
    total_cost = 0.0

    for provider, usage in all_usage.items():
        input_tokens = usage["input_tokens"]
        output_tokens = usage["output_tokens"]

        if input_tokens == 0 and output_tokens == 0:
            continue

        # Get default model for this provider
        settings_model = settings.llm_model if settings.llm == provider else None
        if not settings_model:
            from md_skill_craft.config.pricing import get_models_by_provider
            models = get_models_by_provider(provider)
            settings_model = models[0] if models else None

        if settings_model:
            cost = calculate_cost(settings_model, input_tokens, output_tokens)
            total_cost += cost

            provider_name = {"claude": "Claude", "gpt": "GPT", "gemini": "Gemini"}.get(
                provider, provider
            )
            print_info(f"{provider_name} ({settings_model})")
            print_info(f"  입력: {input_tokens:,} 토큰 → ${cost * input_tokens / (input_tokens + output_tokens + 1):.3f}")
            print_info(f"  출력: {output_tokens:,} 토큰 → ${cost * output_tokens / (input_tokens + output_tokens + 1):.3f}")
            print_info(f"  소계: ${cost:.3f}")
            print_info("")

    print_section("합계")
    print_info(f"총 비용: ${total_cost:.3f}")
    print_info("[dim]가격: 2025년 4월 기준, 실제 청구액과 다를 수 있습니다.[/dim]")


def show_setup() -> None:
    """Show setup menu to change settings."""
    print_header("설정 변경")

    choice = Menu.select(
        "변경할 항목을 선택하세요:",
        options=[
            (1, "언어"),
            (2, "LLM 및 API 키"),
            (3, "모드 (1 ↔ 2)"),
            (4, "개입 방식", "(모드 2만 해당)" if settings.mode == 2 else ""),
            (5, "돌아가기"),
        ],
    )

    if choice == 1:
        lang_choice = Menu.select(
            "언어를 선택하세요:",
            options=[
                (1, "한국어"),
                (2, "English"),
            ],
        )
        settings.language = "ko" if lang_choice == 1 else "en"
        print_success("언어가 변경되었습니다.")

    elif choice == 2:
        llm_choice = Menu.select(
            "LLM을 선택하세요:",
            options=[
                (1, "Claude (Anthropic)"),
                (2, "GPT / Codex (OpenAI)"),
                (3, "Gemini (Google)"),
            ],
        )
        llm_map = {1: "claude", 2: "gpt", 3: "gemini"}
        new_llm = llm_map[llm_choice]
        api_key = get_api_key(new_llm, use_env=True)
        settings.llm = new_llm
        provider = ProviderFactory.create(new_llm, api_key)
        settings.llm_model = provider.available_models[0] if provider.available_models else "unknown"
        print_success(f"LLM이 {new_llm.upper()}로 변경되었습니다.")

    elif choice == 3:
        mode_choice = Menu.select(
            "모드를 선택하세요:",
            options=[
                (1, "새 프로젝트 생성"),
                (2, "기존 프로젝트 분석"),
            ],
        )
        settings.mode = mode_choice
        print_success(f"모드가 {mode_choice}로 변경되었습니다.")

    elif choice == 4 and settings.mode == 2:
        active_choice = Menu.select(
            "개입 방식을 선택하세요:",
            options=[
                (1, "능동적"),
                (2, "수동적"),
            ],
        )
        settings.active_mode = active_choice == 1
        print_success(f"개입 방식이 변경되었습니다.")

    elif choice == 5:
        return

    settings.save()


def main() -> int:
    """Main CLI entry point.

    Returns:
        Exit code
    """
    # Check if this is first run
    if settings.is_first_run:
        run_onboarding()

    # Main REPL loop
    print_header(f"md-skill-craft v0.1.0", f"LLM: {settings.llm.upper()} | 모드: {settings.mode}")
    print_info("모드 1: 새 프로젝트 가이드 생성\n모드 2: 기존 프로젝트 분석\n(/help로 명령어 확인)")

    while True:
        try:
            # Show prompt
            user_input = input("\nmd-skill-craft > ").strip()

            # Handle empty input
            if not user_input:
                print_info("엔터를 누르거나 텍스트를 입력하세요.")
                continue

            # Handle /commands
            if user_input.startswith("/"):
                cmd = user_input[1:].lower().split()[0]

                if cmd == "help":
                    show_help()
                elif cmd == "setup":
                    show_setup()
                elif cmd == "cost":
                    show_cost()
                elif cmd == "mode":
                    new_mode = Menu.select(
                        "모드를 선택하세요:",
                        options=[
                            (1, "새 프로젝트 생성"),
                            (2, "기존 프로젝트 분석"),
                        ],
                    )
                    settings.mode = new_mode
                    settings.save()
                    print_success(f"모드가 {new_mode}로 변경되었습니다.")
                elif cmd == "exit":
                    print_info("프로그램을 종료합니다.")
                    return 0
                else:
                    print_error(f"알 수 없는 명령어: {cmd}")

            else:
                # Normal input - pass to mode handler
                if settings.mode == 1:
                    # Mode 1: LLM interactive guide generation
                    guide = Mode1Guide()
                    guide.run(Path.cwd())
                elif settings.mode == 2:
                    # Mode 2: Project analysis and validation
                    analyzer = Mode2Analysis()
                    analyzer.run(Path.cwd())

        except KeyboardInterrupt:
            print_info("\n프로그램을 종료합니다.")
            return 0
        except Exception as e:
            print_error(f"오류 발생: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
