from pathlib import Path

from app.services.file_services import (
    scan_repository,
)


def test_scan_repository_counts_python_files(
    tmp_path: Path,
):
    project = tmp_path / "project"

    project.mkdir()

    python_file = project / "main.py"

    python_file.write_text(
        "print('hello')\n"
        "print('world')\n",
        encoding="utf-8",
    )

    result = scan_repository(
        str(project)
    )

    assert result["total_python_files"] == 1
    assert result["total_lines"] == 2


def test_scan_repository_ignores_virtual_environment(
    tmp_path: Path,
):
    project = tmp_path / "project"

    project.mkdir()

    main_file = project / "main.py"

    main_file.write_text(
        "print('hello')\n",
        encoding="utf-8",
    )

    venv = project / "venv"

    venv.mkdir()

    ignored_file = venv / "ignored.py"

    ignored_file.write_text(
        "print('ignored')\n",
        encoding="utf-8",
    )

    result = scan_repository(
        str(project)
    )

    assert result["total_python_files"] == 1

    paths = result["files"]

    assert "main.py" in paths

    assert not any(
        "venv" in path
        for path in paths
    )


def test_scan_repository_returns_file_metadata(
    tmp_path: Path,
):
    project = tmp_path / "project"

    project.mkdir()

    source_file = project / "app.py"

    source_file.write_text(
        "def hello():\n"
        "    return 'hello'\n",
        encoding="utf-8",
    )

    result = scan_repository(
        str(project)
    )

    assert "file_metadata" in result

    assert len(
        result["file_metadata"]
    ) == 1

    metadata = result[
        "file_metadata"
    ][0]

    assert metadata["path"] == "app.py"
    assert metadata["language"] == "Python"
    assert metadata["lines"] == 2
    assert metadata["size_bytes"] > 0