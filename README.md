# Automation Toolkit

![Tests](https://github.com/andreas-portfolio/automation-toolkit/actions/workflows/automation-toolkit.yml/badge.svg)

Python automation scripts for development workflows


## Features
Currently contains 4 scripts

### Log analyzer
A tool used to parse application log files to extract useful information such as which errors have occured and how many

### Backup automation
Creates timestamped, compressed backups of directories

### Project setup automation
Creates new Python projects with proper structure

### Environment validator
Checks and validates:
- Python version
- Git installation and version
- Docker installation and if a container is running
- If minimum required disk space is available

## Installation

Clone the repository:
```bash
git clone https://github.com/andreas-portfolio/automation-toolkit.git
cd automation-toolkit
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
### Log analyzer
```
$ python ./scripts/analyze_logs.py -i test.log
Analyzing log file: test.log

Found 10 total log entries

- INFO: 3
- WARNING: 2
- ERROR: 4
- CRITICAL: 1
- DEBUG: 0

Found 5 error/critical entries

Database connection timeout: 3 times, first seen 2025-12-03 09:15:23
Failed to process request: 1 times, first seen 2025-12-03 10:42:11
System shutting down: 1 times, first seen 2025-12-03 13:45:10

Report saved to: test_report.json
```

### Backup automation
```
$ python scripts/backup.py -s my-project -d backup-dir
Backup created: backup-dir\my-project_2025-12-10_15-08-04.tar.gz
```

### Project setup automation
```
$ python ./scripts/setup_projects.py
Project name: example-project
Creating project: example-project!
Type: basic

Created: example-project
Created: example-project\src
Created: example-project\tests
Created: example-project\docs
Created: example-project\README.md
Created: example-project\.gitignore
Created: example-project\requirements.txt
Project 'example-project' created successfully!
Location: ./example-project/
```

### Environment validator
```
$ python ./scripts/validate_env.py
Starting validation...

✓ Python version 3.12.0 (required: 3.9+)
✓ Git version 2.50.1.windows.1
✓ Docker version 29.0.1, build eedd969
X Docker is not running.
✓ Disk space: 84GB (required: >10GB)

4/5 points passed.
```

## Testing
Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=scripts
```

## Tech Stack
- Python 3.12
- Click (CLI framework)
- pytest (testing)
- GitHub Actions (CI/CD)
- Libraries: tarfile, csv, json, pathlib, subprocess, datetime, sys, shutil, re