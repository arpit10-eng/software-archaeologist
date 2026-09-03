import os


IGNORED_DIRECTORIES = {
    ".git",
    "__pycache__",
    "venv",
    ".venv",
    "env",
    ".env",
    "node_modules",
    "dist",
    "build",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "coverage",
    "htmlcov",
    ".next",
    "target",
}


TEXT_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
    ".go",
    ".rs",
    ".rb",
    ".php",
    ".cs",
    ".swift",
    ".kt",
    ".kts",
    ".md",
    ".txt",
    ".json",
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".css",
    ".html",
    ".xml",
    ".sql",
    ".sh",
}


LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".c": "C",
    ".cpp": "C++",
    ".h": "C/C++",
    ".hpp": "C++",
    ".go": "Go",
    ".rs": "Rust",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".swift": "Swift",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".md": "Markdown",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".css": "CSS",
    ".html": "HTML",
    ".xml": "XML",
    ".sql": "SQL",
    ".sh": "Shell",
}


def get_file_extension(filename):
    return os.path.splitext(filename)[1].lower()


def _line_count(path):
    try:
        with open(
            path,
            "rb",
        ) as file:
            return sum(
                1
                for _ in file
            )
    except (
        OSError,
        UnicodeDecodeError,
    ):
        return 0


def scan_repository(repo_path):
    files = []
    file_metadata = []

    total_lines = 0
    largest_file = None
    largest_file_lines = 0
    total_size_bytes = 0

    language_file_counts = {}

    for root, directories, filenames in os.walk(repo_path):

        directories[:] = [
            directory
            for directory in directories
            if directory not in IGNORED_DIRECTORIES
        ]

        for filename in filenames:

            full_path = os.path.join(
                root,
                filename,
            )

            relative_path = os.path.relpath(
                full_path,
                repo_path,
            )

            relative_path = relative_path.replace(
                os.sep,
                "/",
            )

            extension = get_file_extension(
                filename
            )

            language = LANGUAGE_BY_EXTENSION.get(
                extension
            )

            try:
                size_bytes = os.path.getsize(
                    full_path
                )
            except OSError:
                size_bytes = 0

            lines = 0

            if extension in TEXT_EXTENSIONS:
                lines = _line_count(
                    full_path
                )

                total_lines += lines

            total_size_bytes += size_bytes

            files.append(
                relative_path
            )

            file_metadata.append(
                {
                    "path": relative_path,
                    "extension": extension,
                    "language": language or "Unknown",
                    "size_bytes": size_bytes,
                    "lines": lines,
                }
            )

            if language:
                language_file_counts[language] = (
                    language_file_counts.get(
                        language,
                        0,
                    )
                    + 1
                )

            if lines > largest_file_lines:
                largest_file_lines = lines
                largest_file = relative_path

    files.sort()

    file_metadata.sort(
        key=lambda item: item["path"]
    )

    total_python_files = language_file_counts.get(
        "Python",
        0,
    )

    total_javascript_files = language_file_counts.get(
        "JavaScript",
        0,
    )

    total_java_files = language_file_counts.get(
        "Java",
        0,
    )

    return {
        # -----------------------------------------------------
        # Existing / legacy metrics
        # -----------------------------------------------------

        "total_files": len(files),
        "total_python_files": total_python_files,
        "total_javascript_files": total_javascript_files,
        "total_java_files": total_java_files,
        "total_lines": total_lines,
        "largest_file": largest_file,
        "largest_file_lines": largest_file_lines,
        "total_size_bytes": total_size_bytes,

        # -----------------------------------------------------
        # Language metrics
        # -----------------------------------------------------

        "language_file_counts": language_file_counts,

        # -----------------------------------------------------
        # Phase 2 file analysis
        # -----------------------------------------------------

        "files": files,
        "file_metadata": file_metadata,
    }