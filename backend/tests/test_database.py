import json

from app.database.database import SessionLocal
from app.database.models import RepositoryAnalysis


def test_database_can_create_and_read_analysis():
    db = SessionLocal()

    record = None

    try:
        record = RepositoryAnalysis(
            repository="https://github.com/test-user/test-repo",
            branch="main",
            primary_language="Python",
            analysis_json=json.dumps(
                {
                    "health_score": 85,
                    "health_level": "Good",
                }
            ),
        )

        db.add(record)
        db.commit()
        db.refresh(record)

        assert record.id is not None
        assert record.repository == (
            "https://github.com/test-user/test-repo"
        )
        assert record.branch == "main"
        assert record.primary_language == "Python"
        assert record.created_at is not None

    finally:
        if record is not None and record.id is not None:
            db.delete(record)
            db.commit()

        db.close()


def test_database_analysis_json_persists():
    db = SessionLocal()

    record = None

    try:
        payload = {
            "health_score": 92,
            "health_level": "Excellent",
            "total_files": 10,
        }

        record = RepositoryAnalysis(
            repository="https://github.com/test-user/json-repo",
            branch="develop",
            primary_language="Java",
            analysis_json=json.dumps(payload),
        )

        db.add(record)
        db.commit()

        analysis_id = record.id

        stored = (
            db.query(RepositoryAnalysis)
            .filter(
                RepositoryAnalysis.id == analysis_id
            )
            .first()
        )

        assert stored is not None

        restored_payload = json.loads(
            stored.analysis_json
        )

        assert restored_payload == payload

    finally:
        if record is not None and record.id is not None:
            db.delete(record)
            db.commit()

        db.close()


def test_database_repository_and_branch_filtering():
    db = SessionLocal()

    records = []

    try:
        records = [
            RepositoryAnalysis(
                repository="https://github.com/test-user/filter-repo",
                branch="main",
                primary_language="Python",
                analysis_json="{}",
            ),
            RepositoryAnalysis(
                repository="https://github.com/test-user/filter-repo",
                branch="develop",
                primary_language="Python",
                analysis_json="{}",
            ),
        ]

        db.add_all(records)
        db.commit()

        results = (
            db.query(RepositoryAnalysis)
            .filter(
                RepositoryAnalysis.repository
                == "https://github.com/test-user/filter-repo"
            )
            .filter(
                RepositoryAnalysis.branch == "main"
            )
            .all()
        )

        assert len(results) == 1
        assert results[0].branch == "main"

    finally:
        for record in records:
            if record.id is not None:
                db.delete(record)

        db.commit()
        db.close()


def test_database_indexes_exist():
    indexes = RepositoryAnalysis.__table__.indexes

    index_names = {
        index.name
        for index in indexes
    }

    assert (
        "ix_repository_analyses_repo_branch_created"
        in index_names
    )