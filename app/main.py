from fastapi import FastAPI

from app.routers.skills import skills_router

app = FastAPI()

app.include_router(skills_router, prefix="/skills", tags=["Skills"])

@app.get("/health", tags=["health_check"])
def health_check():
    """Health check"""
    return {"message": "Server is healthy"}