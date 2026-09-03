from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = "sqlite:///./software_archaeologist.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
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
    """

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