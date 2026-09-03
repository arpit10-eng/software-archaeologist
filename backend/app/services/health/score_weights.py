"""
Canonical health-score weights used by the repository health engine.

All category maximums live here so the scoring system has a single
source of truth.
"""

SCORE_WEIGHTS = {
    "security": 15,
    "tests": 10,
    "documentation": 10,
    "maintainability": 10,
    "architecture": 10,
    "ci_cd": 10,
    "community": 5,
    "license": 10,
    "configuration": 5,
    "secret_exposure": 5,
    "repository_metrics": 5,
    "code_quality": 10,
}


def get_total_weight():
    """Return the maximum possible raw health score."""
    return sum(SCORE_WEIGHTS.values())