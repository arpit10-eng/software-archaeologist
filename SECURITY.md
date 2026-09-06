# Security Policy

## Reporting a vulnerability

Please do not open a public issue for a suspected security vulnerability.
Report it privately to the repository maintainer with a description, affected
component, reproduction steps, and potential impact.

## Scope

Security reports for the Software Archaeologist API, repository analysis
logic, secret detection, and dashboard are welcome.

## Secret handling

The analyzer is designed to redact detected secret values from findings.
Detected credentials should still be treated as compromised and rotated.
