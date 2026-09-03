from app.utils.ai_recommendation import (
    generate_recommendations,
)


def test_recommendations_return_list():
    analysis = {
        "security": 2,
        "secret_exposure": 1,
        "tests": 1,
        "documentation": 2,
        "maintainability": 3,
        "architecture": 3,
        "code_quality": 2,
        "ci_cd": 0,
        "license": 0,
        "community": 0,
        "configuration": 1,
        "repository_metrics": 2,
    }

    recommendations = (
        generate_recommendations(
            analysis
        )
    )

    assert isinstance(
        recommendations,
        list,
    )


def test_low_scores_generate_recommendations():
    analysis = {
        "security": 0,
        "secret_exposure": 0,
        "tests": 0,
        "documentation": 0,
        "maintainability": 0,
        "architecture": 0,
        "code_quality": 0,
        "ci_cd": 0,
        "license": 0,
        "community": 0,
        "configuration": 0,
        "repository_metrics": 0,
    }

    recommendations = (
        generate_recommendations(
            analysis
        )
    )

    assert len(
        recommendations
    ) > 0


def test_recommendations_have_expected_fields():
    analysis = {
        "security": 0,
        "secret_exposure": 0,
        "tests": 0,
        "documentation": 0,
        "maintainability": 0,
        "architecture": 0,
        "code_quality": 0,
        "ci_cd": 0,
        "license": 0,
        "community": 0,
        "configuration": 0,
        "repository_metrics": 0,
    }

    recommendations = (
        generate_recommendations(
            analysis
        )
    )

    assert len(
        recommendations
    ) > 0

    recommendation = recommendations[0]

    assert "title" in recommendation
    assert "description" in recommendation
    assert "priority" in recommendation
    assert "category" in recommendation