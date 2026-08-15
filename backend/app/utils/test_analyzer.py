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

    # ---------------------------------------------
    # Test quality analysis
    # ---------------------------------------------

    test_file_count = len(test_files)
    test_function_count = len(test_functions)

    if test_file_count == 0:

        test_score = 0
        test_level = "Poor"
        test_reason = "No test files were found."

    elif test_function_count == 0:

        test_score = 25
        test_level = "Poor"
        test_reason = (
            "Test files exist but no test functions were detected."
        )

    elif test_function_count < 5:

        test_score = 60
        test_level = "Fair"
        test_reason = (
            "Some test functions were detected, "
            "but the test suite is relatively small."
        )

    elif test_function_count < 10:

        test_score = 80
        test_level = "Good"
        test_reason = (
            "The repository contains a reasonable number "
            "of test functions."
        )

    else:

        test_score = 100
        test_level = "Excellent"
        test_reason = (
            "The repository contains a strong number "
            "of test functions."
        )

    return {
        "test_files": test_files,
        "test_file_count": test_file_count,
        "test_functions": test_functions,
        "test_function_count": test_function_count,
        "test_quality": {
            "score": test_score,
            "level": test_level,
            "reason": test_reason
        }
    }