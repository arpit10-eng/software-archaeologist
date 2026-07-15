import os


def detect_code_structure(repo_path, files):

    classes = []
    functions = []

    for file in files:

        if not file.endswith(".py"):
            continue

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("class "):

                class_name = stripped.split()[1].split("(")[0].rstrip(":")

                classes.append(class_name)

            elif stripped.startswith("def "):

                function_name = stripped.split()[1].split("(")[0]

                functions.append(function_name)

    classes = sorted(set(classes))
    functions = sorted(set(functions))

    return {
        "classes": classes,
        "functions": functions
}