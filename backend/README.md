# Software Archaeologist

Software Archaeologist is a full-stack repository intelligence platform that analyzes public GitHub repositories and generates structured insights about their codebase, architecture, dependencies, complexity, security, maintainability, and overall engineering health.

It combines a FastAPI backend, automated repository analysis services, database-backed analysis history, and an interactive React dashboard.

---

## Live Demo

- **Frontend:** https://software-archaeologist-frontend.onrender.com
- **Backend API:** https://software-archaeologist-api.onrender.com
- **API Documentation:** https://software-archaeologist-api.onrender.com/docs
- **Health Check:** https://software-archaeologist-api.onrender.com/health

---

## Project Overview

Software Archaeologist works like a digital archaeologist for software repositories.

A user provides a public GitHub repository URL. The system validates the repository, verifies it through GitHub, retrieves and scans the codebase, detects technologies and dependencies, analyzes the repository structure, calculates code and health metrics, identifies security and code-quality findings, generates recommendations, and presents the results through an interactive dashboard.

The project was designed to provide a single place where developers can quickly understand the engineering health and structure of an unfamiliar repository.

---

## Key Features

### Repository Analysis

- Analyze public GitHub repositories
- Validate repository URLs
- Verify repositories through the GitHub API
- Clone repositories for local analysis
- Scan repository files and directories
- Detect repository size and structure

### Technology Detection

- Detect primary programming language
- Detect supported programming languages
- Detect frameworks
- Detect project dependencies
- Analyze common dependency configuration files

### Code Analysis

- Count source files
- Count total lines
- Detect functions
- Detect classes
- Analyze code structure
- Calculate cyclomatic complexity
- Identify large files and functions
- Analyze maintainability indicators

### Architecture Analysis

- Generate repository dependency relationships
- Visualize module dependencies
- Inspect analyzed repository structure
- Explore files through the Code Explorer

### Engineering Health

The platform calculates an overall repository health score using multiple engineering categories, including:

- Security
- Testing
- Documentation
- Maintainability
- Architecture
- CI/CD
- Community
- License
- Configuration
- Secret exposure
- Repository metrics
- Code quality

### Security Analysis

- Detect potentially unsafe patterns
- Detect exposed secrets
- Inspect subprocess usage
- Inspect potentially risky database and configuration patterns
- Generate security-related findings

### Code Quality

- Detect code smells
- Analyze complexity
- Identify maintainability issues
- Highlight areas that may require refactoring

### AI-Based Recommendations

The system converts analysis findings and health scores into actionable recommendations.

Recommendations help identify:

- Security improvements
- Testing improvements
- Documentation improvements
- Maintainability improvements
- Code-quality improvements
- Architecture improvements

### Analysis History

- Store previous repository analyses
- View previous analysis results
- Filter analysis history
- Open individual historical analyses
- Persist analysis data using SQLite

### Interactive Dashboard

The React dashboard provides:

- Repository overview
- Overall health score
- Health category breakdown
- Language distribution
- Repository metrics
- Complexity information
- Dependency graph
- Code Explorer
- Findings
- Recommendations
- Analysis history

---

## Architecture / Workflow

The overall analysis workflow is:

```text
GitHub Repository URL
        |
        v
Repository URL Validation
        |
        v
GitHub Repository Verification
        |
        v
Repository Cloning
        |
        v
Repository File Scanning
        |
        v
Language / Framework / Dependency Detection
        |
        v
Architecture & Code Structure Analysis
        |
        v
Complexity & Repository Metrics
        |
        v
Security & Code Quality Analysis
        |
        v
Health Score Calculation
        |
        v
Findings Generation
        |
        v
AI-Based Recommendations
        |
        v
Database Storage
        |
        v
React Dashboard