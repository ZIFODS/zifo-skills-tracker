from fastapi import Request
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer

from app.models.auth import InternalUser
from app.utils.exceptions import UnauthorizedUser, exception_handling
from app.utils.security import util as auth_util


class CSRFTokenRedirectCookieBearer:
    """
    Scheme that checks the validity of the state parameter returned by the
    Authentication provider when it redirects the user to the application after
    a successful sign in.
    """

    async def __call__(self, request: Request) -> None:
        async with exception_handling():
            # State token from redirect
            state_csrf_token: str = request.query_params.get("state")
            # State token from cookie
            state_csrf_token_cookie: str = request.cookies.get("state")

            if not state_csrf_token_cookie:
                raise UnauthorizedUser("Invalid state token")

            # Remove Bearer
            state_csrf_token_cookie = state_csrf_token_cookie.split()[1]

            await auth_util.validate_state_csrf_token(
                state_csrf_token, state_csrf_token_cookie
            )


class AccessTokenCookieBearer(OAuth2AuthorizationCodeBearer):
    """
    Scheme that checks the validity of the access token that is stored to an
    HTTPOnly secure cookie to authorize the user.
    """

    async def __call__(self, request: Request) -> InternalUser:
        async with exception_handling():
            internal_access_token: str = request.cookies.get("access_token")
            if not internal_access_token:
                raise UnauthorizedUser("Invalid access token cookie")

            # Remove Bearer
            internal_access_token = internal_access_token.split()[1]
            external_access_token = await auth_util.validate_internal_access_token(
                internal_access_token
            )

            return external_access_token
