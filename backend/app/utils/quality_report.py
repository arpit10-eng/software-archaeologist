def generate_quality_report(
    framework,
    architecture,
    dependencies,
    files
):

    strengths = []
    warnings = []

    # Framework Check
    if framework == "FastAPI":
        strengths.append("Uses FastAPI")

    # Service Layer Check
    if "services" in architecture:
        strengths.append("Uses Service Layer Architecture")

    # Modular Architecture Check
    if (
        "models" in architecture and
        "services" in architecture and
        "utils" in architecture
    ):
        strengths.append("Follows Modular Architecture")

    # README Check
    for file in files:
        if file.endswith("README.md"):
            strengths.append("Repository contains documentation")
            break

    # Dependency Check
    if not dependencies:
        warnings.append("No dependencies detected")

    # Tests Check
    if "tests" in architecture:
        strengths.append("Contains Test Suite")
    else:
        warnings.append("No tests directory found")

    return {
        "strengths": strengths,
        "warnings": warnings
    }