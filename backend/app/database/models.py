from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    String,
    Text,
    func,
)

from app.database.database import Base


class RepositoryAnalysis(Base):
    __tablename__ = "repository_analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    repository = Column(
        String(500),
        nullable=False,
        index=True,
    )

    branch = Column(
        String(250),
        nullable=False,
        index=True,
    )

    primary_language = Column(
        String(100),
        nullable=True,
    )

    analysis_json = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=func.current_timestamp(),
        server_default=func.current_timestamp(),
        nullable=False,
        index=True,
    )

    __table_args__ = (
        Index(
            "ix_repository_analyses_repo_branch_created",
            "repository",
            "branch",
            "created_at",
        ),
    )