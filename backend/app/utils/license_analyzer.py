import os

def analyze_license(repo_path, files):

    license_files = []
    valid_license_names = [
        "LICENSE",
        "LICENSE.md",
        "LICENSE.txt",
        "COPYING",
        "COPYING.md"
    ]

    for file in files:

        filename = os.path.basename(file)

        if filename in valid_license_names:

            license_files.append(file)

    return {
        "license_found": len(license_files) > 0,
        "license_files": license_files,
        "license_count": len(license_files)
    }