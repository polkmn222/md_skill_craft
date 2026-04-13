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
            print_info(f"Detected {provider.upper()} API key in environment")
            choice = Menu.select(
                "Use this API key?",
                options=[
                    (1, "Use environment variable"),
                    (2, "Enter new key (encrypted)"),
                ],
            )

            if choice == 1:
                return env_key

    # Try keystore
    stored_key = KeyStore.get(provider)
    if stored_key:
        print_info(f"Stored {provider.upper()} API key found")
        choice = Menu.select(
            "Use this API key?",
            options=[
                (1, "Stored 키 사용"),
                (2, "Enter new key (encrypted)"),
            ],
        )

        if choice == 1:
            return stored_key

    # Get new key from user
    print_section(f"{provider.upper()} Enter API Key")
    api_key = Menu.prompt(f"{provider.upper()} Enter API key:")

    if not api_key:
        raise ValueError(f"No API key provided for {provider}")

    # Save to keystore
    KeyStore.save(provider, api_key)
    print_success(f"{provider.upper()} API key saved securely")

    return api_key


def run_onboarding() -> None:
    """Run first-time setup onboarding."""
    print_header("md-skill-craft v0.1.0", "LLM Project Configuration Generator")
    print_info("First run setup\n")

    # Step 1: Language
    print_section("[1/4] Language 선택")
    lang_choice = Menu.select(
        "Select language:",
        options=[
            (1, "Korean"),
            (2, "English"),
        ],
    )
    settings.language = "ko" if lang_choice == 1 else "en"

    # Step 2: LLM Provider
    print_section("[2/4] LLM 도구 선택")
    llm_choice = Menu.select(
        "Which LLM provider?",
        options=[
            (1, "Claude (Anthropic)", "CLAUDE.md"),
            (2, "GPT / Codex (OpenAI)", "AGENT.md"),
            (3, "Gemini (Google)", "GEMINI.md"),
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
    print_section("[4/4] Select mode:")
    mode_choice = Menu.select(
        "어떤 목적으로 사용할까요?",
        options=[
            (1, "New project", "Generate config files interactively"),
            (2, "Analyze project", "Validate project configuration"),
        ],
    )
    settings.mode = mode_choice

    # Step 4-B: Mode 2 additional question
    if mode_choice == 2:
        print_section("Intervention method (Mode 2):")
        active_choice = Menu.select(
            "Select intervention:",
            options=[
                (1, "Active", "Auto-apply suggestions"),
                (2, "Passive", "Show suggestions only"),
            ],
        )
        settings.active_mode = active_choice == 1

    # Save settings
    settings.save()
    print_success("✅ Settings saved! (Use /setup to change anytime)")


def show_help() -> None:
    """Show help information."""
    print_header("md-skill-craft Help")

    print_section("Built-in Commands")
    print_option(1, "/help", "Help 표시")
    print_option(2, "/setup", "Change or view settings")
    print_option(3, "/cost", "View API usage and costs")
    print_option(4, "/mode", "Switch mode (1 ↔ 2)")
    print_option(5, "/exit", "Exit program")

    print_section("Current Settings")
    print_info(f"Language: {settings.language}")
    print_info(f"LLM: {settings.llm}")
    print_info(f"Mode: {settings.mode}")

    if settings.mode == 2:
        mode_str = "Active" if settings.active_mode else "Passive"
        print_info(f"Intervention: {mode_str}")


def show_cost() -> None:
    """Show API usage and costs."""
    from md_skill_craft.config.pricing import calculate_cost

    print_header("API Usage and Costs")

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

    print_section("Total")
    print_info(f"Total cost: ${total_cost:.3f}")
    print_info("[dim][Prices as of April 2025, actual billing may vary][/dim]")


def show_setup() -> None:
    """Show setup menu to change settings."""
    print_header("Settings")

    choice = Menu.select(
        "Select what to change:",
        options=[
            (1, "Language"),
            (2, "LLM & API Key"),
            (3, "Mode (1 ↔ 2)"),
            (4, "Intervention", "(Mode 2 only)" if settings.mode == 2 else ""),
            (5, "Back"),
        ],
    )

    if choice == 1:
        lang_choice = Menu.select(
            "Language를 선택하세요:",
            options=[
                (1, "Korean"),
                (2, "English"),
            ],
        )
        settings.language = "ko" if lang_choice == 1 else "en"
        print_success("Language가 변경되었습니다.")

    elif choice == 2:
        llm_choice = Menu.select(
            "Select LLM:",
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
        print_success(f"LLM: {new_llm.upper()}selected")

    elif choice == 3:
        mode_choice = Menu.select(
            "Select mode:",
            options=[
                (1, "New project"),
                (2, "Analyze project"),
            ],
        )
        settings.mode = mode_choice
        print_success(f"Mode: {mode_choice}selected")

    elif choice == 4 and settings.mode == 2:
        active_choice = Menu.select(
            "Intervention을 선택하세요:",
            options=[
                (1, "Active"),
                (2, "Passive"),
            ],
        )
        settings.active_mode = active_choice == 1
        print_success(f"Intervention이 변경되었습니다.")

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
    print_header(f"md-skill-craft v0.1.0", f"LLM: {settings.llm.upper()} | Mode: {settings.mode}")
    print_info("Mode 1 - Generate Guide\n모드 2: Analyze project\n(Use /help for commands)")

    while True:
        try:
            # Show prompt
            user_input = input("\nmd-skill-craft > ").strip()

            # Handle empty input
            if not user_input:
                print_info("Press Enter or type text")
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
                        "Select mode:",
                        options=[
                            (1, "New project"),
                            (2, "Analyze project"),
                        ],
                    )
                    settings.mode = new_mode
                    settings.save()
                    print_success(f"Mode: {new_mode}selected")
                elif cmd == "exit":
                    print_info("Exiting...")
                    return 0
                else:
                    print_error(f"Unknown command: {cmd}")

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
            print_info("\nExiting...")
            return 0
        except Exception as e:
            print_error(f"Error: {e}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
