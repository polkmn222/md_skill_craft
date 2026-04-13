"""Mode 2: Project analysis and configuration file validation."""

from pathlib import Path
from typing import Optional, Dict, List
import os

from md_skill_craft.config.settings import settings, usage_tracker
from md_skill_craft.config.keystore import KeyStore
from md_skill_craft.config.localization import get_string as t
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


# Directories to ignore during file scanning
IGNORED_DIRS = {
    "node_modules", "__pycache__", ".git", ".venv", "venv",
    ".next", "dist", "build", ".pytest_cache", ".mypy_cache",
    "target", "bin", ".cargo", ".env", ".egg-info", ".tox",
    "htmlcov", ".coverage", ".env.local", ".DS_Store",
}

# Key project files to look for
KEY_FILES = {
    "README.md", "pyproject.toml", "package.json", "Dockerfile",
    "docker-compose.yml", "go.mod", "Cargo.toml", "pom.xml",
    ".gitignore", "Makefile", "requirements.txt",
}


class Mode2Analysis:
    """Analyze projects and validate/improve configuration files."""

    def __init__(self) -> None:
        """Initialize Mode 2 analyzer."""
        self.llm_provider = settings.llm
        self.llm_model = settings.llm_model
        self.language = settings.language or "ko"
        self.active_mode = settings.active_mode if settings.mode == 2 else False
        self.analysis_results: Optional[str] = None

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
            key = os.getenv(env_var)
            if key:
                return key

        raise ValueError(f"No API key found for {self.llm_provider}")

    def _scan_directory(self, root_path: Path, depth: str) -> Dict[str, List[str]]:
        """Scan project directory structure.

        Args:
            root_path: Root directory to scan
            depth: Analysis depth (fast, standard, deep)

        Returns:
            Dictionary with project structure info
        """
        result = {
            "key_files": [],
            "source_dirs": [],
            "all_files": [],
        }

        # Fast mode: only key files
        if depth == "fast":
            for file in root_path.iterdir():
                if file.is_file() and file.name in KEY_FILES:
                    result["key_files"].append(file.name)
            return result

        # Standard and deep modes: scan directories
        for item in root_path.rglob("*"):
            # Skip ignored directories
            if any(ignored in item.parts for ignored in IGNORED_DIRS):
                continue

            if item.is_file():
                # Collect key files
                if item.name in KEY_FILES:
                    result["key_files"].append(str(item.relative_to(root_path)))

                # Collect source files for standard mode
                if depth == "standard":
                    if item.parent == root_path or str(item.relative_to(root_path)).count(os.sep) == 0:
                        if item.suffix in {".py", ".js", ".go", ".rs", ".java", ".rb"}:
                            result["source_dirs"].append(str(item.relative_to(root_path)))

            elif item.is_dir() and len(result["all_files"]) < 50:
                # Collect directory structure for deep mode
                if depth == "deep":
                    result["all_files"].append(str(item.relative_to(root_path)) + "/")

        return result

    def _read_existing_config(self, root_path: Path) -> Optional[str]:
        """Read existing configuration file if present.

        Args:
            root_path: Root directory to scan

        Returns:
            Configuration file content or None
        """
        file_type = self._get_file_type()
        config_file = root_path / f"{file_type}.md"

        if config_file.exists():
            try:
                return config_file.read_text(encoding="utf-8")
            except Exception:
                return None

        return None

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

    def select_analysis_depth(self) -> str:
        """Let user select analysis depth.

        Returns:
            Analysis depth (fast, standard, deep)
        """
        print_section("Select Analysis Depth")

        choice = Menu.select(
            t("analysis.select_depth", self.language),
            options=[
                (1, t("analysis.depth_fast", self.language), t("analysis.depth_fast_desc", self.language)),
                (2, t("analysis.depth_standard", self.language), t("analysis.depth_standard_desc", self.language)),
                (3, t("analysis.depth_deep", self.language), t("analysis.depth_deep_desc", self.language)),
            ],
        )

        depth_map = {1: "fast", 2: "standard", 3: "deep"}
        return depth_map[choice]

    def analyze_with_llm(self, root_path: Path, project_info: str, existing_config: Optional[str]) -> str:
        """Analyze project using LLM.

        Args:
            root_path: Root directory path
            project_info: Scanned project structure
            existing_config: Existing configuration file content

        Returns:
            Analysis results and suggestions
        """
        from md_skill_craft.core.base_provider import LLMConfig

        try:
            api_key = self.get_api_key()
            provider = ProviderFactory.create(self.llm_provider, api_key)

            # Build system prompt
            system_prompt = self._build_system_prompt()

            # Build user message
            user_message = self._build_user_message(
                root_path.name,
                project_info,
                existing_config,
            )

            progress_desc = (
                "Analyzing project..."
            )

            with progress_bar(progress_desc) as (progress, task_id):
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

                progress.update(task_id, advance=100)

                self.analysis_results = response.text
                return response.text

        except ValueError as e:
            print_error(str(e))
            return ""
        except Exception as e:
            print_error(f"Analysis error: {e}")
            return ""

    def _build_system_prompt(self) -> str:
        """Build system prompt for LLM analysis.

        Returns:
            System prompt string
        """
        if self.language == "ko":
            return """당신은 프로젝트 구조 분석 전문가입니다.

사용자의 프로젝트를 분석하고 다음을 평가해주세요:
1. 기존 CLAUDE.md/AGENT.md/GEMINI.md 파일의 정확성
2. 누락된 정보 (Key Commands, Architecture 등)
3. 실제 프로젝트 구조와의 불일치
4. 개선 권고사항

출력 형식:
## 발견된 문제
- ⚠️ [문제 설명]
- ✅ [잘된 부분]

## 권고사항
- [개선사항 1]
- [개선사항 2]

## 개선된 설정 파일
[전체 CLAUDE.md/AGENT.md/GEMINI.md 내용]

정확하고 실용적인 분석만 제공하세요."""
        else:
            return """You are a project structure analysis expert.

Analyze the user's project and evaluate:
1. Accuracy of existing CLAUDE.md/AGENT.md/GEMINI.md file
2. Missing information (Key Commands, Architecture, etc.)
3. Mismatch between actual structure and documented structure
4. Recommendations for improvement

Output format:
## Issues Found
- ⚠️ [Issue description]
- ✅ [What's good]

## Recommendations
- [Improvement 1]
- [Improvement 2]

## Improved Configuration File
[Complete CLAUDE.md/AGENT.md/GEMINI.md content]

Provide only accurate, practical analysis."""

    def _build_user_message(
        self,
        project_name: str,
        project_info: str,
        existing_config: Optional[str],
    ) -> str:
        """Build user message for LLM analysis.

        Args:
            project_name: Project directory name
            project_info: Scanned project structure
            existing_config: Existing configuration file

        Returns:
            User message string
        """
        if self.language == "ko":
            config_section = f"""## 기존 설정 파일
```
{existing_config}
```""" if existing_config else "기존 설정 파일이 없습니다."

            return f"""프로젝트: {project_name}

## 프로젝트 구조
```
{project_info}
```

{config_section}

이 프로젝트를 분석하고 설정 파일을 검증해주세요.
마크다운 형식으로 분석 결과를 출력하세요."""
        else:
            config_section = f"""## Existing Configuration File
```
{existing_config}
```""" if existing_config else "No existing configuration file."

            return f"""Project: {project_name}

## Project Structure
```
{project_info}
```

{config_section}

Analyze this project and validate the configuration file.
Output analysis results in markdown format."""

    def save_analysis(self, root_path: Path) -> bool:
        """Save analysis results to .suggested file.

        Args:
            root_path: Root directory to save to

        Returns:
            True if saved successfully
        """
        if not self.analysis_results:
            return False

        file_type = self._get_file_type()
        filename = f"{file_type}.md.suggested"
        filepath = root_path / filename

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.analysis_results)

            print_success(t("analysis.file_saved", self.language, filename=filename))
            return True

        except Exception as e:
            print_error(f"Save failed: {e}")
            return False

    def show_results(self) -> None:
        """Display analysis results."""
        if not self.analysis_results:
            print_error(t("analysis.no_results", self.language))
            return

        print_section("Analysis Results")
        print_code_block(self.analysis_results, "md")

    def run(self, root_path: Optional[Path] = None) -> bool:
        """Run Mode 2 workflow.

        Args:
            root_path: Optional project root directory

        Returns:
            True if completed successfully
        """
        if root_path is None:
            root_path = Path.cwd()

        print_header(
            "Mode 2: Project Analysis"
        )

        # Step 1: Select analysis depth
        depth = self.select_analysis_depth()

        # Step 2: Scan directory
        print_info(t("analysis.scanning", self.language, root=root_path.name))
        project_info = self._scan_directory(root_path, depth)
        project_info_str = "\n".join(
            project_info.get("key_files", []) +
            project_info.get("source_dirs", []) +
            project_info.get("all_files", [])
        )

        if not project_info_str:
            print_error(t("analysis.no_info_found", self.language))
            return False

        # Step 3: Read existing config
        existing_config = self._read_existing_config(root_path)

        # Step 4: Analyze with LLM
        print_info(t("analysis.analyzing", self.language))
        results = self.analyze_with_llm(root_path, project_info_str, existing_config)
        if not results:
            return False

        # Step 5: Show results
        self.show_results()

        # Step 6: Ask what to do
        if self.active_mode:
            # Active mode: ask for confirmation
            choice = Menu.select(
                t("analysis.update_config", self.language),
                options=[
                    (1, t("misc.yes", self.language)),
                    (2, t("misc.no", self.language)),
                ],
            )
            if choice == 1:
                file_type = self._get_file_type()
                # TODO: Extract and save improved config from analysis results
                print_info(t("analysis.config_updated", self.language))
                return True
            else:
                return False
        else:
            # Passive mode: show save options
            choice = Menu.select(
                t("analysis.what_to_do", self.language),
                options=[
                    (1, t("analysis.save_as_suggested", self.language, file_type=self._get_file_type())),
                    (2, t("analysis.terminal_output_only", self.language)),
                    (3, t("analysis.skip", self.language)),
                ],
            )

            if choice == 1:
                return self.save_analysis(root_path)
            elif choice == 2:
                return True
            else:
                return False
