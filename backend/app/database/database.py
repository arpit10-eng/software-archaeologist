import logging

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings


logger = logging.getLogger("software_archaeologist.database")


DATABASE_URL = settings.DATABASE_URL


engine_kwargs = {}


if DATABASE_URL.startswith("sqlite"):
    engine_kwargs["connect_args"] = {
        "check_same_thread": False,
    }

    engine_kwargs["pool_pre_ping"] = True

else:
    engine_kwargs["pool_pre_ping"] = True


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


def get_db():
    """
    Provide a database session for FastAPI endpoints.

    The session is always closed after the request,
    even when an exception occurs.
    """

    db = SessionLocal()

    try:
        yield db

    except SQLAlchemyError:
        logger.exception(
            "Database error while processing request."
        )
        db.rollback()
        raise

    finally:
        db.close()


def ensure_schema():
    """
    Perform lightweight schema compatibility checks.

    Existing SQLite databases are preserved.

    This function ensures that the created_at column exists
    and that existing rows have a timestamp.

    For production deployments using a database such as
    PostgreSQL, a dedicated migration system should be used.
    """

    if not DATABASE_URL.startswith("sqlite"):
        return

    try:
        inspector = inspect(engine)

        table_names = inspector.get_table_names()

        if "repository_analyses" not in table_names:
            return

        columns = {
            column["name"]
            for column in inspector.get_columns(
                "repository_analyses"
            )
        }

        if "created_at" not in columns:
            logger.info(
                "Adding missing created_at column to "
                "repository_analyses."
            )

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

        else:
            with engine.begin() as connection:
                connection.execute(
                    text(
                        """
                        UPDATE repository_analyses
                        SET created_at = CURRENT_TIMESTAMP
                        WHERE created_at IS NULL
                        """
                    )
                )

    except SQLAlchemyError:
        logger.exception(
            "Failed to ensure database schema."
        )
        raise


def initialize_database():
    """
    Create database tables and apply lightweight
    compatibility updates.
    """

    try:
        Base.metadata.create_all(
            bind=engine
        )

        ensure_schema()

        logger.info(
            "Database initialized successfully."
        )

    except SQLAlchemyError:
        logger.exception(
            "Database initialization failed."
        )
        raise