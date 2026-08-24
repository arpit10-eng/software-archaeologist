# backend/app/services/health/score_weights.py

SCORE_WEIGHTS = {
    "security": 15,
    "testing": 10,
    "code_quality": 10,
    "documentation": 10,
    "maintainability": 10,
    "architecture": 10,
    "ci_cd": 10,
    "community": 5,
    "license": 5,
    "configuration": 5,
    "secret_exposure": 5,
    "repository_metrics": 5,
}


def get_total_weight():
    return sum(SCORE_WEIGHTS.values())