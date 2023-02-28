from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse

from app.config import FRONTEND_URL, SESSION_SECRET_KEY
from app.routers.auth import auth_router
from app.routers.skills import skills_router
from app.utils.exceptions import exception_handling
from app.utils.mongo import db_client

app = FastAPI()


origins = [
    FRONTEND_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET_KEY,
)

app.include_router(auth_router)
app.include_router(skills_router)


@app.get("/health", tags=["health_check"])
def health_check():
    """Health check"""
    return {"message": "Server is healthy"}


@app.on_event("startup")
async def startup_event():
    """Startup functionality"""
    async with exception_handling():
        await db_client.start_session()


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown functionality"""
    async with exception_handling():
        await db_client.end_session()
        await db_client.close_connection()


# TODO: is this needed?
@app.middleware("http")
async def setup_request(request: Request, call_next) -> JSONResponse:
    """A middleware for setting up a request. It creates a new request_id
    and adds some basic metrics.

    Args:
            request: The incoming request
            call_next (obj): The wrapper as per FastAPI docs

    Returns:
            response: The JSON response
    """
    response = await call_next(request)

    return response
