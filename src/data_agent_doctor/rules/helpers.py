from __future__ import annotations

from data_agent_doctor.context import ScanContext


SOURCE_EXTENSIONS = {".py", ".sql", ".yaml", ".yml", ".json", ".toml", ".md"}
CODE_CONFIG_EXTENSIONS = {".py", ".sql", ".yaml", ".yml", ".json", ".toml"}


def has_any_text(context: ScanContext, patterns: list[str], *, include_tests: bool = True) -> bool:
    return any(
        context.grep(pattern, extensions=SOURCE_EXTENSIONS, include_tests=include_tests)
        for pattern in patterns
    )


def first_match_path(context: ScanContext, patterns: list[str], *, include_tests: bool = True) -> str | None:
    for pattern in patterns:
        matches = context.grep(pattern, extensions=SOURCE_EXTENSIONS, include_tests=include_tests)
        if matches:
            match = matches[0]
            return f"{match.path}:{match.line}"
    return None


def has_file(context: ScanContext, *paths: str) -> bool:
    file_paths = {file.path for file in context.files}
    return any(path in file_paths for path in paths)


def has_directory(context: ScanContext, directory: str) -> bool:
    prefix = directory.rstrip("/") + "/"
    return any(file.path.startswith(prefix) for file in context.files)
