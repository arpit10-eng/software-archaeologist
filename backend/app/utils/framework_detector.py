import os


SUPPORTED_SOURCE_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".java",
    ".php",
}


def _safe_read(path):
    """
    Safely read a source file.
    """

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            return file.read().lower()

    except OSError:
        return ""


def detect_framework(repo_path, files):
    """
    Detect the most likely framework used by a repository.

    Detection uses source-code markers and framework-specific
    configuration files.
    """

    names = {
        os.path.basename(file).lower()
        for file in files
    }

    source_files = [
        file
        for file in files
        if os.path.splitext(file)[1].lower()
        in SUPPORTED_SOURCE_EXTENSIONS
    ]

    content_parts = []

    for file in source_files:

        content = _safe_read(
            os.path.join(
                repo_path,
                file
            )
        )

        if content:
            content_parts.append(content)

    content = "\n".join(
        content_parts
    )

    # =========================================================
    # Python
    # =========================================================

    if (
        "from fastapi" in content
        or "import fastapi" in content
        or "fastapi(" in content
    ):
        return "FastAPI"

    if (
        "from django" in content
        or "import django" in content
        or "django.conf" in content
    ):
        return "Django"

    if (
        "from flask" in content
        or "import flask" in content
        or "flask(" in content
    ):
        return "Flask"

    # =========================================================
    # JavaScript / TypeScript
    # =========================================================

    if (
        "next.config.js" in names
        or "next.config.mjs" in names
        or "next.config.ts" in names
    ):
        return "Next.js"

    if (
        "from 'next/" in content
        or 'from "next/' in content
        or "require('next')" in content
        or 'require("next")' in content
    ):
        return "Next.js"

    if (
        "from 'react'" in content
        or 'from "react"' in content
        or "from 'react/" in content
        or 'from "react/' in content
    ):
        return "React"

    if (
        "require('react')" in content
        or 'require("react")' in content
    ):
        return "React"

    if (
        "from 'express'" in content
        or 'from "express"' in content
        or "require('express')" in content
        or 'require("express")' in content
    ):
        return "Express"

    # =========================================================
    # Java
    # =========================================================

    if (
        "org.springframework" in content
        or "springframework" in content
    ):
        return "Spring"

    # =========================================================
    # PHP
    # =========================================================

    if (
        "illuminate\\" in content
        or "laravel" in content
    ):
        return "Laravel"

    return "Unknown"