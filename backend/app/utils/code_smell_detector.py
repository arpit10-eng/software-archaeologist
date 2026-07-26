import os


def detect_code_smells(repo_path, files):

    smells = []

    for file in files:

        if not file.endswith(".py"):
            continue

        path = os.path.join(repo_path, file)

        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Long file
        if len(lines) > 300:
            smells.append({
                "file": file,
                "issue": "Large file",
                "severity": "Medium",
                "recommendation": "Split the file into smaller modules."
            })

        nested_loops = 0

        for line in lines:

            stripped = line.lstrip()

            if stripped.startswith(("for ", "while ")):
                indent = len(line) - len(stripped)

                if indent >= 8:
                    nested_loops += 1

        if nested_loops >= 3:
            smells.append({
                "file": file,
                "issue": "Deeply nested loops",
                "severity": "Low",
                "recommendation": "Refactor nested loops into helper functions."
            })

    return smells