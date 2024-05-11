from fastapi import FastAPI, HTTPException, APIRouter
from typing import List, Dict
import docker

router = APIRouter()

client = docker.DockerClient(base_url='unix://var/run/docker.sock') 
# Add Windows support

@router.post("/containers/", response_model=str, status_code=201)
def create_container(image: str, name: str):
    try:
        container = client.containers.create(image, name=name)
        container.start()
        return f"Container {name} created successfully"
    except docker.errors.ImageNotFound:
        raise HTTPException(status_code=404, detail=f"Image {image} not found")
    except docker.errors.APIError as e:
        raise HTTPException(status_code=500, detail=f"Error creating container: {e.explanation}")

@router.get("/containers/", status_code=200)
def list_containers() -> List[Dict[str, str]]:
    containers = client.containers.list(all=True)
    return [{"name": container.name, "id": container.id} for container in containers]

@router.get("/containers/{name}", response_model=str, status_code=200)
def get_container(name: str):
    try:
        container = client.containers.get(name)
        return f"Container {name} found"
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {name} not found")

@router.delete("/containers/{name}", status_code=204)
def delete_container(name: str):
    try:
        container = client.containers.get(name)
        container.remove()
        return {"message": "Container deleted successfully"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {name} not found")

@router.post("/containers/{name}/restart", status_code=204)
def restart_container(name: str):
    try:
        container = client.containers.get(name)
        container.restart()
        return {"message": "Container restarted successfully"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {name} not found")

@router.post("/containers/{name}/stop", status_code=204)
def stop_container(name: str):
    try:
        container = client.containers.get(name)
        container.stop()
        return {"message": "Container stopped successfully"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {name} not found")

@router.post("/containers/{name}/start", status_code=204)
def start_container(name: str):
    try:
        container = client.containers.get(name)
        container.start()
        return {"message": "Container started successfully"}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail=f"Container {name} not found")
