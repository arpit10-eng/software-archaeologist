import os


def analyze_complexity(repo_path, files):

    total_lines = 0
    largest_file = ""
    largest_file_lines = 0

    for file in files:

        if not file.endswith(".py"):
            continue

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        line_count = len(lines)

        total_lines += line_count

        if line_count > largest_file_lines:
            largest_file_lines = line_count
            largest_file = os.path.basename(file)

    return {
        "total_lines": total_lines,
        "largest_file": largest_file,
        "largest_file_lines": largest_file_lines
    }