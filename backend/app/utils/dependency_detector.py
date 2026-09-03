import json
import os
import re

try:
    import tomllib
except ModuleNotFoundError:
    tomllib = None


def _read_lines(path):
    """
    Safely read a text file line-by-line.
    """

    try:
        with open(
            path,
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as file:

            return [
                line.strip()
                for line in file
            ]

    except OSError:
        return []


def _extract_package_name(value):
    """
    Extract a package name from a dependency declaration.

    Examples:

        fastapi==0.100.0 -> fastapi
        requests>=2.0   -> requests
        numpy~=1.26     -> numpy
    """

    value = str(value).strip()

    if not value:
        return None

    value = value.lstrip("- ")

    match = re.match(
        r"^([A-Za-z0-9_.-]+)",
        value
    )

    if match:
        return match.group(1)

    return None


def detect_dependencies(repo_path, files):
    """
    Detect dependencies from common package-manager files.

    Supported:

        requirements.txt
        package.json
        pyproject.toml
        go.mod
    """

    dependencies = []
    seen = set()

    def add(value):

        if value is None:
            return

        value = str(value).strip()

        if not value:
            return

        if value not in seen:

            seen.add(value)
            dependencies.append(value)

    for file in files:

        lower = file.lower()

        path = os.path.join(
            repo_path,
            file
        )

        # -----------------------------------------------------
        # Python: requirements.txt
        # -----------------------------------------------------

        if lower.endswith("requirements.txt"):

            for line in _read_lines(path):

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                if line.startswith((
                    "-r ",
                    "--requirement",
                    "-c ",
                    "--constraint",
                )):
                    continue

                package = _extract_package_name(
                    line
                )

                add(package)

        # -----------------------------------------------------
        # JavaScript / TypeScript: package.json
        # -----------------------------------------------------

        elif lower.endswith("package.json"):

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8",
                    errors="ignore",
                ) as file_handle:

                    data = json.load(
                        file_handle
                    )

                sections = (
                    "dependencies",
                    "devDependencies",
                    "peerDependencies",
                    "optionalDependencies",
                )

                for section in sections:

                    section_data = (
                        data.get(section)
                        or {}
                    )

                    if isinstance(
                        section_data,
                        dict,
                    ):

                        for name in section_data:
                            add(name)

            except (
                OSError,
                ValueError,
                TypeError,
            ):
                pass

        # -----------------------------------------------------
        # Python: pyproject.toml
        # -----------------------------------------------------

        elif lower.endswith("pyproject.toml"):

            if tomllib is None:
                continue

            try:

                with open(
                    path,
                    "rb",
                ) as file_handle:

                    data = tomllib.load(
                        file_handle
                    )

                # PEP 621 project dependencies.
                project = data.get(
                    "project",
                    {}
                )

                if isinstance(
                    project,
                    dict,
                ):

                    for dependency in (
                        project.get(
                            "dependencies",
                            []
                        )
                        or []
                    ):

                        package = (
                            _extract_package_name(
                                dependency
                            )
                        )

                        add(package)

                # Poetry dependencies.
                poetry = (
                    data
                    .get("tool", {})
                    .get("poetry", {})
                )

                if isinstance(
                    poetry,
                    dict,
                ):

                    poetry_dependencies = (
                        poetry.get(
                            "dependencies",
                            {}
                        )
                        or {}
                    )

                    if isinstance(
                        poetry_dependencies,
                        dict,
                    ):

                        for name in poetry_dependencies:

                            if name.lower() != "python":
                                add(name)

            except (
                OSError,
                ValueError,
                TypeError,
            ):
                pass

        # -----------------------------------------------------
        # Go: go.mod
        # -----------------------------------------------------

        elif lower.endswith("go.mod"):

            lines = _read_lines(path)

            inside_require_block = False

            for line in lines:

                if line.startswith("require ("):

                    inside_require_block = True
                    continue

                if inside_require_block:

                    if line == ")":

                        inside_require_block = False
                        continue

                    if line.startswith("//"):
                        continue

                    parts = line.split()

                    if parts:
                        add(parts[0])

                    continue

                if line.startswith("require "):

                    parts = line.split()

                    if len(parts) >= 2:
                        add(parts[1])

    return dependencies