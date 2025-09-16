# Changelog

Notable functional changes

2023-11-24 - Self-modifying API introduced (ccbd052)

- POST /endpoints: accepts code and filepath, commits to GitHub (Contents API), updates app.py to include the new router, and triggers a Render redeploy.
- Required env vars: RENDER_SERVICE_ID, RENDER_TOKEN, GITHUB_TOKEN, GITHUB_REPO, GITHUB_OWNER.
- Health endpoints: GET / and GET /healthcheck return {"status": "ok"}.
- Example endpoint: GET /random-number returns a random integer between 1 and 100.

2023-11-24 - Initial setup (f9b5e4a)

- Initial README and project scaffolding.
