import os


EXTENSION_MAP = {
    ".py": "Python",

    ".java": "Java",

    ".js": "JavaScript",
    ".jsx": "JavaScript",

    ".ts": "TypeScript",
    ".tsx": "TypeScript",

    ".cpp": "C++",
    ".cc": "C++",
    ".cxx": "C++",

    ".c": "C",

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

    ".scala": "Scala",

    ".dart": "Dart",

    ".r": "R",

    ".lua": "Lua",

    ".html": "HTML",
    ".htm": "HTML",

    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "Sass",
    ".less": "Less",

    ".sql": "SQL",

    ".sh": "Shell",
    ".bash": "Shell",
    ".zsh": "Shell",

    ".ps1": "PowerShell",
}


def detect_language(files):
    """
    Detect programming languages used in a repository.

    Detection is based on file extensions.
    """

    language_count = {}

    for file in files:

        extension = os.path.splitext(
            file
        )[1].lower()

        language = EXTENSION_MAP.get(
            extension
        )

        if language is None:
            continue

        language_count[language] = (
            language_count.get(language, 0) + 1
        )

    if not language_count:

        return {
            "primary_language": "Unknown",
            "languages": {},
        }

    primary_language = max(
        language_count,
        key=language_count.get
    )

    languages = dict(
        sorted(
            language_count.items(),
            key=lambda item: item[1],
            reverse=True,
        )
    )

    return {
        "primary_language": primary_language,
        "languages": languages,
    }