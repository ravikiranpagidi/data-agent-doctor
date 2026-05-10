from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable, Pattern


IGNORED_DIRECTORIES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "venv",
}

TEXT_EXTENSIONS = {
    ".cfg",
    ".conf",
    ".ini",
    ".ipynb",
    ".json",
    ".md",
    ".py",
    ".sql",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}


@dataclass(frozen=True)
class ProjectFile:
    path: str
    absolute_path: Path
    name: str
    suffix: str


@dataclass(frozen=True)
class GrepMatch:
    path: str
    line: int
    text: str


class ScanContext:
    def __init__(self, cwd: Path, config: dict):
        self.cwd = cwd
        self.config = config
        self.ignore_paths = tuple(config.get("ignore_paths", []))
        self.files = self._walk(max_files=int(config.get("max_files", 3000)))

    def file_exists(self, relative_path: str) -> bool:
        return (self.cwd / relative_path).exists()

    def read_text(self, relative_path: str) -> str:
        return (self.cwd / relative_path).read_text(encoding="utf-8")

    def read_json(self, relative_path: str) -> dict:
        return json.loads(self.read_text(relative_path))

    def find_files(self, predicate: Callable[[ProjectFile], bool]) -> list[ProjectFile]:
        return [file for file in self.files if predicate(file)]

    def grep(
        self,
        pattern: str | Pattern[str],
        *,
        extensions: Iterable[str] | None = None,
        include_tests: bool = True,
    ) -> list[GrepMatch]:
        compiled = re.compile(pattern, re.IGNORECASE) if isinstance(pattern, str) else pattern
        allowed_extensions = set(extensions or TEXT_EXTENSIONS)
        matches: list[GrepMatch] = []

        for file in self.files:
            if file.suffix not in allowed_extensions:
                continue
            if not include_tests and _is_non_production_path(file.path):
                continue
            try:
                content = file.absolute_path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue

            for index, line in enumerate(content.splitlines(), start=1):
                if compiled.search(line):
                    matches.append(GrepMatch(path=file.path, line=index, text=line.strip()))

        return matches

    def _walk(self, *, max_files: int) -> list[ProjectFile]:
        files: list[ProjectFile] = []
        for path in self.cwd.rglob("*"):
            if len(files) >= max_files:
                break
            if any(part in IGNORED_DIRECTORIES for part in path.parts):
                continue
            relative = path.relative_to(self.cwd).as_posix()
            if self.ignore_paths and relative.startswith(self.ignore_paths):
                continue
            if not path.is_file():
                continue

            files.append(
                ProjectFile(
                    path=relative,
                    absolute_path=path,
                    name=path.name,
                    suffix=path.suffix.lower(),
                )
            )
        return files


def _is_non_production_path(path: str) -> bool:
    lowered = path.lower()
    return (
        lowered.startswith("tests/")
        or lowered.startswith("test/")
        or "/tests/" in lowered
        or lowered.startswith("examples/")
        or lowered.startswith("docs/")
        or lowered.endswith("_test.py")
        or ".test." in lowered
    )
