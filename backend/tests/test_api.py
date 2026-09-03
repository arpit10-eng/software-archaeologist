from fastapi.testclient import (
    TestClient,
)

from app.main import app


client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(
        data,
        dict,
    )


def test_history_endpoint():
    response = client.get(
        "/repository/history"
    )

    assert response.status_code == 200

    data = response.json()

    assert "results" in data
    assert "total" in data

    assert isinstance(
        data["results"],
        list,
    )


def test_history_not_found():
    response = client.get(
        "/repository/history/999999999"
    )

    assert response.status_code == 404


def test_file_endpoint_requires_repository():
    response = client.get(
        "/repository/file"
    )

    assert response.status_code == 422