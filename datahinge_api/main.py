from fastapi import FastAPI
from git import git_clone
from databases import postgres
from dockerutil import dockerutil

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Depends

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

app.include_router(git_clone.router)
app.include_router(postgres.router)
app.include_router(dockerutil.router)
