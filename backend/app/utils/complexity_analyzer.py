import os


def analyze_complexity(repo_path, files):

    total_lines = 0
    largest_file = ""
    largest_file_lines = 0
    python_file_count = 0

    longest_function_name = ""
    longest_function_file = ""
    longest_function_lines = 0

    for file in files:

        if not file.endswith(".py"):
            continue

        python_file_count += 1

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        line_count = len(lines)

        total_lines += line_count

        if line_count > largest_file_lines:
            largest_file_lines = line_count
            largest_file = os.path.basename(file)

        # ---------- Longest Function Detection ----------

        inside_function = False
        current_function = ""
        current_length = 0
        function_indent = 0

        for line in lines:

            stripped = line.lstrip()

            if inside_function:

                if stripped == "" or stripped.startswith("#"):
                    continue

                current_indent = len(line) - len(stripped)

                if current_indent <= function_indent:

                    if current_length > longest_function_lines:
                        longest_function_lines = current_length
                        longest_function_name = current_function
                        longest_function_file = os.path.basename(file)

                    inside_function = False

                else:
                    current_length += 1
                    continue

            if stripped.startswith("def "):

                inside_function = True
                current_function = stripped.split()[1].split("(")[0]
                current_length = 1
                function_indent = len(line) - len(stripped)

        # Save last function if file ends while inside it
        if inside_function:

            if current_length > longest_function_lines:
                longest_function_lines = current_length
                longest_function_name = current_function
                longest_function_file = os.path.basename(file)

    if python_file_count > 0:
        average_lines_per_file = round(
            total_lines / python_file_count,
            2
        )
    else:
        average_lines_per_file = 0

    return {
        "total_lines": total_lines,
        "largest_file": largest_file,
        "largest_file_lines": largest_file_lines,
        "total_python_files": python_file_count,
        "average_lines_per_file": average_lines_per_file,
        "longest_function": {
            "name": longest_function_name,
            "file": longest_function_file,
            "lines": longest_function_lines
        }
    }