from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.skills import skills_router
from app.routers.consultants import consultants_router

app = FastAPI()

origins = [
    "http://ec2-35-176-61-224.eu-west-2.compute.amazonaws.com:3000",
    "http://localhost:3000",
    "http://react-frontend:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(skills_router, prefix="/skills", tags=["Skills"])
app.include_router(consultants_router, prefix="/consultants", tags=["Consultants"])

@app.get("/health", tags=["health_check"])
def health_check():
    """Health check"""
    return {"message": "Server is healthy"}