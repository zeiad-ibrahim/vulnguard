# VulnGuard

VulnGuard is a full-stack vulnerability-scanning web application built independently as an A-level project. It gives small IT teams an easy way to detect and understand network security risks without needing to read raw Nmap output.

Built as an independent project following a cybersecurity work-experience placement, where I saw first-hand how much manual, repetitive effort goes into basic network security checks.

## Features

- **User accounts** with signup/login, passwords hashed with `bcrypt` (never stored in plaintext)
- **Full System Scan** — scans all ports on a target and reports open ports with associated services
- **Targeted Scan** — scans a single specified port for a faster, focused check
- **Vulnerability lookup** — cross-references every open port found against a local vulnerability database, returning known risks and concrete remediation recommendations
- **Scan history** — past scan results are saved and viewable per user
- **Settings page** for account management

## Tech stack

- **Backend**: Python, Flask
- **Database**: SQLite
- **Scanning engine**: [python-nmap](https://pypi.org/project/python-nmap/) (wraps the Nmap CLI tool)
- **Frontend**: HTML, CSS, JavaScript
- **Auth**: bcrypt password hashing

## Project structure

```
vulnguard/
├── errorhandling.py         # Flask app — routes, auth, and scan endpoints
├── users.py                # User model and database (users.db) setup
├── vulnerability.py         # One-time script that builds and seeds vulnerabilities.db
├── requirements.txt
├── templates/               # Jinja2 HTML templates (one per page)
└── static/
    ├── logo.jpg
    ├── scripts/              # Per-page JavaScript
    └── styles/               # Per-page CSS
```

## Setup

**Prerequisites:**
- Python 3
- [Nmap](https://nmap.org/download.html) installed on your system and available on your `PATH` (`python-nmap` is a wrapper around the real Nmap binary, not a standalone scanner)

**Steps:**

```bash
# 1. Clone the repo
git clone https://github.com/zeiad-ibrahim/vulnguard.git
cd vulnguard

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Build the vulnerability database (run once)
python vulnerability.py

# 5. Run the app
python errorhandling.py
```

The app will then be available at `http://127.0.0.1:5000`.

> Note: `users.db` and `vulnerabilities.db` are created locally when you run the app/setup script and are not committed to this repo (see `.gitignore`) — this keeps no real scan or account data in version control.

## Background

This project began after a cybersecurity work-experience placement at Xynotech, where I researched cryptography — symmetric and asymmetric encryption, RSA, and the growing threat quantum computing poses to current encryption standards — and presented my findings to the company's engineering and leadership teams. That placement sparked a broader interest in practical, accessible cybersecurity tooling, which led me to independently design and build VulnGuard as an A-level project.

## Author

**Zeiad Ibrahim** — [LinkedIn](https://www.linkedin.com/in/zeiad-ibrahim9/) · [GitHub](https://github.com/zeiad-ibrahim)
