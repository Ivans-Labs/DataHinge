from fastapi import APIRouter, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import git
from uuid import uuid4
import shutil
from datetime import datetime

router = APIRouter()

class DownloadRepoRequest(BaseModel):
    repo_url: str
    output_dir: str
    github_token: str = None
    clone_depth: int = None
    branch: str = None

def download_repo(task_id: str, repo_url: str, output_dir: str, github_token: str = None, clone_depth: int = None, branch: str = None):
    env = {"GIT_HTTP_USER_AGENT": "GitDownloader"}
    if github_token:
        env["GIT_HTTP_AUTHORIZATION"] = f"token {github_token}"

    repo_name = os.path.basename(repo_url)
    if not repo_name:
        repo_name = datetime.now().strftime('%Y%m%d%H%M%S%f')
    repo_path = os.path.join(output_dir, repo_name)

    try:
        clone_args = {'env': env, 'depth': clone_depth} if clone_depth else {'env': env}
        if branch:
            clone_args['branch'] = branch
        repo = git.Repo.clone_from(repo_url, repo_path, **clone_args)
        print(f"Repository {repo_name} cloned to {repo_path} with task ID {task_id}.")
    except Exception as e:
        print(f"Error cloning repository {repo_url}: {e}")
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
        raise HTTPException(status_code=500, detail=f"Error cloning repository {repo_url}. {str(e)}")

@router.post("/download-repo/", status_code=202)
async def api_download_repo(download_request: DownloadRepoRequest, background_tasks: BackgroundTasks):
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    if download_request.github_token:
        headers["Authorization"] = f"token {download_request.github_token}"

    if not os.path.exists(download_request.output_dir):
        os.makedirs(download_request.output_dir, exist_ok=True)
    
    task_id = str(uuid4())

    background_tasks.add_task(download_repo, task_id, download_request.repo_url, download_request.output_dir, download_request.github_token, download_request.clone_depth, download_request.branch)
    
    return {"message": "Download initiated", "task_id": task_id}