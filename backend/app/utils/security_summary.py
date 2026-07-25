def generate_security_summary(security_issues):

    summary = {
        "total_issues": len(security_issues),
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    for issue in security_issues:

        severity = issue["severity"].lower()

        if severity in summary:
            summary[severity] += 1

    return summary