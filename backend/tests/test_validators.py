from app.utils.validators import is_valid_github_url


def test_valid_github_url():
    url = "https://github.com/arpit10-eng/software-archaeologist"

    assert is_valid_github_url(url) is True


def test_invalid_github_url():
    url = "https://google.com/test"

    assert is_valid_github_url(url) is False


def test_github_url_without_repository():
    url = "https://github.com/"

    assert is_valid_github_url(url) is False