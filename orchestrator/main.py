import os
import subprocess
import uuid
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()
# os.makedirs("downloads", exist_ok=True)
# os.makedirs("workspaces", exist_ok=True)
# app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACES_DIR = os.path.join(BASE_DIR, "workspaces")
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
AGENT_DIR = os.path.join(BASE_DIR, "agent")

os.makedirs(WORKSPACES_DIR, exist_ok=True)
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

app.mount("/downloads", StaticFiles(directory=DOWNLOADS_DIR), name="downloads")

jobs = {}

class TaskRequest(BaseModel):
    task: str

@app.post("/submit")
async def submit_task(req: TaskRequest):
    job_id = str(uuid.uuid4())
    workspace_dir = os.path.join(WORKSPACES_DIR, job_id)
    os.makedirs(workspace_dir, exist_ok=True)

    agent_files = ["agent_start.sh", "context_manager.py"]
    
    for file_name in agent_files:
        source_path = os.path.join(AGENT_DIR, file_name)
        dest_path = os.path.join(workspace_dir, file_name)
        if os.path.exists(source_path):
            shutil.copy2(source_path, dest_path)
            
            if file_name.endswith('.sh'):
                os.chmod(dest_path, 0o755)

    cmd = [
        "docker", "run", "-d",
        "--name", job_id,
        "-v", f"{os.path.abspath(workspace_dir)}:/workspace",
        "-e", f"TASK={req.task}",
        "agent-image"
    ]
    subprocess.run(cmd, check=True)
    jobs[job_id] = {"status": "running", "workspace": workspace_dir}
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    job = jobs[job_id]
    workspace_dir = job["workspace"]
    done_file = os.path.join(workspace_dir, "DONE")
    if os.path.exists(done_file):
        zip_path = os.path.join(DOWNLOADS_DIR, f"{job_id}.zip")
        shutil.make_archive(zip_path.replace('.zip', ''), 'zip', workspace_dir)
        subprocess.run(["docker", "stop", job_id], check=False)
        subprocess.run(["docker", "rm", job_id], check=False)
        shutil.rmtree(workspace_dir)
        job["status"] = "completed"
        return {"status": "completed", "download_link": f"/downloads/{job_id}.zip"}
    return {"status": "running"}
