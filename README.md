# pytest-api-automation-framework

> **Production-grade REST API test automation framework built with Python & Pytest**
> — CRUD testing · Schema validation · Auth handling · CI/CD · HTML reports

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Pytest](https://img.shields.io/badge/Pytest-8.1-green)](https://pytest.org)
[![CI](https://github.com/S0SP/AutoPy-API-Test-Automation-Framework/actions/workflows/test.yml/badge.svg)](https://github.com/S0SP/AutoPy-API-Test-Automation-Framework/actions)

---

## 📌 Project Overview

This framework automates REST API testing against **[ReqRes.in](https://reqres.in/)** — a realistic public API — using patterns found in real enterprise QA environments:

- Token-based auth handled once at session level (no repeated logins)
- Reusable HTTP client wrapper — swap the base URL, all tests follow
- JSON Schema validation on every critical response
- Data-driven test cases via external JSON files
- GitHub Actions pipeline — tests run on every push/PR and daily at 6 AM

Built to demonstrate real automation engineering, not just "write a test that hits an API."

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3.11 |
| Test Runner | Pytest 8.1 |
| HTTP Client | Requests 2.31 |
| Schema Validation | jsonschema 4.22 |
| Reporting | pytest-html 4.1 |
| Env Management | python-dotenv |
| Parallel Execution | pytest-xdist |
| CI/CD | GitHub Actions |

---

## 📂 Folder Structure

```
pytest-api-automation-framework/
├── tests/
│   ├── test_users.py        # CRUD tests: GET, POST, PUT, PATCH, DELETE
│   └── test_auth.py         # Login, Register, Token tests
├── utils/
│   ├── api_client.py        # Reusable HTTP wrapper (GET/POST/PUT/PATCH/DELETE)
│   ├── assertions.py        # Custom assertion helpers with clear error messages
│   └── logger.py            # File + console logging setup
├── config/
│   └── settings.py          # Env-var-based config (BASE_URL, credentials)
├── data/
│   ├── users.json           # Test data: user IDs, create payloads, update payloads
│   └── schemas.py           # JSON Schema definitions for response validation
├── reports/                 # Auto-generated HTML report + log files
├── .github/
│   └── workflows/
│       └── test.yml         # GitHub Actions CI pipeline
├── conftest.py              # Session fixtures, auth token, teardown hooks
├── pytest.ini               # Test config, markers, HTML report output path
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## ⚡ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/S0SP/AutoPy-API-Test-Automation-Framework.git
cd AutoPy-API-Test-Automation-Framework
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment
```bash
cp .env.example .env
```
Edit `.env` and add your **free API key** from [app.reqres.in](https://app.reqres.in/):
```
API_KEY=your-key-here
```
> All other values are pre-configured for reqres.in — only the API key is required.

---

## ▶️ Running Tests

### Run all tests
```bash
pytest
```

### Run with verbose output
```bash
pytest -v
```

### Run by marker (smoke tests only)
```bash
pytest -m smoke
```

### Run auth tests only
```bash
pytest tests/test_auth.py -v
```

### Run in parallel (4 workers)
```bash
pytest -n 4
```

### Run with HTML report
```bash
pytest --html=reports/report.html --self-contained-html
```

---

## 📊 Sample Output

```
tests/test_auth.py::TestAuthentication::test_login_valid_credentials PASSED
tests/test_auth.py::TestAuthentication::test_login_missing_password PASSED
tests/test_users.py::TestGetUsers::test_get_users_list_returns_200 PASSED
tests/test_users.py::TestGetUsers::test_get_single_user_parametrized[1-George-Bluth] PASSED
tests/test_users.py::TestGetUsers::test_get_single_user_parametrized[2-Janet-Weaver] PASSED
tests/test_users.py::TestCreateUser::test_create_user_parametrized[user0] PASSED
tests/test_users.py::TestUpdateUser::test_put_update_user PASSED
tests/test_users.py::TestDeleteUser::test_delete_user_returns_204 PASSED

====== 18 passed in 4.21s ======
```

After running, open `reports/report.html` in your browser to see the full interactive HTML report.

---

## 🔁 CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/test.yml`) automatically:

1. Triggers on every push to `main` or `develop`, every pull request, and daily at 6 AM UTC
2. Sets up Python 3.11 with pip caching for faster runs
3. Installs dependencies and creates `.env` from GitHub Secrets
4. Runs the full test suite with HTML report generation
5. Uploads the HTML report and logs as artifacts (retained 14 days)

**To set secrets**: Go to your repo → Settings → Secrets → Actions → New secret

---

## 🔑 Key Design Decisions

| Decision | Why it matters |
|---|---|
| `APIClient` wrapper | All HTTP logic in one place — tests stay clean |
| Session-scoped auth fixture | Login once per run, not per test |
| JSON Schema validation | Catches breaking API contract changes early |
| Parametrized tests | Covers multiple cases with one function |
| Custom `Assertions` class | Descriptive failure messages — no guessing what broke |
| `.env` config | Zero hardcoded secrets, environment-switchable |

---

## 🌍 Why This Matters

In production environments, automation engineers don't just write test scripts — they build **maintainable frameworks** that teams rely on for CI/CD gating. This project demonstrates:

- Framework architecture thinking (not just test writing)
- Separation of concerns (config / utils / tests / data)
- Real-world patterns: session reuse, schema contracts, environment isolation
- CI/CD integration that runs without human intervention

---

*Built to demonstrate production-quality pytest automation engineering.*
