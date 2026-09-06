import os
import re

SENSITIVE_NAMES = {".env", ".env.local", ".env.production", ".env.development", ".env.test", "credentials.json", "secrets.json", "service-account.json", "id_rsa", "id_ed25519"}
PATTERNS = [
    ("AWS access key", r"\bAKIA[0-9A-Z]{16}\b", "Critical"),
    ("Private key", r"-----BEGIN [A-Z ]*PRIVATE KEY-----", "Critical"),
    ("API key", r"(?i)\b(?:api[_-]?key|secret[_-]?key|access[_-]?token)\s*[:=]\s*['\"][^'\"]{8,}['\"]", "High"),
    ("Password", r"(?i)\b(?:password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{6,}['\"]", "High"),
    ("Database credentials", r"(?i)\b(?:postgres|mysql|mongodb(?:\+srv)?|redis)://[^/\s:@]+:[^/\s@]+@", "High"),
]

def _redact(value):
    return re.sub(r"(?i)(password|passwd|pwd|api[_-]?key|secret[_-]?key|token|authorization)\s*[:=]\s*(['\"])[^'\"]*\2", r"\1=\2[REDACTED]\2", value or "")

def analyze_secret_exposure(repo_path, files):
    sensitive_files, findings = [], []
    gitignore_found = False
    for file in files:
        normalized = file.replace("\\", "/")
        filename = os.path.basename(normalized).lower()
        if filename == ".gitignore": gitignore_found = True
        if filename in SENSITIVE_NAMES or filename.startswith(".env."): sensitive_files.append(file)
        path = os.path.join(repo_path, normalized.replace("/", os.sep))
        if not os.path.isfile(path): continue
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as handle:
                for line_number, line in enumerate(handle, 1):
                    stripped=line.strip()
                    if not stripped or stripped.startswith("#"): continue
                    for kind, pattern, severity in PATTERNS:
                        if re.search(pattern, stripped):
                            findings.append({"file":file,"line":line_number,"type":kind,"severity":severity,"message":"Potential secret detected. The source value is redacted.","code":_redact(stripped)})
                            break
        except OSError: continue
    unique={(f["file"],f["line"],f["type"]):f for f in findings}
    return {"gitignore_found":gitignore_found,"sensitive_files":sorted(set(sensitive_files)),"sensitive_file_count":len(set(sensitive_files)),"findings":sorted(unique.values(),key=lambda x:(x["file"],x["line"])),"secret_finding_count":len(unique)}
