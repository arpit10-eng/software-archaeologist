import os


def analyze_tests(repo_path, files):

    test_files = []
    test_functions = []

    for file in files:

        if not file.endswith(".py"):
            continue

        filename = os.path.basename(file)

        if filename.startswith("test_"):
            test_files.append(file)

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line in lines:

            stripped = line.strip()

            if stripped.startswith("def test_"):

                function_name = (
                    stripped.split()[1]
                    .split("(")[0]
                )

                test_functions.append({
                    "file": file,
                    "function": function_name
                })

    return {
        "test_files": test_files,
        "test_file_count": len(test_files),
        "test_functions": test_functions,
        "test_function_count": len(test_functions)
    }