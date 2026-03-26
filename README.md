# DevGuard
Automated DevOps Compliance Analyzer

DevGuard is a powerful, command-line tool that automatically scans your DevOps configuration files (such as Dockerfiles and CI/CD workflows) to ensure they adhere to security guidelines and compliance best practices.

## Features

DevGuard currently scans for the following compliance checks:

### Docker Compliance
- **Latest Tag Rule:** Warns against using the `latest` tag for base images to ensure deterministic builds.
- **Root User Rule:** Checks if the container runs as root, suggesting a dedicated user for better security.
- **Sensitive Port Rule:** Detects exposed sensitive ports (e.g., 22 for SSH) inside Dockerfiles.

### CI/CD Pipeline Checks
- **Pipeline Existence:** Ensures that CI/CD workflows (like GitHub Actions) actually exist.
- **Test Stage Verification:** Checks if testing stages are included in the pipeline to prevent untested code deployments.
- **Action Pinning:** Verifies that GitHub Actions use specific version hashes instead of volatile tags/branches.

### Security Checks
- **Hardcoded Secrets:** Scans files to identify embedded sensitive tokens (AWS credentials, Stripe tokens, generic API keys).

## Installation

**Prerequisites:** Python 3.8+ and Git installed on your system.

1. **Clone the repository:**
   ```bash
   git clone https://github.com/amaygarg15/DevGuard.git
   cd DevGuard
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

You can run DevGuard against a local directory or directly against a remote GitHub repository.

**Scan a Local Repository:**
```bash
python main.py --path /path/to/your/repo
```

**Scan a Remote GitHub Repository:**
```bash
python main.py --url https://github.com/username/repository
```

## How It Works

1. **Scanner:** Clones (if a URL is provided) and recursively scans the target repository for common DevOps configuration files (like `Dockerfile` or `.github/workflows/*.yml`).
2. **Rules Engine:** Passes the discovered files through categorized rule classes (`rules/docker_rules.py`, `rules/cicd_rules.py`, etc.).
3. **Report Generation:** Aggregates warnings and failures, calculates a compliance score, and prints a final structured summary to your terminal.

## Example Output

```text
==================================================
   DEVGUARD - DevOps Compliance Checker
==================================================
Found 1 Dockerfiles
Found 1 CI/CD workflows
Running compliance checks...

[FAIL] [tests/sample_repo/Dockerfile:8] Detected 'latest' tag. Pin a specific version instead.
[PASS] [tests/sample_repo/Dockerfile] No exposed sensitive ports found.
[FAIL] [tests/sample_repo/Dockerfile:14] Potential Generic Secret Assignment detected.

--------------------------------------------------
COMPLIANCE SCORE: 75/100
STATUS: FAILED ❌ (Please fix the highly critical issues above)
```

