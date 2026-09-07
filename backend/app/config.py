import os


def get_bool_env(
    name: str,
    default: bool = False,
) -> bool:
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


class Settings:
    """
    Central application configuration.

    Values are loaded from environment variables so that
    development and production environments can use different
    settings without changing source code.
    """

    APP_NAME = os.getenv(
        "SOFTWARE_ARCHAEOLOGIST_APP_NAME",
        "Software Archaeologist",
    )

    APP_VERSION = os.getenv(
        "SOFTWARE_ARCHAEOLOGIST_APP_VERSION",
        "2.1.0",
    )

    ENVIRONMENT = os.getenv(
        "SOFTWARE_ARCHAEOLOGIST_ENVIRONMENT",
        "development",
    )

    DEBUG = get_bool_env(
        "SOFTWARE_ARCHAEOLOGIST_DEBUG",
        default=False,
    )

    DATABASE_URL = os.getenv(
        "SOFTWARE_ARCHAEOLOGIST_DATABASE_URL",
        "sqlite:///./software_archaeologist.db",
    )

    ALLOWED_ORIGINS = [
        origin.strip()
        for origin in os.getenv(
            "SOFTWARE_ARCHAEOLOGIST_ALLOWED_ORIGINS",
            (
                "http://localhost:5173,"
                "http://127.0.0.1:5173,"
                "http://localhost:5174,"
                "http://127.0.0.1:5174"
            ),
        ).split(",")
        if origin.strip()
    ]

    GITHUB_API_TIMEOUT = int(
        os.getenv(
            "SOFTWARE_ARCHAEOLOGIST_GITHUB_API_TIMEOUT",
            "10",
        )
    )

    REPOSITORY_STORAGE_PATH = os.getenv(
        "SOFTWARE_ARCHAEOLOGIST_REPOSITORY_STORAGE_PATH",
        "temp",
    )


settings = Settings()