import os


def analyze_license(repo_path, files):

    license_files = []
    detected_license = "Unknown"

    # Common license filename patterns
    license_names = [
        "license",
        "license.txt",
        "license.md",
        "licence",
        "licence.txt",
        "licence.md",
        "copying",
        "copying.txt",
        "copying.md"
    ]

    # ---------------------------------------------
    # Find license files
    # ---------------------------------------------

    for file in files:

        filename = os.path.basename(
            file.replace("\\", "/")
        ).lower()

        if filename in license_names:
            license_files.append(file)

    # ---------------------------------------------
    # Read license content
    # ---------------------------------------------

    for file in license_files:

        normalized = file.replace("\\", "/")

        absolute_path = os.path.join(
            repo_path,
            normalized.replace("/", os.sep)
        )

        if not os.path.isfile(absolute_path):
            continue

        try:

            with open(
                absolute_path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:

                content = f.read().lower()

            # ---------------------------------------------
            # Detect license type
            # ---------------------------------------------

            if "permission is hereby granted" in content:
                detected_license = "MIT"

            elif (
                "apache license" in content
                and "version 2.0" in content
            ):
                detected_license = "Apache 2.0"

            elif (
                "gnu general public license" in content
                and "version 3" in content
            ):
                detected_license = "GPL-3.0"

            elif (
                "gnu general public license" in content
                and "version 2" in content
            ):
                detected_license = "GPL-2.0"

            elif "gnu lesser general public license" in content:
                detected_license = "LGPL"

            elif "mozilla public license" in content:
                detected_license = "MPL"

            elif (
                "redistribution and use in source and binary forms"
                in content
            ):
                detected_license = "BSD"

            else:
                detected_license = "Unknown"

            break

        except OSError:
            continue

    # ---------------------------------------------
    # License quality
    # ---------------------------------------------

    if detected_license == "Unknown":

        if license_files:
            quality = "Unknown"
            reason = (
                "A license file was found, but the license "
                "type could not be identified."
            )
        else:
            quality = "Missing"
            reason = (
                "No license file was found. "
                "The repository does not clearly specify "
                "software usage rights."
            )

    else:

        quality = "Present"
        reason = (
            f"The repository contains a recognized "
            f"{detected_license} license."
        )

    return {
        "license": detected_license,
        "license_files": license_files,
        "license_file_count": len(license_files),
        "status": quality,
        "reason": reason
    }