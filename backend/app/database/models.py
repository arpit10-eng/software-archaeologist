from sqlalchemy import Column, Integer, String, Text

from app.database.database import Base


class RepositoryAnalysis(Base):

    __tablename__ = "repository_analysis"

    id = Column(Integer, primary_key=True, index=True)

    repository_url = Column(String, nullable=False)

    branch = Column(String, default="main")

    health_score = Column(Integer)

    summary = Column(Text)