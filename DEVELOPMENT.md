# Development Setup — Self Modifying API

WARNING: This project is a proof of concept and intentionally dangerous. Do NOT deploy to the public internet without understanding the risks.

This document walks you through setting up a local development environment, configuring external services, and running the application.

## 1) Prerequisites

- OS: macOS, Linux, or Windows (WSL recommended on Windows)
- Git 2.40+
- Python 3.11+ (3.10 may work but 3.11 is recommended)
- pip and venv (bundled with Python)
- curl or HTTPie (for manual API calls)
- Accounts and tokens (only required if you plan to exercise the self-modifying endpoint locally):
  - GitHub account + Personal Access Token (classic) with at least `repo` scope
  - Render account + API key and an existing Render Web Service for this repo

## 2) Clone and install

- Clone the repository:
  - git clone <your fork or the canonical repo URL>
  - cd self-modifying-api
- Create and activate a virtual environment:
  - python3 -m venv .venv
  - source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
- Install dependencies:
  - pip install -r requirements.txt

## 3) Configuration (environment variables)

The app reads environment variables via python-dotenv. Create a file named `.env` in the project root with the following keys if you want to use the self-modifying endpoint that commits to GitHub and triggers a Render redeploy:

RENDER_SERVICE_ID=<your-render-service-id>
RENDER_TOKEN=<your-render-api-token>
GITHUB_TOKEN=<your-github-personal-access-token>
GITHUB_REPO=<repository-name-only>
GITHUB_OWNER=<your-github-username-or-org>

- RENDER_SERVICE_ID: The ID of your Render Web Service. You can find this in the Render dashboard under the service’s settings (also visible in the service details URL and via the Render API).
- RENDER_TOKEN: Create a Render API key in the Render dashboard.
- GITHUB_TOKEN: A GitHub Personal Access Token (classic) with `repo` scope so the app can commit to your repository and update files via the GitHub Contents API.
- GITHUB_REPO: The repository name (e.g., `self-modifying-api`), not the full URL.
- GITHUB_OWNER: The owner/org of the repo (e.g., `your-username` or `your-org`).

Notes:
- The implementation commits to the `main` branch. Ensure your repo’s default branch is `main` or adjust the code accordingly.
- For local development that does NOT call the self-modifying endpoint, you can omit these variables.

## 4) Run the application locally

- Start the dev server with auto-reload:
  - ./bin/dev
  - Or: uvicorn app:app --reload
- The API will be available at:
  - http://127.0.0.1:8000
  - Interactive docs: http://127.0.0.1:8000/docs

Available starter endpoints:
- GET / and GET /healthcheck → returns {"status": "ok"}
- POST /endpoints → commits new endpoint code to GitHub and triggers a Render redeploy (requires env vars)

## 5) Common development commands

- Start server (hot reload):
  - ./bin/dev
- Run server manually:
  - uvicorn app:app --reload --port 8000
- Linting / formatting / tests:
  - This repository does not currently include linting or tests. You can add tools like `black`, `ruff`, and `pytest` if desired.

## 6) External services setup (Render + GitHub)

Render
- A sample Render configuration is provided in `render.yaml`:
  - Build command: pip install -r requirements.txt
  - Start command: uvicorn app:app --host 0.0.0.0 --port $PORT
  - autoDeploy: false (redeploys are triggered via the API)
- Configure environment variables on Render. The example references an environment group named `self-modifying-api`:
  - You can either create that group and add the variables, or set them directly on the service.
- Find your service ID in the Render dashboard (required by the app to trigger redeploys).

GitHub
- Create a repo to host the API (or use this repo).
- Ensure the default branch is `main` or update the code to commit to your chosen branch.
- Create a Personal Access Token (classic) with `repo` scope and keep it secret.

How the self-modification flow works
1) POST /endpoints with JSON body:
{
  "code": "from fastapi import APIRouter\n\nrouter = APIRouter()\n\n@router.get(\"/hello\")\ndef hello():\n    return {\"message\": \"hello\"}",
  "filepath": "hello.py"
}
2) The API:
  - Commits the file to your GitHub repo via the Contents API
  - Appends to `app.py` in the repo to import the new module and include its router
  - Triggers a Render redeploy so the new route becomes available in production

Important behaviors and limitations
- New Python dependencies required by newly added endpoints are NOT auto-installed. If a new endpoint imports a library not in `requirements.txt`, update `requirements.txt` and redeploy.
- The /endpoints flow updates files in GitHub and production. Your local dev server won’t automatically pick up those remote changes until you pull/rebase locally and restart.

## 7) Troubleshooting

- uvicorn: command not found
  - Ensure your virtual environment is activated and dependencies are installed.
- 401/403 errors from GitHub commit or get file calls
  - Verify `GITHUB_TOKEN`, `GITHUB_OWNER`, `GITHUB_REPO` are correct and the token has `repo` scope.
  - Ensure the target repo and `main` branch exist and you have write access.
- 401/403 errors from Render redeploy
  - Verify `RENDER_TOKEN` and `RENDER_SERVICE_ID`.
- GitHub file not found errors for `app.py`
  - Ensure the GitHub repo you target contains `app.py` at the root (i.e., you’re pointing at the correct repo).
- Address already in use (when starting server)
  - Another process occupies port 8000. Stop it or use `--port 8001`.
- Changes to endpoint code don’t show up locally
  - The self-modifying flow updates the GitHub copy of `app.py` and the endpoint file, then redeploys Render. Pull the latest changes locally and restart the dev server.
- Permission errors running ./bin/dev
  - Make the script executable: `chmod +x bin/dev`.

## Reference: Project structure

- app.py — FastAPI app creation, router inclusion (updated remotely by the API)
- endpoints.py — Implementation of the self-modifying POST /endpoints
- healthcheck.py — Simple health endpoints
- random_number.py — Example endpoint
- bin/dev — Convenience script to run uvicorn with reload
- render.yaml — Render deployment configuration
- requirements.txt — Python dependencies
- .env — Local environment variables (not committed)

If you run into issues not covered here, please open an issue with details about your OS, Python version, and any error logs.
