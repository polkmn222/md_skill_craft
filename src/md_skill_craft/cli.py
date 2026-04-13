"""Main CLI entry point and REPL loop."""

import sys
import os
from pathlib import Path
from typing import Optional

from md_skill_craft.config.settings import settings, usage_tracker
from md_skill_craft.config.keystore import KeyStore
from md_skill_craft.config.localization import get_string as t
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
                (1, "Use stored key"),
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
    print_section(t("section.language_select", "en"))
    lang_choice = Menu.select(
        t("prompt.select_language", "en"),
        options=[
            (1, "Korean"),
            (2, "English"),
        ],
    )
    settings.language = "ko" if lang_choice == 1 else "en"
    lang = settings.language

    # Step 2: LLM Provider
    print_section(t("section.llm_select", lang))
    llm_choice = Menu.select(
        t("prompt.select_llm", lang),
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
    print_section(t("section.api_key", lang))
    api_key = get_api_key(selected_llm, use_env=True)
    settings.use_env_var = True  # Remember user prefers env vars

    # Get default model for this LLM
    provider = ProviderFactory.create(selected_llm, api_key)
    default_model = provider.available_models[0] if provider.available_models else "unknown"
    settings.llm_model = default_model

    # Step 4: Mode
    print_section(t("section.select_mode", lang))
    mode_choice = Menu.select(
        t("prompt.select_mode_purpose", lang),
        options=[
            (1, t("mode.generate_guide", lang), t("mode.generate_guide_description", lang)),
            (2, t("mode.analyze_project", lang), t("mode.analyze_project_description", lang)),
        ],
    )
    settings.mode = mode_choice

    # Step 4-B: Mode 2 additional question
    if mode_choice == 2:
        print_section(t("section.intervention_method", lang))
        active_choice = Menu.select(
            t("prompt.select_intervention", lang),
            options=[
                (1, t("intervention.active", lang), t("intervention.active_description", lang)),
                (2, t("intervention.passive", lang), t("intervention.passive_description", lang)),
            ],
        )
        settings.active_mode = active_choice == 1

    # Save settings
    settings.save()
    print_success(t("success.settings_saved", lang))


def show_help() -> None:
    """Show help information."""
    lang = settings.language or "en"
    print_header("md-skill-craft Help")

    print_section("Built-in Commands")
    print_option(1, "/help", t("help.help_command", lang))
    print_option(2, "/setup", t("help.setup_command", lang))
    print_option(3, "/cost", t("help.cost_command", lang))
    print_option(4, "/mode", t("help.mode_command", lang))
    print_option(5, "/exit", t("help.exit_command", lang))

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
    lang = settings.language or "en"

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
            input_cost = cost * input_tokens / (input_tokens + output_tokens + 1)
            output_cost = cost * output_tokens / (input_tokens + output_tokens + 1)
            input_label = "입력" if lang == "ko" else "Input"
            output_label = "출력" if lang == "ko" else "Output"
            subtotal_label = "소계" if lang == "ko" else "Subtotal"
            print_info(f"  {input_label}: {input_tokens:,} tokens → ${input_cost:.3f}")
            print_info(f"  {output_label}: {output_tokens:,} tokens → ${output_cost:.3f}")
            print_info(f"  {subtotal_label}: ${cost:.3f}")
            print_info("")

    print_section("Total" if lang == "en" else "총합")
    print_info(f"Total cost: ${total_cost:.3f}")
    print_info("[dim][Prices as of April 2025, actual billing may vary][/dim]")


def show_setup() -> None:
    """Show setup menu to change settings."""
    lang = settings.language or "en"
    print_header("Settings")

    mode2_desc = t("menu.mode2_only", lang) if settings.mode == 2 else ""
    choice = Menu.select(
        t("menu.select_to_change", lang),
        options=[
            (1, t("menu.option_language", lang)),
            (2, t("menu.option_llm", lang)),
            (3, t("menu.option_mode", lang)),
            (4, t("menu.option_intervention", lang), mode2_desc),
            (5, t("menu.back", lang)),
        ],
    )

    if choice == 1:
        lang_choice = Menu.select(
            t("prompt.change_language", lang),
            options=[
                (1, "Korean"),
                (2, "English"),
            ],
        )
        settings.language = "ko" if lang_choice == 1 else "en"
        new_lang = settings.language
        print_success(t("success.language_changed", new_lang))

    elif choice == 2:
        llm_choice = Menu.select(
            t("prompt.change_llm", lang),
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
        print_success(t("success.llm_changed", lang))

    elif choice == 3:
        mode_choice = Menu.select(
            t("prompt.change_mode", lang),
            options=[
                (1, t("mode.generate_guide", lang)),
                (2, t("mode.analyze_project", lang)),
            ],
        )
        settings.mode = mode_choice
        print_success(t("success.mode_changed", lang))

    elif choice == 4 and settings.mode == 2:
        active_choice = Menu.select(
            t("prompt.change_intervention", lang),
            options=[
                (1, t("intervention.active", lang)),
                (2, t("intervention.passive", lang)),
            ],
        )
        settings.active_mode = active_choice == 1
        print_success(t("success.intervention_changed", lang))

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
    lang = settings.language or "en"
    print_header(f"md-skill-craft v0.1.0", f"LLM: {settings.llm.upper()} | Mode: {settings.mode}")
    print_info(t("repl.mode_info", lang))

    while True:
        try:
            # Show prompt
            user_input = input("\nmd-skill-craft > ").strip()

            # Handle empty input
            if not user_input:
                print_info(t("misc.press_enter", lang))
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
                        t("prompt.change_mode", lang),
                        options=[
                            (1, t("mode.generate_guide", lang)),
                            (2, t("mode.analyze_project", lang)),
                        ],
                    )
                    settings.mode = new_mode
                    settings.save()
                    print_success(t("success.mode_changed", lang))
                elif cmd == "exit":
                    print_info(t("repl.exiting", lang))
                    return 0
                else:
                    print_error(t("repl.unknown_command", lang, cmd=cmd))

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
