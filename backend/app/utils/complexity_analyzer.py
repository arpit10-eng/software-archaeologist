import os


def analyze_complexity(repo_path, files):

    total_lines = 0
    largest_file = ""
    largest_file_lines = 0
    python_file_count = 0

    for file in files:

        if not file.endswith(".py"):
            continue

        # Count Python files
        python_file_count += 1

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        line_count = len(lines)

        # Count total lines
        total_lines += line_count

        # Find largest file
        if line_count > largest_file_lines:
            largest_file_lines = line_count
            largest_file = os.path.basename(file)

    # Calculate average lines per Python file
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
        "average_lines_per_file": average_lines_per_file
    }