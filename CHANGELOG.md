# Changelog

Summary of important functional changes on this branch (last two commits available on this branch).

2023-11-24 - Introduced self-modifying FastAPI service (ccbd052 "Squash")

- New FastAPI application (app.py) with environment loading via python-dotenv.
- Health endpoints (healthcheck.py):
  - GET / and GET /healthcheck return {"status": "ok"}.
- Endpoint factory (endpoints.py):
  - New POST /endpoints accepts JSON payload { code: string, filepath: string }.
  - Commits the provided code to GitHub via the Contents API.
  - Automatically updates app.py to import the new module and include its router.
  - Triggers a redeploy on Render to make the new endpoint live.
  - Requires environment variables: RENDER_SERVICE_ID, RENDER_TOKEN, GITHUB_TOKEN, GITHUB_REPO, GITHUB_OWNER.
- Example endpoint (random_number.py):
  - GET /random-number returns a random integer between 1 and 100.
- Tooling and config:
  - bin/dev script to run the dev server locally.
  - render.yaml for Render deployment configuration.
  - requirements.txt with FastAPI, requests, uvicorn, and related dependencies.
  - .gitignore updated to ignore env files and pyc.

2023-11-24 - Project genesis (f9b5e4a "first commit")

- Added initial README.md describing the proof-of-concept and usage notes.
