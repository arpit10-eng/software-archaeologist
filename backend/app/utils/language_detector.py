import os


def detect_language(files):

    extension_map = {
        ".py": "Python",
        ".java": "Java",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".cpp": "C++",
        ".c": "C",
        ".go": "Go",
        ".rs": "Rust",
        ".html": "HTML",
        ".css": "CSS"
    }

    language_count = {}

    for file in files:

        extension = os.path.splitext(file)[1]

        if extension in extension_map:

            language = extension_map[extension]

            language_count[language] = language_count.get(language, 0) + 1

    if not language_count:
        return {
            "primary_language": "Unknown",
            "languages": {}
        }

    primary_language = max(
        language_count,
        key=language_count.get
    )

    return {
        "primary_language": primary_language,
        "languages": language_count
    }