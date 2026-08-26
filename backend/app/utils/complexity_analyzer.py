import os
import ast


# =============================================================
# Complexity Visitor
# =============================================================

class ComplexityVisitor(ast.NodeVisitor):

    def __init__(self):
        self.complexity = 1

    def visit_If(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_For(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncFor(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_While(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_IfExp(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_Try(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_ExceptHandler(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_With(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_AsyncWith(self, node):
        self.complexity += 1
        self.generic_visit(node)

    def visit_BoolOp(self, node):
        self.complexity += len(node.values) - 1
        self.generic_visit(node)

    def visit_Match(self, node):
        self.complexity += len(node.cases)
        self.generic_visit(node)

    def visit_Assert(self, node):
        self.complexity += 1
        self.generic_visit(node)


# =============================================================
# Calculate Function Complexity
# =============================================================

def calculate_function_complexity(function):

    visitor = ComplexityVisitor()

    for node in function.body:

        # -----------------------------------------------------
        # Important:
        # Do not include nested function/class complexity
        # inside the parent function.
        # -----------------------------------------------------

        if isinstance(
            node,
            (
                ast.FunctionDef,
                ast.AsyncFunctionDef,
                ast.ClassDef
            )
        ):
            continue

        visitor.visit(node)

    return visitor.complexity


# =============================================================
# Function Type
# =============================================================

def get_function_type(function):

    if isinstance(function, ast.AsyncFunctionDef):
        return "async"

    return "function"


# =============================================================
# Severity
# =============================================================

def determine_severity(complexity, lines):

    if complexity >= 15 or lines > 100:
        return "Critical"

    if complexity > 10 or lines > 75:
        return "High"

    if complexity > 7 or lines > 50:
        return "Medium"

    return "Low"


# =============================================================
# Main Analyzer
# =============================================================

def analyze_complexity(repo_path, files):

    total_lines = 0
    largest_file = ""
    largest_file_lines = 0

    python_file_count = 0

    total_functions = 0
    total_classes = 0

    total_complexity = 0

    longest_function_name = ""
    longest_function_file = ""
    longest_function_lines = 0

    function_details = []
    file_details = []

    # =========================================================
    # 1. Analyze Python Files
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

        except (
            OSError,
            UnicodeDecodeError
        ):

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
        # 3. Parse AST
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

        file_complexity = 0

        # =====================================================
        # 6. Analyze Functions
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
            # Function complexity
            # -------------------------------------------------

            complexity = calculate_function_complexity(
                function
            )

            total_complexity += complexity

            file_complexity += complexity

            # -------------------------------------------------
            # Function type
            # -------------------------------------------------

            function_type = get_function_type(
                function
            )

            # -------------------------------------------------
            # Method detection
            # -------------------------------------------------

            is_method = False

            for parent in ast.walk(tree):

                if isinstance(parent, ast.ClassDef):

                    for child in parent.body:

                        if child is function:

                            is_method = True
                            break

            # -------------------------------------------------
            # Longest function
            # -------------------------------------------------

            if function_lines > longest_function_lines:

                longest_function_lines = function_lines

                longest_function_name = function.name

                longest_function_file = (
                    os.path.basename(file)
                )

            # -------------------------------------------------
            # Function details
            # -------------------------------------------------

            function_details.append(
                {
                    "name": function.name,
                    "file": os.path.basename(file),
                    "lines": function_lines,
                    "complexity": complexity,
                    "type": function_type,
                    "is_method": is_method
                }
            )

        # =====================================================
        # 7. File Details
        # =====================================================

        file_details.append(
            {
                "file": os.path.basename(file),
                "lines": line_count,
                "functions": len(functions),
                "classes": len(classes),
                "complexity": file_complexity
            }
        )

    # =========================================================
    # 8. Average Lines Per File
    # =========================================================

    if python_file_count > 0:

        average_lines_per_file = round(
            total_lines / python_file_count,
            2
        )

    else:

        average_lines_per_file = 0

    # =========================================================
    # 9. Average Complexity
    # =========================================================

    if total_functions > 0:

        average_complexity = round(
            total_complexity / total_functions,
            2
        )

    else:

        average_complexity = 0

    # =========================================================
    # 10. Complexity Level
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
    # 11. Most Complex Functions
    # =========================================================

    most_complex_functions = sorted(
        function_details,
        key=lambda x: x["complexity"],
        reverse=True
    )[:10]

    # =========================================================
    # 12. Long Functions
    # =========================================================

    long_functions = [
        function
        for function in function_details
        if function["lines"] > 50
    ]

    # =========================================================
    # 13. Complexity Warnings
    # =========================================================

    complexity_warnings = []

    for function in function_details:

        complexity = function["complexity"]
        lines = function["lines"]

        severity = determine_severity(
            complexity,
            lines
        )

        # -----------------------------------------------------
        # Critical
        # -----------------------------------------------------

        if severity == "Critical":

            if complexity >= 15 and lines > 100:

                recommendation = (
                    "Function is both highly complex and very long. "
                    "Break it into smaller functions."
                )

            elif complexity >= 15:

                recommendation = (
                    "Function has very high cyclomatic complexity. "
                    "Break conditional logic into smaller functions."
                )

            else:

                recommendation = (
                    "Function is too long. "
                    "Split it into smaller functions."
                )

            complexity_warnings.append(
                {
                    "file": function["file"],
                    "function": function["name"],
                    "complexity": complexity,
                    "lines": lines,
                    "severity": severity,
                    "recommendation": recommendation
                }
            )

        # -----------------------------------------------------
        # High
        # -----------------------------------------------------

        elif severity == "High":

            if complexity > 10:

                recommendation = (
                    "Break this function into smaller functions."
                )

            else:

                recommendation = (
                    "Reduce the size of this function."
                )

            complexity_warnings.append(
                {
                    "file": function["file"],
                    "function": function["name"],
                    "complexity": complexity,
                    "lines": lines,
                    "severity": severity,
                    "recommendation": recommendation
                }
            )

        # -----------------------------------------------------
        # Medium
        # -----------------------------------------------------

        elif severity == "Medium":

            complexity_warnings.append(
                {
                    "file": function["file"],
                    "function": function["name"],
                    "complexity": complexity,
                    "lines": lines,
                    "severity": severity,
                    "recommendation":
                        "Consider simplifying this function."
                }
            )

    # =========================================================
    # 14. Most Complex Files
    # =========================================================

    most_complex_files = sorted(
        file_details,
        key=lambda x: x["complexity"],
        reverse=True
    )[:10]

    # =========================================================
    # 15. Return Report
    # =========================================================

    return {

        "total_lines":
            total_lines,

        "largest_file":
            largest_file,

        "largest_file_lines":
            largest_file_lines,

        "total_python_files":
            python_file_count,

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
            "name":
                longest_function_name,
            "file":
                longest_function_file,
            "lines":
                longest_function_lines
        },

        "long_functions":
            long_functions,

        "most_complex_functions":
            most_complex_functions,

        "most_complex_files":
            most_complex_files,

        "complexity_warnings":
            complexity_warnings
    }