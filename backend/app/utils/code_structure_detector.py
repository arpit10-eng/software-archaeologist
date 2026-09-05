import os


def detect_code_structure(repo_path, files):
    classes = []
    functions = []

    for file in files:
        if not file.endswith(".py"):
            continue

        absolute_path = os.path.join(repo_path, file)

        try:
            with open(
                absolute_path,
                "r",
                encoding="utf-8",
                errors="ignore",
            ) as f:
                lines = f.readlines()
        except OSError:
            continue

        for line in lines:
            stripped = line.strip()

            # Detect classes
            if stripped.startswith("class "):
                class_name = stripped.split()[1].split("(")[0].rstrip(":")
                classes.append(class_name)

            # Detect functions
            elif stripped.startswith("def "):
                function_name = stripped.split()[1].split("(")[0]
                functions.append(function_name)

    # Remove duplicates and keep results deterministic
    classes = sorted(set(classes))
    functions = sorted(set(functions))

    return {
        "classes": classes,
        "functions": functions,
        "total_classes": len(classes),
        "total_functions": len(functions),
    }