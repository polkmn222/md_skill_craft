"""Mode 1: Interactive LLM-based project configuration file generation."""

from pathlib import Path
from typing import Optional

from md_skill_craft.config.settings import settings, usage_tracker
from md_skill_craft.config.keystore import KeyStore
from md_skill_craft.core.provider_factory import ProviderFactory
from md_skill_craft.ui.formatter import (
    print_header,
    print_section,
    print_success,
    print_error,
    print_info,
    print_code_block,
)
from md_skill_craft.ui.menu import Menu
from md_skill_craft.ui.progress import progress_bar


class Mode1Guide:
    """Generate project configuration files through LLM conversation."""

    def __init__(self) -> None:
        """Initialize Mode 1 guide generator."""
        self.llm_provider = settings.llm
        self.llm_model = settings.llm_model
        self.language = settings.language or "ko"
        self.generated_content: Optional[str] = None

    def get_api_key(self) -> str:
        """Get API key for configured LLM provider.

        Returns:
            API key string

        Raises:
            ValueError: If no API key available
        """
        # Try keystore first
        key = KeyStore.get(self.llm_provider)
        if key:
            return key

        # Try environment variable
        env_map = {
            "claude": "ANTHROPIC_API_KEY",
            "gpt": "OPENAI_API_KEY",
            "gemini": "GOOGLE_API_KEY",
        }
        env_var = env_map.get(self.llm_provider)
        if env_var:
            import os
            key = os.getenv(env_var)
            if key:
                return key

        raise ValueError(f"No API key found for {self.llm_provider}")

    def collect_project_info(self) -> str:
        """Collect project information through user input.

        Returns:
            Project description string
        """
        print_section("프로젝트 정보 수집" if self.language == "ko" else "Collect Project Information")

        prompt_text = (
            "프로젝트에 대해 설명해주세요:\n"
            "[언어, 프레임워크, 목적 등을 자유롭게 입력하세요]"
            if self.language == "ko"
            else "Describe your project:\n"
            "[Language, framework, purpose, etc.]"
        )

        description = Menu.prompt(prompt_text)
        return description

    def generate_with_llm(self, project_description: str) -> str:
        """Generate configuration file through LLM conversation.

        Args:
            project_description: User's project description

        Returns:
            Generated configuration file content
        """
        from md_skill_craft.core.base_provider import LLMConfig

        try:
            api_key = self.get_api_key()

            # Create provider
            provider = ProviderFactory.create(self.llm_provider, api_key)

            # Build system prompt based on LLM type
            file_type = self._get_file_type()
            system_prompt = self._build_system_prompt(file_type)

            # Build user message
            user_message = self._build_user_message(project_description, file_type)

            # Show progress
            progress_desc = (
                f"{file_type}.md 생성 중..." if self.language == "ko" else f"Generating {file_type}.md..."
            )

            with progress_bar(progress_desc) as (progress, task_id):
                # Call LLM
                config = LLMConfig(
                    model=self.llm_model,
                    system_prompt=system_prompt,
                    temperature=0.7,
                )

                response = provider.generate(user_message, config)

                # Track usage
                usage_tracker.add(
                    self.llm_provider,
                    response.input_tokens,
                    response.output_tokens,
                )
                usage_tracker.save()

                # Update progress
                progress.update(task_id, advance=100)

                self.generated_content = response.text
                return response.text

        except ValueError as e:
            print_error(str(e))
            return ""
        except Exception as e:
            print_error(f"LLM 생성 오류: {e}" if self.language == "ko" else f"LLM generation error: {e}")
            return ""

    def _get_file_type(self) -> str:
        """Get configuration file type based on LLM.

        Returns:
            File type (CLAUDE, AGENT, or GEMINI)
        """
        file_map = {
            "claude": "CLAUDE",
            "gpt": "AGENT",
            "gemini": "GEMINI",
        }
        return file_map.get(self.llm_provider, "CLAUDE")

    def _get_file_extension(self) -> str:
        """Get file extension with .md.

        Returns:
            File name (e.g., CLAUDE.md)
        """
        return f"{self._get_file_type()}.md"

    def _build_system_prompt(self, file_type: str) -> str:
        """Build system prompt for LLM.

        Args:
            file_type: Configuration file type (CLAUDE, AGENT, GEMINI)

        Returns:
            System prompt string
        """
        if self.language == "ko":
            return f"""당신은 {file_type}.md 설정 파일을 생성하는 전문가입니다.

사용자의 프로젝트 설명을 기반으로 {file_type}.md 파일을 생성해주세요.

출력 형식:
# [프로젝트명]

## Project
[한 줄 설명]
**Stack**: [기술 스택]

## Key Commands
| Task | Command |
|------|---------|
| [명령] | [실행 방법] |

## Architecture
- [구조 설명]

## Conventions
- [규칙들]

## Skills
@skills/coding-standards.md @skills/validation.md

주의사항:
- 정확하고 실용적인 내용만 포함
- 30줄 내외로 간결하게 작성
- 프로젝트에 맞는 실제 명령어 사용"""
        else:
            return f"""You are an expert in generating {file_type}.md configuration files.

Based on the user's project description, generate a {file_type}.md file.

Output format:
# [PROJECT_NAME]

## Project
[One-line description]
**Stack**: [Technology stack]

## Key Commands
| Task | Command |
|------|---------|
| [Task] | [Command] |

## Architecture
- [Architecture description]

## Conventions
- [Rules]

## Skills
@skills/coding-standards.md @skills/validation.md

Notes:
- Include only accurate, practical content
- Keep it concise (~30 lines)
- Use actual commands relevant to the project"""

    def _build_user_message(self, project_description: str, file_type: str) -> str:
        """Build user message for LLM.

        Args:
            project_description: Project description from user
            file_type: Configuration file type

        Returns:
            User message string
        """
        if self.language == "ko":
            return f"""다음 프로젝트에 대한 {file_type}.md 파일을 생성해주세요:

{project_description}

프로젝트 이름과 설명을 기반으로 적절한 {file_type}.md를 생성해주세요.
마크다운 형식으로만 결과를 출력하고, 다른 설명은 포함하지 마세요."""
        else:
            return f"""Generate a {file_type}.md file for this project:

{project_description}

Based on the project name and description, create an appropriate {file_type}.md file.
Output only markdown format, no explanations."""

    def show_output(self) -> None:
        """Display generated content."""
        if not self.generated_content:
            print_error("생성된 파일이 없습니다." if self.language == "ko" else "No generated content")
            return

        print_section("생성된 파일" if self.language == "ko" else "Generated File")
        print_code_block(self.generated_content, self._get_file_extension())

    def save_output(self, output_path: Optional[Path] = None) -> bool:
        """Save generated content to file.

        Args:
            output_path: Optional path to save file. If None, use current directory.

        Returns:
            True if saved successfully
        """
        if not self.generated_content:
            return False

        if output_path is None:
            output_path = Path.cwd()

        filename = self._get_file_extension()
        filepath = output_path / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.generated_content)

            print_success(f"{filename}이(가) {filepath}에 저장되었습니다."
                         if self.language == "ko"
                         else f"{filename} saved to {filepath}")
            return True

        except Exception as e:
            print_error(f"파일 저장 실패: {e}" if self.language == "ko" else f"Failed to save file: {e}")
            return False

    def save_suggested(self, output_path: Optional[Path] = None) -> bool:
        """Save as .suggested file for preview.

        Args:
            output_path: Optional path to save file

        Returns:
            True if saved successfully
        """
        if not self.generated_content:
            return False

        if output_path is None:
            output_path = Path.cwd()

        filename = f"{self._get_file_extension()}.suggested"
        filepath = output_path / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.generated_content)

            print_success(f"{filename}이(가) 저장되었습니다. (미리보기)"
                         if self.language == "ko"
                         else f"{filename} saved (preview)")
            return True

        except Exception as e:
            print_error(f"파일 저장 실패: {e}" if self.language == "ko" else f"Failed to save file: {e}")
            return False

    def run(self, output_path: Optional[Path] = None) -> bool:
        """Run Mode 1 workflow.

        Args:
            output_path: Optional output directory

        Returns:
            True if completed successfully
        """
        print_header(
            "Mode 1: 프로젝트 가이드 생성" if self.language == "ko" else "Mode 1: Generate Project Guide"
        )

        # Step 1: Collect project info
        project_description = self.collect_project_info()
        if not project_description:
            return False

        # Step 2: Generate with LLM
        print_info("LLM과 상호작용 중..." if self.language == "ko" else "Communicating with LLM...")
        content = self.generate_with_llm(project_description)
        if not content:
            return False

        # Step 3: Show output
        self.show_output()

        # Step 4: Ask what to do
        prompt = (
            "어떻게 하시겠어요?" if self.language == "ko" else "What would you like to do?"
        )
        choice = Menu.select(
            prompt,
            options=[
                (1, f"{self._get_file_extension()}로 저장" if self.language == "ko" else f"Save to {self._get_file_extension()}"),
                (2, f"{self._get_file_extension()}.suggested로 저장 (미리보기)" if self.language == "ko" else f"Save as .suggested (preview)"),
                (3, "계속 수정하기" if self.language == "ko" else "Continue editing"),
                (4, "넘기기" if self.language == "ko" else "Skip"),
            ],
        )

        if choice == 1:
            return self.save_output(output_path)
        elif choice == 2:
            return self.save_suggested(output_path)
        elif choice == 3:
            # TODO: Implement editing loop
            print_info("편집 기능은 추후 구현됩니다." if self.language == "ko" else "Editing feature coming soon")
            return False
        else:  # choice == 4
            print_info("건너뛰었습니다." if self.language == "ko" else "Skipped")
            return False
