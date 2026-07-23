import os


def analyze_security(repo_path, files):

    security_issues = []

    for file in files:

        # Analyze only Python files
        if not file.endswith(".py"):
            continue

        absolute_path = os.path.join(repo_path, file)

        with open(absolute_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for line_number, line in enumerate(lines, start=1):

            # Detect eval()
            if "eval(" in line:
                security_issues.append({
                    "file": file,
                    "line": line_number,
                    "issue": "Use of eval() detected",
                    "severity": "High",
                    "recommendation": "Avoid eval(). Use safer alternatives such as ast.literal_eval() when appropriate."
                })

            # Detect exec()
            if "exec(" in line:
                security_issues.append({
                    "file": file,
                    "line": line_number,
                    "issue": "Use of exec() detected",
                    "severity": "High",
                    "recommendation": "Avoid exec() unless absolutely necessary. Prefer explicit function calls."
                })

            # Detect os.system()
            if "os.system(" in line:
                security_issues.append({
                    "file": file,
                    "line": line_number,
                    "issue": "Use of os.system() detected",
                    "severity": "Medium",
                    "recommendation": "Use subprocess.run() with validated arguments instead of os.system()."
                })

            # Detect subprocess.run()
            if "subprocess.run(" in line:
                security_issues.append({
                    "file": file,
                    "line": line_number,
                    "issue": "Use of subprocess.run() detected",
                    "severity": "Medium",
                    "recommendation": "Validate user input before passing arguments to subprocess.run(). Avoid shell=True unless absolutely necessary."
                })

            # Detect subprocess.call()
            if "subprocess.call(" in line:
                security_issues.append({
                    "file": file,
                    "line": line_number,
                    "issue": "Use of subprocess.call() detected",
                    "severity": "Medium",
                    "recommendation": "Validate user input before calling subprocess.call(). Avoid shell=True whenever possible."
                })

    return security_issues