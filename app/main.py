from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth import auth_router
from app.routers.skills import skills_router

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(skills_router, prefix="/skills", tags=["Skills"])


@app.get("/health", tags=["health_check"])
def health_check():
    """Health check"""
    return {"message": "Server is healthy"}
