from app.services.health.health_score_service import (
    calculate_health_score,
)


def test_health_score_returns_expected_structure():
    analysis = {
        "security": 10,
        "tests": 5,
        "documentation": 8,
        "maintainability": 7,
        "architecture": 8,
        "ci_cd": 5,
        "community": 2,
        "license": 10,
        "configuration": 4,
        "secret_exposure": 5,
        "repository_metrics": 4,
        "code_quality": 7,
    }

    result = calculate_health_score(analysis)

    assert isinstance(result, dict)

    assert "overall_score" in result
    assert "health_level" in result
    assert "category_percentages" in result

    assert isinstance(
        result["overall_score"],
        (int, float),
    )

    assert isinstance(
        result["category_percentages"],
        dict,
    )


def test_health_score_is_between_zero_and_hundred():
    analysis = {
        "security": 0,
        "tests": 0,
        "documentation": 0,
        "maintainability": 0,
        "architecture": 0,
        "ci_cd": 0,
        "community": 0,
        "license": 0,
        "configuration": 0,
        "secret_exposure": 0,
        "repository_metrics": 0,
        "code_quality": 0,
    }

    result = calculate_health_score(analysis)

    assert 0 <= result["overall_score"] <= 100


def test_perfect_health_score():
    analysis = {
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

    result = calculate_health_score(analysis)

    assert result["overall_score"] == 100