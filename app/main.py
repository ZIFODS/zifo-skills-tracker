from fastapi import FastAPI

from app.routers.skills import skills_router

app = FastAPI()

app.include_router(skills_router, prefix="/skills", tags=["Skills"])