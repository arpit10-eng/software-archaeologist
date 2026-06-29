import re

def is_valid_github_url(url: str):
    pattern = r"^https://github\.com/[\w.-]+/[\w.-]+/?$"
    return bool(re.match(pattern, url))