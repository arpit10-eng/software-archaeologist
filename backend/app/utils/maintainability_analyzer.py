import os

def generate_maintainability(repo_path, files):

    excellent = 0
    good = 0
    poor = 0

    largest_file = ""
    largest_file_lines = 0
    for file in files:

        if not file.endswith(".py"):
            continue

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        line_count = len(lines)
        if line_count < 100:
            excellent += 1
        elif line_count < 150:
            good += 1
        else:
            poor += 1

        if line_count > largest_file_lines:
            largest_file_lines = line_count
            largest_file = os.path.basename(file)

    return {
    "excellent": excellent,
    "good": good,
    "poor": poor,
    "worst_file": largest_file
}