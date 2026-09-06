from app.services.health.score_weights import SCORE_WEIGHTS


def get_total_weight():
    return sum(SCORE_WEIGHTS.values())


def _to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _extract_score(value, maximum):
    maximum = float(maximum)
    if value is None:
        return 0.0
    number = _to_float(value)
    if number is not None:
        return max(0.0, min(number, maximum))
    if isinstance(value, dict):
        for key in ("score", "health_score", "overall_score", "weighted_score", "category_score", "points", "value", "weighted_points"):
            number = _to_float(value.get(key))
            if number is not None:
                return max(0.0, min(number, maximum))
        for key in ("percentage", "score_percentage", "health_percentage", "percent", "completion_percentage"):
            number = _to_float(value.get(key))
            if number is not None:
                return max(0.0, min(number / 100.0 * maximum, maximum))
        for key in ("result", "data", "analysis", "summary", "metrics"):
            if isinstance(value.get(key), dict):
                nested = _extract_score(value[key], maximum)
                if nested > 0:
                    return nested
    return 0.0


def calculate_health_score(analysis=None, **kwargs):
    analysis = dict(analysis or {}) if isinstance(analysis or {}, dict) else {}
    analysis.update(kwargs)
    category_scores = {}
    category_percentages = {}
    category_details = {}
    total_score = 0.0
    maximum_score = float(get_total_weight())

    for category, maximum in SCORE_WEIGHTS.items():
        score = round(_extract_score(analysis.get(category, 0), maximum), 2)
        percentage = round((score / maximum) * 100.0, 2) if maximum else 0.0
        category_scores[category] = score
        category_percentages[category] = percentage
        if percentage >= 90: status = "Excellent"
        elif percentage >= 75: status = "Good"
        elif percentage >= 60: status = "Fair"
        elif percentage >= 40: status = "Needs Improvement"
        else: status = "Poor"
        category_details[category] = {"score": score, "maximum": maximum, "percentage": percentage, "status": status}
        total_score += score

    overall_score = round((total_score / maximum_score) * 100.0, 2) if maximum_score else 0.0
    if overall_score >= 90: health_level = "Excellent"
    elif overall_score >= 75: health_level = "Good"
    elif overall_score >= 60: health_level = "Fair"
    elif overall_score >= 40: health_level = "Needs Improvement"
    else: health_level = "Poor"

    return {"overall_score": overall_score, "health_level": health_level,
            "total_score": round(total_score, 2), "maximum_score": int(maximum_score),
            "category_scores": category_scores, "category_percentages": category_percentages,
            "category_details": category_details}
