import os


def analyze_repository_size(repo_path, files):

    total_size = 0
    largest_file = ""
    largest_file_size = 0

    for file in files:

        absolute_path = os.path.join(repo_path, file)

        if not os.path.isfile(absolute_path):
            continue

        size = os.path.getsize(absolute_path)
        total_size += size

        if size > largest_file_size:
            largest_file_size = size
            largest_file = file

    return {
        "total_size_bytes": total_size,
        "largest_file": largest_file,
        "largest_file_size_bytes": largest_file_size
    }