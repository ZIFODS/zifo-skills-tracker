import logging

from fastapi import APIRouter, Depends, Request
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse, RedirectResponse

from app import config
from app.models.auth import ExternalAuthToken, InternalAccessTokenData, InternalUser
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


@auth_router.get("/login")
async def login_redirect():
    """
    Endpoint for redirecting the user to the external authentication provider.
    CSRF token is generated and stored in a HTTPOnly cookie.

    Returns
    -------
    response: RedirectResponse
        Redirects the user to the external authentication provider
    """
    async with exception_handling():
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
    then used to get user's info from external provider. Internal user is created if
    it does not exist. Internal access token is created and returned to the user in a
    HTTPOnly cookie.

    Parameters
    ----------
    request: Request
        The request object which contains the authorization code

    Returns
    -------
    response: RedirectResponse
        Redirects the user to the frontend home page
    """
    async with exception_handling():
        code = request.query_params.get("code")

        if not code:
            raise AuthorizationException("Missing external authentication token")

        provider = AzureAuthProvider()

        # Authenticate token and get user's info from external provider
        external_user = await provider.get_user(auth_token=ExternalAuthToken(code=code))

        # Get or create the internal user
        internal_user = await db_client.get_user_by_external_sub_id(external_user)
        if internal_user is None:
            internal_user = await db_client.create_internal_user(external_user)

        # Create internal access token
        access_token = await auth_util.create_internal_access_token(
            InternalAccessTokenData(
                sub=internal_user.internal_sub_id,
            )
        )

        # Redirect the user to the frontend
        response = RedirectResponse(url=config.FRONTEND_URL)

        # Delete state cookie. No longer required
        response.delete_cookie(key="state")

        # Assign access token cookie
        response.set_cookie(
            key="access_token",
            value=f"Bearer {access_token}",
            httponly=True,
            max_age=3600,
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
    internal_user: InternalUser
        Internal user object

    Returns
    -------
    response: JSONResponse
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
    internal_user: InternalUser = Depends(access_token_cookie_scheme),
) -> JSONResponse:
    """
    Endpoint for checking the status of the user's session based on validity
    of HTTPOnly access token cookie.

    Parameters
    ----------
    internal_user: InternalUser
        Internal user object

    Returns
    -------
    response: JSONResponse
        A JSON response with the status of the user's session
    """
    async with exception_handling():
        logged_id = True if internal_user else False

        response = JSONResponse(
            content=jsonable_encoder(
                {
                    "userLoggedIn": logged_id,
                    "userName": internal_user.username,
                }
            ),
        )

        return response
