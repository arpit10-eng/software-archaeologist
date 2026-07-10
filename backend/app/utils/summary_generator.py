def generate_summary(
    primary_language,
    framework,
    architecture,
    dependencies
):

    summary = (
        f"This repository is a {primary_language} project "
        f"built using {framework}. "
    )

    if architecture:
        summary += (
            f"It follows a modular architecture with "
            f"{', '.join(architecture.keys())}. "
        )

    if dependencies:
        summary += (
            f"It uses dependencies such as "
            f"{', '.join(dependencies)}."
        )

    return summary