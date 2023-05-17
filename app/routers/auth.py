import logging
from functools import lru_cache

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse, RedirectResponse

from app import config
from app.utils.exceptions import AuthorizationException, exception_handling
from app.utils.mongo import db_client
from app.utils.security import schemes as auth_schemes
from app.utils.security import util as auth_util
from app.utils.security.providers import AzureAuthProvider

logger = logging.getLogger(__name__)

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

csrf_token_redirect_cookie_scheme = auth_schemes.CSRFTokenRedirectCookieBearer()
access_token_cookie_scheme = auth_schemes.AccessTokenCookieBearer(
    authorizationUrl="/auth/login", tokenUrl="/auth/callback"
)


@lru_cache()
def get_admin_users() -> list[str]:
    """
    Returns a list of admin users' emails from local text file.

    Returns
    -------
    admin_users : list[str]
        List of admin users' emails
    """
    if not config.PROD_ENV:
        return []

    with open("data/admin_users.txt", "r") as f:
        admin_users = f.read().splitlines()
    admin_users = [user.lower() for user in admin_users]
    return admin_users


@auth_router.get("/login")
async def login_redirect():
    """
    Endpoint for redirecting the user to the external authentication provider.
    CSRF token is generated and stored in a HTTPOnly cookie.

    Returns
    -------
    response : RedirectResponse
        Redirects the user to the external authentication provider
    """
    async with exception_handling():

        if not config.PROD_ENV:
            return RedirectResponse(url="/auth/callback")

        provider = AzureAuthProvider()

        request_uri, state_csrf_token = await provider.get_request_uri()

        response = RedirectResponse(url=request_uri)

        # Make this a secure cookie for production use
        response.set_cookie(
            key="state", value=f"Bearer {state_csrf_token}", httponly=True
        )

        return response


@auth_router.get("/callback")
async def azure_login_callback(
    request: Request, _=Depends(csrf_token_redirect_cookie_scheme)
):
    """
    Callback endpoint for the external authentication provider after the user
    has authenticated. This endpoint is called by the external provider.
    External authorization code is exchanged for an external access token. Token is
    then encoded to generate internal access token. Internal access token is stored
    in a HTTPOnly cookie.

    Parameters
    ----------
    request : Request
        The request object which contains the authorization code

    Returns
    -------
    response : RedirectResponse
        Redirects the user to the frontend home page with the internal access token
    """
    async with exception_handling():

        if not config.PROD_ENV:
            return RedirectResponse(url=config.FRONTEND_URL)

        code = request.query_params.get("code")

        if not code:
            raise AuthorizationException("Missing external authentication token")

        provider = AzureAuthProvider()

        # Exchange external authorization code for external access token
        external_access_token = await provider.get_token(external_auth_code=code)

        # Authenticate token and get user's info from external provider
        external_user = await provider.get_user(
            external_access_token=external_access_token.access_token
        )

        # Get or create the internal user
        internal_user = await db_client.get_user_by_external_id(external_user)
        if internal_user is None:
            internal_user = await db_client.create_internal_user(external_user)

        # Create internal access token
        internal_access_token = await auth_util.create_internal_access_token(
            external_access_token
        )

        # Redirect the user to the frontend
        response = RedirectResponse(url=config.FRONTEND_URL)

        # Delete state cookie. No longer required
        response.delete_cookie(key="state")

        # Assign access token cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {internal_access_token}",
            httponly=True,
            max_age=external_access_token.expires_in,
        )

        return response


@auth_router.get("/logout")
async def logout(
    _: str = Depends(access_token_cookie_scheme),
) -> JSONResponse:
    """
    Endpoint for logging out the user.
    Deletes the HTTPOnly access token cookie.

    Parameters
    ----------
    _ : str
        Azure access token

    Returns
    -------
    response : JSONResponse
        A JSON response with the status of the user's session
    """
    async with exception_handling():
        response = JSONResponse(
            content=jsonable_encoder(
                {
                    "userLoggedIn": False,
                }
            ),
        )

        response.delete_cookie(key="access_token")

        return response


@auth_router.get("/me")
async def user_session_status(
    external_access_token: str = Depends(access_token_cookie_scheme),
    admin_users: list[str] = Depends(get_admin_users),
) -> JSONResponse:
    """
    Endpoint for checking the status of the user's session based on validity
    of HTTPOnly access token cookie.

    Parameters
    ----------
    external_access_token : str
        Azure access token
    admin_users : list[str]
        List of admin users' emails

    Returns
    -------
    response : JSONResponse
        A JSON response with the status of the user's session
    """
    async with exception_handling():

        if not config.PROD_ENV:
            return JSONResponse(
                content=jsonable_encoder(
                    {"userLoggedIn": True, "userName": "Test User", "isAdmin": True}
                ),
            )

        provider = AzureAuthProvider()
        external_user = await provider.get_user(
            external_access_token=external_access_token
        )
        internal_user = await db_client.get_user_by_external_id(external_user)

        logged_id = True if internal_user else False

        is_admin = True if external_user.email in admin_users else False

        response = JSONResponse(
            content=jsonable_encoder(
                {
                    "userLoggedIn": logged_id,
                    "userName": external_user.username,
                    "isAdmin": is_admin,
                }
            ),
        )

        return response
