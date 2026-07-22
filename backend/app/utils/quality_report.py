def generate_quality_report(
    framework,
    architecture,
    dependencies
):

    strengths = []
    warnings = []

    if framework == "FastAPI":
        strengths.append("Uses FastAPI")

    if "services" in architecture:
        strengths.append("Uses Service Layer Architecture")

    if (
        "models" in architecture and
        "services" in architecture and
        "utils" in architecture
    ):
        strengths.append("Follows Modular Architecture")

    if not dependencies:
        warnings.append("No dependencies detected")

    return {
        "strengths": strengths,
        "warnings": warnings
    }