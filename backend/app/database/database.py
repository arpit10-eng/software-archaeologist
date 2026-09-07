from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


DATABASE_URL = settings.DATABASE_URL


engine_kwargs = {}

if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {
        "check_same_thread": False
    }


engine = create_engine(
    DATABASE_URL,
    **engine_kwargs,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


def ensure_schema():
    """
    Update an existing SQLite database without destroying existing data.

    This is mainly used to add newly introduced columns to an existing
    repository_analyses table.

    For non-SQLite production databases, schema migrations should
    eventually be handled by a dedicated migration system.
    """

    if not DATABASE_URL.startswith("sqlite"):
        return

    inspector = inspect(engine)

    if "repository_analyses" not in inspector.get_table_names():
        return

    columns = {
        column["name"]
        for column in inspector.get_columns(
            "repository_analyses"
        )
    }

    if "created_at" not in columns:
        with engine.begin() as connection:
            connection.execute(
                text(
                    """
                    ALTER TABLE repository_analyses
                    ADD COLUMN created_at DATETIME
                    """
                )
            )

            connection.execute(
                text(
                    """
                    UPDATE repository_analyses
                    SET created_at = CURRENT_TIMESTAMP
                    WHERE created_at IS NULL
                    """
                )
            )