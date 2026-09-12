# Software Archaeologist

Software Archaeologist is a full-stack repository intelligence platform that analyzes GitHub repositories and generates structured insights about their codebase, architecture, dependencies, complexity, security, maintainability, and overall repository health.

It combines a FastAPI backend, automated repository analysis services, a database-backed analysis history, and an interactive React dashboard.

## Live Demo

- Frontend: https://software-archaeologist-frontend.onrender.com
- Backend API: https://software-archaeologist-api.onrender.com
- API Documentation: https://software-archaeologist-api.onrender.com/docs
- Health Check: https://software-archaeologist-api.onrender.com/health

## Overview

Software Archaeologist works like a digital archaeologist for software repositories.

A user provides a public GitHub repository URL. The system validates the repository, retrieves and scans the codebase, detects technologies and dependencies, analyzes the repository structure, calculates code and health metrics, identifies security and code-quality findings, and presents the results through an interactive dashboard.

## How It Works

```text
GitHub Repository URL
        ↓
Repository Validation
        ↓
GitHub Repository Verification
        ↓
Repository Cloning
        ↓
Repository Scanning
        ↓
Language / Framework / Dependency Detection
        ↓
Architecture & Code Structure Analysis
        ↓
Complexity & Repository Metrics
        ↓
Security & Code Quality Findings
        ↓
Health Score Calculation
        ↓
AI-Based Recommendations
        ↓
Database Storage
        ↓
Interactive React Dashboard