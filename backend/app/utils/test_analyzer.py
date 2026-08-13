import os


def analyze_tests(repo_path, files):

    test_files = []
    test_functions = []

    for file in files:

        normalized = file.replace("\\", "/")
        filename = os.path.basename(normalized)

        # Detect Python test files
        if (
            filename.startswith("test_")
            or filename.endswith("_test.py")
        ):
            test_files.append(file)

            absolute_path = os.path.join(
                repo_path,
                normalized.replace("/", os.sep)
            )

            if os.path.isfile(absolute_path):

                try:
                    with open(
                        absolute_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        for line in f:

                            stripped = line.strip()

                            if stripped.startswith("def test_"):

                                function_name = (
                                    stripped
                                    .split("(")[0]
                                    .replace("def ", "")
                                )

                                test_functions.append(
                                    function_name
                                )

                except (UnicodeDecodeError, OSError):
                    continue

    test_functions = sorted(set(test_functions))

    return {
        "test_files": test_files,
        "test_file_count": len(test_files),
        "test_functions": test_functions,
        "test_function_count": len(test_functions)
    }