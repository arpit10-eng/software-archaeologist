from app.services.health.score_weights import SCORE_WEIGHTS


def get_total_weight():
    """
    Return the maximum possible health score.
    """
    return sum(SCORE_WEIGHTS.values())


def _to_float(value):
    """
    Safely convert a value to float.
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_score(value, maximum):
    """
    Extract a usable score from analyzer output.

    Supports:
    - int / float
    - numeric strings
    - dictionaries containing score fields
    - dictionaries containing percentage fields
    - nested dictionaries

    The returned value is always clamped between
    0 and the category maximum.
    """

    maximum = float(maximum)

    if value is None:
        return 0.0

    # ---------------------------------------------------------
    # Direct numeric value
    # ---------------------------------------------------------

    numeric_value = _to_float(value)

    if numeric_value is not None:
        return max(
            0.0,
            min(numeric_value, maximum),
        )

    # ---------------------------------------------------------
    # Dictionary
    # ---------------------------------------------------------

    if isinstance(value, dict):

        # Direct score fields
        score_keys = [
            "score",
            "health_score",
            "overall_score",
            "weighted_score",
            "category_score",
            "points",
            "value",
            "weighted_points",
        ]

        for key in score_keys:

            if key not in value:
                continue

            score = _to_float(value[key])

            if score is not None:
                return max(
                    0.0,
                    min(score, maximum),
                )

        # -----------------------------------------------------
        # Percentage fields
        # -----------------------------------------------------

        percentage_keys = [
            "percentage",
            "score_percentage",
            "health_percentage",
            "percent",
            "completion_percentage",
        ]

        for key in percentage_keys:

            if key not in value:
                continue

            percentage = _to_float(value[key])

            if percentage is not None:

                score = (
                    percentage / 100.0
                ) * maximum

                return max(
                    0.0,
                    min(score, maximum),
                )

        # -----------------------------------------------------
        # Some analyzers may store the actual result nested
        # inside another dictionary.
        # -----------------------------------------------------

        nested_keys = [
            "result",
            "data",
            "analysis",
            "summary",
            "metrics",
        ]

        for key in nested_keys:

            nested_value = value.get(key)

            if isinstance(nested_value, dict):

                nested_score = _extract_score(
                    nested_value,
                    maximum,
                )

                if nested_score > 0:
                    return nested_score

    # ---------------------------------------------------------
    # Unknown structure
    # ---------------------------------------------------------

    return 0.0


def calculate_health_score(
    analysis=None,
    **kwargs,
):
    """
    Calculate repository health score.

    Supports both:

        calculate_health_score({
            "security": 14,
            "tests": 6,
        })

    and:

        calculate_health_score(
            security_summary=security_summary,
            tests=tests,
            documentation=documentation,
            ...
        )

    SCORE_WEIGHTS defines the maximum points available
    for every category.

    The final score is normalized to 0-100.
    """

    # ---------------------------------------------------------
    # Normalize input
    # ---------------------------------------------------------

    if analysis is None:
        analysis = {}

    if not isinstance(analysis, dict):
        analysis = {}

    analysis = {
        **analysis,
        **kwargs,
    }

    # ---------------------------------------------------------
    # Calculate category scores
    # ---------------------------------------------------------

    category_scores = {}

    total_score = 0.0
    maximum_score = float(
        get_total_weight()
    )

    for category, maximum in SCORE_WEIGHTS.items():

        value = analysis.get(
            category,
            0,
        )

        score = _extract_score(
            value,
            maximum,
        )

        category_scores[category] = round(
            score,
            2,
        )

        total_score += score

    # ---------------------------------------------------------
    # Overall score
    # ---------------------------------------------------------

    if maximum_score > 0:

        overall_score = (
            total_score
            / maximum_score
        ) * 100.0

    else:

        overall_score = 0.0

    overall_score = max(
        0.0,
        min(
            overall_score,
            100.0,
        ),
    )

    overall_score = round(
        overall_score,
        2,
    )

    # ---------------------------------------------------------
    # Category percentages
    # ---------------------------------------------------------

    category_percentages = {}

    for category, maximum in SCORE_WEIGHTS.items():

        score = category_scores.get(
            category,
            0.0,
        )

        if maximum > 0:

            percentage = (
                score
                / float(maximum)
            ) * 100.0

        else:

            percentage = 0.0

        category_percentages[category] = round(
            percentage,
            2,
        )

    # ---------------------------------------------------------
    # Health level
    # ---------------------------------------------------------

    if overall_score >= 90:

        health_level = "Excellent"

    elif overall_score >= 75:

        health_level = "Good"

    elif overall_score >= 60:

        health_level = "Fair"

    elif overall_score >= 40:

        health_level = "Needs Improvement"

    else:

        health_level = "Poor"

    # ---------------------------------------------------------
    # Final result
    # ---------------------------------------------------------

    return {
        "overall_score": overall_score,
        "health_level": health_level,
        "total_score": round(
            total_score,
            2,
        ),
        "maximum_score": int(
            maximum_score
        ),
        "category_scores": category_scores,
        "category_percentages": category_percentages,
    }