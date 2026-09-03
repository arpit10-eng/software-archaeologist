from sqlalchemy import Column, DateTime, Integer, String, Text, func

from app.database.database import Base


class RepositoryAnalysis(Base):
    __tablename__ = "repository_analyses"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    repository = Column(
        String,
        nullable=False,
    )

    branch = Column(
        String,
        nullable=False,
    )

    primary_language = Column(
        String,
        nullable=True,
    )

    analysis_json = Column(
        Text,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
    )