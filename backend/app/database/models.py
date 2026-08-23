from sqlalchemy import Column, Integer, String, Text
from app.database.database import Base


class RepositoryAnalysis(Base):

    __tablename__ = "repository_analyses"

    id = Column(Integer, primary_key=True, index=True)

    repository = Column(String, nullable=False)

    branch = Column(String, nullable=False)

    primary_language = Column(String, nullable=True)

    analysis_json = Column(Text, nullable=False)