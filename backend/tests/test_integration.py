import base64
import json
from pathlib import Path
from unittest.mock import patch

import requests
from fastapi.testclient import TestClient

from app.database.database import SessionLocal
from app.database.models import RepositoryAnalysis
from app.main import app


client = TestClient(app)


FAKE_REPOSITORY_URL = (
    "https://github.com/test-user/integration-repo"
)


def create_fake_repository(destination):
    repository_path = Path(destination)

    repository_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    (repository_path / "README.md").write_text(
        "# Integration Test Repository\n\n"
        "This repository is used for integration testing.\n",
        encoding="utf-8",
    )

    (repository_path / "requirements.txt").write_text(
        "fastapi\n"
        "requests\n",
        encoding="utf-8",
    )

    (repository_path / "main.py").write_text(
        "from fastapi import FastAPI\n\n"
        "app = FastAPI()\n\n"
        "@app.get('/')\n"
        "def hello():\n"
        "    return {'message': 'hello'}\n",
        encoding="utf-8",
    )

    return str(repository_path)


def fake_clone_repository(
    repo_url,
    destination,
):
    return create_fake_repository(
        destination
    )


class FakeGitHubResponse:
    status_code = 200

    def json(self):
        return {
            "name": "integration-repo",
            "full_name": "test-user/integration-repo",
            "default_branch": "main",
        }


def fake_requests_get(
    url,
    timeout=10,
):
    return FakeGitHubResponse()


def get_latest_integration_record():
    db = SessionLocal()

    try:
        return (
            db.query(RepositoryAnalysis)
            .filter(
                RepositoryAnalysis.repository
                == FAKE_REPOSITORY_URL
            )
            .order_by(
                RepositoryAnalysis.id.desc()
            )
            .first()
        )

    finally:
        db.close()


def delete_integration_records():
    db = SessionLocal()

    try:
        records = (
            db.query(RepositoryAnalysis)
            .filter(
                RepositoryAnalysis.repository
                == FAKE_REPOSITORY_URL
            )
            .all()
        )

        for record in records:
            db.delete(record)

        db.commit()

    finally:
        db.close()


def test_analyze_repository_complete_flow():
    delete_integration_records()

    with patch(
        "app.services.github_services.clone_repository",
        side_effect=fake_clone_repository,
    ), patch(
        "app.services.github_services.requests.get",
        side_effect=fake_requests_get,
    ):
        response = client.post(
            "/repository/analyze",
            params={
                "repository_url": FAKE_REPOSITORY_URL,
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        dict,
    )

    assert data["status"] == "success"

    assert data["repository"] == (
        FAKE_REPOSITORY_URL
    )

    assert data["branch"] == "main"

    assert "primary_language" in data
    assert "languages" in data
    assert "framework" in data
    assert "dependencies" in data
    assert "architecture" in data

    assert "health_score" in data

    assert "security_issues" in data
    assert "complexity" in data
    assert "code_smells" in data

    assert "ai_recommendations" in data

    assert data["total_files"] >= 3

    delete_integration_records()


def test_analysis_is_saved_to_database():
    delete_integration_records()

    with patch(
        "app.services.github_services.clone_repository",
        side_effect=fake_clone_repository,
    ), patch(
        "app.services.github_services.requests.get",
        side_effect=fake_requests_get,
    ):
        response = client.post(
            "/repository/analyze",
            params={
                "repository_url": FAKE_REPOSITORY_URL,
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert "analysis_id" in data

    analysis_id = data["analysis_id"]

    record = get_latest_integration_record()

    assert record is not None

    assert record.id == analysis_id

    assert record.repository == (
        FAKE_REPOSITORY_URL
    )

    assert record.branch == "main"

    assert record.primary_language is not None

    assert record.created_at is not None

    delete_integration_records()


def test_saved_analysis_json_can_be_restored():
    delete_integration_records()

    with patch(
        "app.services.github_services.clone_repository",
        side_effect=fake_clone_repository,
    ), patch(
        "app.services.github_services.requests.get",
        side_effect=fake_requests_get,
    ):
        response = client.post(
            "/repository/analyze",
            params={
                "repository_url": FAKE_REPOSITORY_URL,
            },
        )

    assert response.status_code == 200

    record = get_latest_integration_record()

    assert record is not None

    restored = json.loads(
        record.analysis_json
    )

    assert isinstance(
        restored,
        dict,
    )

    assert restored["status"] == "success"

    assert restored["repository"] == (
        FAKE_REPOSITORY_URL
    )

    assert "health_score" in restored

    assert "languages" in restored

    assert "code_structure" in restored

    assert "dependency_graph" in restored

    delete_integration_records()


def test_analysis_can_be_retrieved_from_history():
    delete_integration_records()

    with patch(
        "app.services.github_services.clone_repository",
        side_effect=fake_clone_repository,
    ), patch(
        "app.services.github_services.requests.get",
        side_effect=fake_requests_get,
    ):
        response = client.post(
            "/repository/analyze",
            params={
                "repository_url": FAKE_REPOSITORY_URL,
            },
        )

    assert response.status_code == 200

    analysis_id = response.json()[
        "analysis_id"
    ]

    history_response = client.get(
        f"/repository/history/{analysis_id}"
    )

    assert history_response.status_code == 200

    history_data = history_response.json()

    assert history_data["repository"] == (
        FAKE_REPOSITORY_URL
    )

    assert history_data["branch"] == "main"

    assert "health_score" in history_data

    assert "primary_language" in history_data

    delete_integration_records()


def test_analysis_appears_in_history_list():
    delete_integration_records()

    with patch(
        "app.services.github_services.clone_repository",
        side_effect=fake_clone_repository,
    ), patch(
        "app.services.github_services.requests.get",
        side_effect=fake_requests_get,
    ):
        response = client.post(
            "/repository/analyze",
            params={
                "repository_url": FAKE_REPOSITORY_URL,
            },
        )

    assert response.status_code == 200

    history_response = client.get(
        "/repository/history",
        params={
            "repository": FAKE_REPOSITORY_URL,
        },
    )

    assert history_response.status_code == 200

    history_data = history_response.json()

    assert "results" in history_data

    matching_records = [
        record
        for record in history_data["results"]
        if record.get("repository")
        == FAKE_REPOSITORY_URL
    ]

    assert matching_records

    assert all(
        record["repository"]
        == FAKE_REPOSITORY_URL
        for record in matching_records
    )

    delete_integration_records()


def test_analysis_history_filter_by_branch():
    delete_integration_records()

    with patch(
        "app.services.github_services.clone_repository",
        side_effect=fake_clone_repository,
    ), patch(
        "app.services.github_services.requests.get",
        side_effect=fake_requests_get,
    ):
        response = client.post(
            "/repository/analyze",
            params={
                "repository_url": FAKE_REPOSITORY_URL,
            },
        )

    assert response.status_code == 200

    history_response = client.get(
        "/repository/history",
        params={
            "repository": FAKE_REPOSITORY_URL,
            "branch": "main",
        },
    )

    assert history_response.status_code == 200

    history_data = history_response.json()

    assert "results" in history_data

    for record in history_data["results"]:
        assert record["repository"] == (
            FAKE_REPOSITORY_URL
        )

        assert record["branch"] == "main"

    delete_integration_records()


def test_missing_analysis_returns_404():
    response = client.get(
        "/repository/history/999999999"
    )

    assert response.status_code == 404


def test_invalid_repository_is_rejected():
    response = client.post(
        "/repository/analyze",
        params={
            "repository_url": (
                "https://example.com/not-github"
            ),
        },
    )

    assert response.status_code == 400


def test_analysis_does_not_require_real_github_connection():
    delete_integration_records()

    with patch(
        "app.services.github_services.clone_repository",
        side_effect=fake_clone_repository,
    ), patch(
        "app.services.github_services.requests.get",
        side_effect=fake_requests_get,
    ):
        response = client.post(
            "/repository/analyze",
            params={
                "repository_url": FAKE_REPOSITORY_URL,
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"

    delete_integration_records()


# =========================================================
# File Explorer Integration Tests
# =========================================================


FAKE_FILE_REPOSITORY = (
    "https://github.com/test-user/file-repo"
)


class FakeFileResponse:
    def __init__(
        self,
        status_code=200,
        payload=None,
    ):
        self.status_code = status_code
        self.payload = payload

    def json(self):
        if isinstance(
            self.payload,
            Exception,
        ):
            raise self.payload

        return self.payload


def test_file_endpoint_returns_file_content():
    content = (
        "print('hello integration test')\n"
    )

    encoded_content = base64.b64encode(
        content.encode("utf-8")
    ).decode("utf-8")

    response_payload = {
        "type": "file",
        "content": encoded_content,
        "size": len(content),
        "sha": "fake-sha",
    }

    with patch(
        "app.main.requests.get",
        return_value=FakeFileResponse(
            status_code=200,
            payload=response_payload,
        ),
    ):
        response = client.get(
            "/repository/file",
            params={
                "repository": FAKE_FILE_REPOSITORY,
                "branch": "main",
                "path": "main.py",
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["repository"] == (
        FAKE_FILE_REPOSITORY
    )

    assert data["branch"] == "main"

    assert data["path"] == "main.py"

    assert data["content"] == content

    assert data["size"] == len(content)

    assert data["sha"] == "fake-sha"


def test_file_endpoint_returns_404_when_file_missing():
    with patch(
        "app.main.requests.get",
        return_value=FakeFileResponse(
            status_code=404,
            payload={
                "message": "Not Found",
            },
        ),
    ):
        response = client.get(
            "/repository/file",
            params={
                "repository": FAKE_FILE_REPOSITORY,
                "branch": "main",
                "path": "missing.py",
            },
        )

    assert response.status_code == 404

    data = response.json()

    assert data["status"] == "error"

    assert data["error"] == "http_error"

    assert data["message"] == (
        "File not found in repository."
    )


def test_file_endpoint_handles_timeout():
    with patch(
        "app.main.requests.get",
        side_effect=requests.Timeout(),
    ):
        response = client.get(
            "/repository/file",
            params={
                "repository": FAKE_FILE_REPOSITORY,
                "branch": "main",
                "path": "main.py",
            },
        )

    assert response.status_code == 504

    data = response.json()

    assert data["status"] == "error"

    assert data["error"] == "http_error"

    assert data["message"] == (
        "GitHub API request timed out."
    )


def test_file_endpoint_handles_connection_error():
    with patch(
        "app.main.requests.get",
        side_effect=requests.ConnectionError(),
    ):
        response = client.get(
            "/repository/file",
            params={
                "repository": FAKE_FILE_REPOSITORY,
                "branch": "main",
                "path": "main.py",
            },
        )

    assert response.status_code == 502

    data = response.json()

    assert data["status"] == "error"

    assert data["error"] == "http_error"

    assert data["message"] == (
        "Unable to connect to GitHub."
    )


def test_file_endpoint_rejects_invalid_repository():
    response = client.get(
        "/repository/file",
        params={
            "repository": (
                "https://example.com/user/repo"
            ),
            "branch": "main",
            "path": "main.py",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "error"

    assert data["error"] == "http_error"

    assert data["message"] == (
        "Invalid GitHub repository URL."
    )


def test_file_endpoint_rejects_repository_without_owner_and_repo():
    response = client.get(
        "/repository/file",
        params={
            "repository": "https://github.com/",
            "branch": "main",
            "path": "main.py",
        },
    )

    assert response.status_code == 400


def test_file_endpoint_rejects_directory_path():
    response_payload = {
        "type": "dir",
        "content": "",
    }

    with patch(
        "app.main.requests.get",
        return_value=FakeFileResponse(
            status_code=200,
            payload=response_payload,
        ),
    ):
        response = client.get(
            "/repository/file",
            params={
                "repository": FAKE_FILE_REPOSITORY,
                "branch": "main",
                "path": "backend",
            },
        )

    assert response.status_code == 400

    data = response.json()

    assert data["status"] == "error"

    assert data["message"] == (
        "Requested path is not a file."
    )


def test_file_endpoint_handles_invalid_json():
    with patch(
        "app.main.requests.get",
        return_value=FakeFileResponse(
            status_code=200,
            payload=ValueError(
                "Invalid JSON"
            ),
        ),
    ):
        response = client.get(
            "/repository/file",
            params={
                "repository": FAKE_FILE_REPOSITORY,
                "branch": "main",
                "path": "main.py",
            },
        )

    assert response.status_code == 502

    data = response.json()

    assert data["status"] == "error"

    assert data["message"] == (
        "GitHub returned an invalid response."
    )


def test_file_endpoint_handles_empty_content():
    response_payload = {
        "type": "file",
        "content": "",
        "size": 0,
        "sha": "empty-sha",
    }

    with patch(
        "app.main.requests.get",
        return_value=FakeFileResponse(
            status_code=200,
            payload=response_payload,
        ),
    ):
        response = client.get(
            "/repository/file",
            params={
                "repository": FAKE_FILE_REPOSITORY,
                "branch": "main",
                "path": "empty.py",
            },
        )

    assert response.status_code == 500

    data = response.json()

    assert data["status"] == "error"

    assert data["message"] == (
        "Repository file has no readable content."
    )


def test_file_endpoint_requires_repository():
    response = client.get(
        "/repository/file",
        params={
            "branch": "main",
            "path": "main.py",
        },
    )

    assert response.status_code == 422


def test_file_endpoint_requires_path():
    response = client.get(
        "/repository/file",
        params={
            "repository": FAKE_FILE_REPOSITORY,
            "branch": "main",
        },
    )

    assert response.status_code == 422


def test_file_endpoint_rejects_empty_branch():
    response = client.get(
        "/repository/file",
        params={
            "repository": FAKE_FILE_REPOSITORY,
            "branch": "",
            "path": "main.py",
        },
    )

    assert response.status_code == 422