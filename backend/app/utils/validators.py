import re


GITHUB_URL_PATTERN = re.compile(
    r"^https://github\.com/"
    r"[\w.-]+/"
    r"[\w.-]+"
    r"/?$"
)


def is_valid_github_url(url: str) -> bool:
    """
    Validate that a URL points to a GitHub repository.

    Only HTTPS GitHub repository URLs are accepted.
    """

    if not isinstance(
        url,
        str,
    ):
        return False

    url = url.strip()

    if not url:
        return False

    if len(url) > 500:
        return False

    return bool(
        GITHUB_URL_PATTERN.fullmatch(
            url
        )
    )