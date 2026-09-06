import os
import re

SECURITY_RULES = [
    (r"password\s*=\s*['\"].+['\"]", "Hardcoded Password", "High", "Store passwords in environment variables or a secret manager."),
    (r"(api[_-]?key)\s*=\s*['\"].+['\"]", "Hardcoded API Key", "High", "Store API keys outside source control."),
    (r"(token|access_token)\s*=\s*['\"].+['\"]", "Hardcoded Token", "High", "Store tokens securely outside source control."),
    (r"(secret|secret_key|jwt_secret)\s*=\s*['\"].+['\"]", "Hardcoded Secret", "High", "Store secrets outside source control."),
    (r"(aws_access_key|aws_secret_access_key)\s*=\s*['\"].+['\"]", "AWS Credentials", "Critical", "Never commit cloud credentials."),
    (r"-----BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY-----", "Private Key Found", "Critical", "Remove private keys from source control and rotate exposed credentials."),
    (r"os\.system\s*\(", "Use of os.system()", "Medium", "Prefer subprocess APIs with argument lists and validated input."),
    (r"\beval\s*\(", "Use of eval()", "High", "Avoid dynamic evaluation of untrusted input."),
    (r"\bexec\s*\(", "Use of exec()", "High", "Avoid dynamic code execution unless strictly controlled."),
    (r"pickle\.(load|loads)\s*\(", "Unsafe pickle deserialization", "High", "Never deserialize untrusted pickle data."),
    (r"shell\s*=\s*True", "Shell execution enabled", "High", "Avoid shell=True and pass arguments as a list where possible."),
]

def _redact(line):
    return re.sub(r"(?i)(password|passwd|pwd|api[_-]?key|secret[_-]?key|token|authorization)\s*([:=])\s*(['\"])[^'\"]*\3", r"\1\2\3[REDACTED]\3", line)

def detect_database_credentials(line):
    match = re.search(r"(database_url|db_url|database_uri|db_uri)\s*=\s*['\"]([^'\"]+)['\"]", line, re.I)
    if not match or match.group(2).lower().startswith("sqlite://"):
        return None
    if re.search(r"://[^/\s:@]+:[^/\s@]+@", match.group(2)):
        return {"issue": "Database Credentials", "severity": "High", "recommendation": "Store database credentials securely."}
    return None

def analyze_security(repo_path, files):
    issues = []
    supported = {".py", ".js", ".jsx", ".ts", ".tsx", ".java", ".php", ".rb", ".go", ".rs", ".json", ".yaml", ".yml"}
    for file in files:
        normalized = file.replace("\\", "/")
        if os.path.splitext(normalized)[1].lower() not in supported:
            continue
        if os.path.basename(normalized).lower() in {"security_analyzer.py", "secret_exposure_analyzer.py"}:
            continue
        path = os.path.join(repo_path, normalized.replace("/", os.sep))
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as handle:
                lines = handle.readlines()
        except OSError:
            continue
        for line_number, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            database_issue = detect_database_credentials(stripped)
            if database_issue:
                issues.append({"file": file, "line": line_number, "code": _redact(stripped), **database_issue})
                continue
            for pattern, issue, severity, recommendation in SECURITY_RULES:
                if re.search(pattern, line, re.I):
                    issues.append({"file": file, "line": line_number, "code": _redact(stripped), "issue": issue, "severity": severity, "recommendation": recommendation})
                    break
    return issues
