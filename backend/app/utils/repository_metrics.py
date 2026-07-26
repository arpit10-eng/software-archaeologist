import os


def generate_repository_metrics(repo_path, files):

    directories = set()
    total_size = 0
    largest_directory = ""
    largest_count = 0
    directory_count = {}

    for file in files:

        full_path = os.path.join(repo_path, file)

        if os.path.exists(full_path):

            total_size += os.path.getsize(full_path)

        directory = os.path.dirname(file)

        directories.add(directory)

        directory_count[directory] = directory_count.get(directory, 0) + 1

    for directory, count in directory_count.items():

        if count > largest_count:
            largest_count = count
            largest_directory = directory

    average_size = 0

    if len(files) > 0:
        average_size = round(total_size / len(files))

    return {
        "directories": len(directories),
        "python_files": sum(1 for f in files if f.endswith(".py")),
        "average_file_size": average_size,
        "largest_directory": largest_directory
    }