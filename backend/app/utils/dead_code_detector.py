import os
import re


def detect_dead_code(repo_path, files):

    defined_functions = []
    called_functions = set()
    dead_code = []

    for file in files:

        if not file.endswith(".py"):
            continue

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Scan every line in the current file
        for line_number, line in enumerate(lines, start=1):

            stripped = line.strip()

            # Detect function definitions
            if stripped.startswith("def "):

                function_name = stripped.split()[1].split("(")[0]

                defined_functions.append({
                    "name": function_name,
                    "file": file,
                    "line": line_number
                })

            # Detect function calls
            matches = re.findall(
                r'([A-Za-z_][A-Za-z0-9_]*)\s*\(',
                stripped
            )

            for match in matches:

                if match not in [
                    "if",
                    "for",
                    "while",
                    "with",
                    "print",
                    "return",
                    "def",
                    "class"
                ]:
                    called_functions.add(match)

    # Find functions that are never called
    for function in defined_functions:

        if function["name"] not in called_functions:

            dead_code.append({
                "file": function["file"],
                "function": function["name"],
                "line": function["line"]
            })

    return dead_code