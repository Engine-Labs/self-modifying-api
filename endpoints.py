import base64
import json
import os

import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

RENDER_SERVICE_ID = os.getenv("RENDER_SERVICE_ID")
RENDER_TOKEN = os.getenv("RENDER_TOKEN")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")
GITHUB_OWNER = os.getenv("GITHUB_OWNER")

router = APIRouter()


class CodeRequest(BaseModel):
    code: str
    filepath: str


@router.post("/endpoints")
def create_endpoint(request: CodeRequest):
    try:
        commit_response = commit_to_github(
            request.code,
            request.filepath,
            GITHUB_TOKEN,
            GITHUB_REPO,
            GITHUB_OWNER,
        )

        deploy_response = trigger_render_redeploy(RENDER_SERVICE_ID, RENDER_TOKEN)

        return {
            "commit_response": commit_response,
            "deploy_response": deploy_response,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


def commit_to_github(file_content: str, path: str, token: str, repo: str, owner: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = {
        "message": "Update " + path,
        "content": base64.b64encode(file_content.encode()).decode(),
        "branch": "main",  # or the branch you want to commit to
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))
    if not response.ok:
        raise Exception("GitHub commit failed: " + response.text)

    # Update app.py with new endpoint route
    import_name = path.replace("/", ".").replace(".py", "")
    current_app_py = get_file("app.py", token, repo, owner)
    app_py_sha = current_app_py["sha"]
    app_py_content = base64.b64decode(current_app_py["content"]).decode()

    app_py_content += f"\nimport {import_name}\n"
    app_py_content += f"\napp.include_router({import_name}.router)\n"

    update_response = update_file(
        "app.py", app_py_content, app_py_sha, token, repo, owner
    )

    return {
        "update_response": update_response,
    }


def update_file(filepath, file_content, file_sha, token, repo, owner):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    data = {
        "message": "Update " + filepath,
        "content": base64.b64encode(file_content.encode()).decode(),
        "branch": "main",  # or the branch you want to commit to
        "sha": file_sha,
    }

    response = requests.put(url, headers=headers, data=json.dumps(data))
    if not response.ok:
        raise Exception("GitHub commit failed: " + response.text)

    return response.json()


def get_file(filepath: str, token: str, repo: str, owner: str):
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{filepath}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers)
    if not response.ok:
        raise Exception("GitHub get file sha failed: " + response.text)

    return response.json()


def trigger_render_redeploy(render_service_id: str, render_token: str):
    url = f"https://api.render.com/v1/services/{render_service_id}/deploys"
    headers = {"Authorization": f"Bearer {render_token}"}

    response = requests.post(url, headers=headers)
    if not response.ok:
        raise Exception("Render redeploy failed: " + response.text)
    return response.json()
