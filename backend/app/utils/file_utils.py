import os

def get_file_extension(file_path):
    """
    Returns the extension of a file.
    Example:
    main.py -> .py
    README.md -> .md
    """

    _, extension = os.path.splitext(file_path)

    return extension.lower()