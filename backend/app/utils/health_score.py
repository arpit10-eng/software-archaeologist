def calculate_health_score(
    framework,
    entry_point,
    dependencies,
    architecture
):

    score = 0

    if framework != "Unknown":
        score += 25

    if entry_point:
        score += 25

    if dependencies:
        score += 25

    if architecture:
        score += 25

    return score