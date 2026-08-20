import os
import ast


def analyze_complexity(repo_path, files):

    total_lines = 0
    largest_file = ""
    largest_file_lines = 0
    python_file_count = 0

    longest_function_name = ""
    longest_function_file = ""
    longest_function_lines = 0

    total_functions = 0
    total_classes = 0

    total_complexity = 0

    function_details = []

    # =========================================================
    # 1. Analyze Python files
    # =========================================================

    for file in files:

        if not file.endswith(".py"):
            continue

        python_file_count += 1

        absolute_path = os.path.join(
            repo_path,
            file
        )

        try:

            with open(
                absolute_path,
                "r",
                encoding="utf-8"
            ) as f:

                source = f.read()

            lines = source.splitlines()

        except (OSError, UnicodeDecodeError):

            continue

        line_count = len(lines)

        total_lines += line_count

        # =====================================================
        # 2. Largest File
        # =====================================================

        if line_count > largest_file_lines:

            largest_file_lines = line_count
            largest_file = os.path.basename(file)

        # =====================================================
        # 3. Parse Python AST
        # =====================================================

        try:

            tree = ast.parse(source)

        except SyntaxError:

            continue

        # =====================================================
        # 4. Count Classes
        # =====================================================

        classes = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.ClassDef)
        ]

        total_classes += len(classes)

        # =====================================================
        # 5. Detect Functions
        # =====================================================

        functions = [
            node
            for node in ast.walk(tree)
            if isinstance(
                node,
                (
                    ast.FunctionDef,
                    ast.AsyncFunctionDef
                )
            )
        ]

        total_functions += len(functions)

        # =====================================================
        # 6. Analyze Every Function
        # =====================================================

        for function in functions:

            # -------------------------------------------------
            # Function length
            # -------------------------------------------------

            if hasattr(function, "end_lineno"):

                function_lines = (
                    function.end_lineno
                    - function.lineno
                    + 1
                )

            else:

                function_lines = 1

            # -------------------------------------------------
            # Cyclomatic Complexity
            # -------------------------------------------------

            complexity = 1

            for node in ast.walk(function):

                if isinstance(
                    node,
                    (
                        ast.If,
                        ast.For,
                        ast.While,
                        ast.IfExp,
                        ast.Try,
                        ast.ExceptHandler,
                        ast.With,
                        ast.AsyncWith
                    )
                ):
                    complexity += 1

                elif isinstance(
                    node,
                    ast.BoolOp
                ):

                    # Every additional boolean condition
                    # increases complexity.

                    complexity += (
                        len(node.values) - 1
                    )

                elif isinstance(
                    node,
                    (
                        ast.comprehension,
                    )
                ):

                    complexity += 1

            total_complexity += complexity

            # -------------------------------------------------
            # Longest Function
            # -------------------------------------------------

            if function_lines > longest_function_lines:

                longest_function_lines = function_lines

                longest_function_name = (
                    function.name
                )

                longest_function_file = (
                    os.path.basename(file)
                )

            # -------------------------------------------------
            # Store Function Information
            # -------------------------------------------------

            function_details.append(
                {
                    "name": function.name,
                    "file": os.path.basename(file),
                    "lines": function_lines,
                    "complexity": complexity
                }
            )

    # =========================================================
    # 7. Average Lines Per File
    # =========================================================

    if python_file_count > 0:

        average_lines_per_file = round(
            total_lines / python_file_count,
            2
        )

    else:

        average_lines_per_file = 0

    # =========================================================
    # 8. Average Cyclomatic Complexity
    # =========================================================

    if total_functions > 0:

        average_complexity = round(
            total_complexity / total_functions,
            2
        )

    else:

        average_complexity = 0

    # =========================================================
    # 9. Complexity Level
    # =========================================================

    if average_complexity <= 3:

        complexity_level = "Low"

    elif average_complexity <= 7:

        complexity_level = "Moderate"

    elif average_complexity <= 10:

        complexity_level = "High"

    else:

        complexity_level = "Very High"

    # =========================================================
    # 10. Find Most Complex Functions
    # =========================================================

    most_complex_functions = sorted(
        function_details,
        key=lambda x: x["complexity"],
        reverse=True
    )[:10]

    # =========================================================
    # 11. Find Long Functions
    # =========================================================

    long_functions = [
        function
        for function in function_details
        if function["lines"] > 50
    ]

    # =========================================================
    # 12. Function Complexity Warnings
    # =========================================================

    complexity_warnings = []

    for function in function_details:

        if function["complexity"] > 10:

            complexity_warnings.append(
                {
                    "file": function["file"],
                    "function": function["name"],
                    "complexity": function["complexity"],
                    "severity": "High",
                    "recommendation":
                        "Break this function into smaller functions."
                }
            )

        elif function["complexity"] > 7:

            complexity_warnings.append(
                {
                    "file": function["file"],
                    "function": function["name"],
                    "complexity": function["complexity"],
                    "severity": "Medium",
                    "recommendation":
                        "Consider simplifying this function."
                }
            )

    # =========================================================
    # 13. Return Complexity Report
    # =========================================================

    return {

        "total_lines": total_lines,

        "largest_file": largest_file,

        "largest_file_lines": largest_file_lines,

        "total_python_files": python_file_count,

        "average_lines_per_file":
            average_lines_per_file,

        "total_functions":
            total_functions,

        "total_classes":
            total_classes,

        "total_cyclomatic_complexity":
            total_complexity,

        "average_cyclomatic_complexity":
            average_complexity,

        "complexity_level":
            complexity_level,

        "longest_function": {
            "name": longest_function_name,
            "file": longest_function_file,
            "lines": longest_function_lines
        },

        "long_functions":
            long_functions,

        "most_complex_functions":
            most_complex_functions,

        "complexity_warnings":
            complexity_warnings
    }