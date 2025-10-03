# Agents

This project is designed to be controlled by “agents” (for example, an OpenAI Assistant, a custom GPT, or any LLM-powered workflow) that can create new API endpoints on-the-fly by sending code to this server. The API will commit that code to the repository, update the running application to mount the new route, and trigger a redeploy.

WARNING: This repository is a proof of concept and is not safe for production use. Running arbitrary, agent-provided code on your infrastructure is extremely risky.


## Overview of agents

- An agent is any automated client that:
  - Generates Python FastAPI route code that follows a simple convention.
  - Sends that code to this service’s POST /endpoints endpoint with a target filepath.
  - Waits for the service to commit the code to GitHub, update the app to include the new router, and trigger a redeploy on Render.
- After deployment completes, the newly created route becomes available from the service.

Core flow:
1. Agent generates FastAPI route code (must use `APIRouter` and expose a `router` variable).
2. Agent POSTs the code and a filename (e.g. `random_number.py`) to `/endpoints`.
3. The server:
   - Commits the code to GitHub (branch: `main`).
   - Fetches `app.py` from GitHub, appends an import for the new module and `app.include_router(...)` for its router, and commits that change.
   - Triggers a redeploy on Render so the new route goes live.


## How to use agents

1. Run the API locally or deploy it (see README for basics):
   - Install dependencies: `pip install -r requirements.txt`
   - Start dev server: `./bin/dev` (runs `uvicorn app:app --reload`)
2. Provide the required environment variables (see Agent configuration below). You can place them in a `.env` file. The app loads `.env` via `python-dotenv`.
3. Point your agent at the service and either:
   - Let it discover functions via the OpenAPI spec at `GET /openapi.json` (e.g., for GPT Actions), or
   - Program it to call `POST /endpoints` directly.
4. Ensure the agent always generates code using this template:

   ```python
   from fastapi import APIRouter

   router = APIRouter()

   @router.get("/your-path")
   def your_handler():
       return {"status": "ok"}
   ```

   The existence of a module-level `router` is required because the app dynamically imports the module and calls `app.include_router(<module>.router)`.


## Agent configuration

- Required environment variables (read by `endpoints.py` and loaded in `app.py`):
  - `GITHUB_TOKEN`: GitHub token with permission to write repository contents.
  - `GITHUB_REPO`: The repository name (e.g., `self-modifying-api`).
  - `GITHUB_OWNER`: The repository owner/organization.
  - `RENDER_SERVICE_ID`: Render service ID to redeploy.
  - `RENDER_TOKEN`: Render API token with permission to trigger deploys.

Example `.env`:

```
GITHUB_TOKEN=ghp_...
GITHUB_REPO=self-modifying-api
GITHUB_OWNER=my-username-or-org
RENDER_SERVICE_ID=svc-xxxxxxxxxxxxxxxx
RENDER_TOKEN=rv_yyyyyyyyyyyyyyyyyyyy
```

- OpenAPI integration:
  - The service exposes its OpenAPI spec at `GET /openapi.json` (and interactive docs at `/docs`).
  - For GPT Actions or similar, you can reference this URL as the source of API definitions. In some UIs you may need to set your server URL explicitly.

- Suggested “system”/instruction prompt for a GPT-like agent:

  You make API endpoints by writing Python code for a FastAPI backend. Always start your files with:

  ```python
  from fastapi import APIRouter
  router = APIRouter()
  ```

  Then add one or more routes (e.g., `@router.get("/my-path")`). When you’re done, send your code as a string with a sensible filename (e.g., `my_feature.py`) to the backend’s `POST /endpoints` endpoint.


## Examples

- Create a new endpoint that returns a random number (cURL):

```bash
curl -X POST http://localhost:8000/endpoints \
  -H 'Content-Type: application/json' \
  -d '{
    "code": "from fastapi import APIRouter\nimport random\n\nrouter = APIRouter()\n\n@router.get(\"/random-number\")\ndef generate_random_number():\n    return {\"random_number\": random.randint(1, 100)}",
    "filepath": "random_number.py"
  }'
```

After the redeploy completes, call the new route:

```bash
curl http://localhost:8000/random-number
```

- Minimal health check endpoints (already present):
  - `GET /` and `GET /healthcheck` return `{"status": "ok"}`.


## Relevant API endpoints and integrations

- POST `/endpoints`
  - Request body (JSON):
    - `code` (string): Python source code for a FastAPI router module.
    - `filepath` (string): The filename to write in the repository, e.g., `my_feature.py` or `some/dir/my_feature.py`.
  - Behavior:
    - Commits the file to GitHub on branch `main` using the “Create or update file contents” API.
    - Fetches `app.py` from GitHub, appends an `import <module>` and `app.include_router(<module>.router)`, and commits the change.
    - Triggers a redeploy on Render via `POST /v1/services/{RENDER_SERVICE_ID}/deploys`.
  - Response (overview):
    - `{ "commit_response": { "update_response": ... }, "deploy_response": ... }`

- GET `/openapi.json`
  - FastAPI-generated OpenAPI spec for the running service.

- GET `/docs`
  - Interactive Swagger UI for exploring the API.

- GET `/` and `/healthcheck`
  - Simple health check.

- Integrations used by this service:
  - GitHub REST API (Contents API) for committing code and updating `app.py`.
  - Render Deploy API for triggering redeploys.


## Constraints, limitations, and safety notes

- Danger: Running arbitrary code from agents is inherently unsafe. Do not expose this publicly. Consider sandboxing, allowlists, or human approval steps if you experiment further.
- Dependencies: New Python dependencies used by generated endpoints are not installed automatically. If an agent writes code that imports new libraries, the deployment will likely fail until you add them to `requirements.txt` and redeploy.
- Code conventions: Modules must define `router = APIRouter()` and attach routes to that router. The app imports the module and calls `app.include_router(<module>.router)`.
- Branch and duplicate imports: Commits are made against `main`. `app.py` is mutated by appending imports and `include_router` calls; repeated creation of the same endpoint may cause duplicate lines.
- File overwrites: The GitHub create/update call as implemented assumes new files. Updating an existing file may require additional logic (e.g., providing a SHA) that is not present in this PoC.
- Redeploy timing: Routes only become available after the Render deploy completes.


## Troubleshooting

- 400 from `/endpoints`: Check that all required environment variables are set and that tokens have appropriate permissions. The error body usually includes details from GitHub or Render.
- New route 404s after success: Wait for the Render deploy to finish. Also confirm your route path (e.g., `/random-number`) and that the module defines `router`.
- OpenAPI/Actions not working in your client: Ensure you are using `GET /openapi.json` as the schema source and that your tool knows your deployment’s base URL.


## Quick reference

- Start locally: `./bin/dev`
- Health: `GET /` or `GET /healthcheck`
- OpenAPI: `GET /openapi.json`
- Create endpoint: `POST /endpoints` with `{ code: <string>, filepath: <string> }`
