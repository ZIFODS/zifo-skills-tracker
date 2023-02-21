import hashlib
import logging
import os

from jwt import PyJWTError
from jwt import decode as jwt_decode
from jwt import encode as jwt_encode

from app import config
from app.models.auth import ExternalToken
from app.utils.cache import cache
from app.utils.exceptions import UnauthorizedUser
from app.utils.mongo import MongoClient

# Initialize db client
db_client = MongoClient()

logger = logging.getLogger(__name__)


async def create_state_csrf_token() -> str:
    """
    Creates a CSRF token to mitigate CSRF attacks on redirects from
    from the Authentication provider.

    The token is added in an HTTPOnly, secure cookie on the browser
    and also passed to the Auth provider as a "state" parameter.
    When the Auth provider redirects the user back to our service,
    we check that the HTTPOnly cookie value matches the "state" value
    returned by the Auth provider. We also check that we did add this
    token in the cache at some time in the past.


    Returns
    -------
    state_csrf_token : str
        The CSRF token
    """
    state_csrf_token = hashlib.sha256(os.urandom(1024)).hexdigest()

    # Values not necessary. We only need to check for existence
    await cache.set(state_csrf_token, {"valid": True})

    return state_csrf_token


async def validate_state_csrf_token(
    state_csrf_token: str, state_csrf_token_cookie: str
) -> None:
    """
    Checks the validity of a state token received by the redirect url,
    against the state token that the server added in the browser cookie.

    Parameters
    ----------
    state_csrf_token : str
        The token returned in the redirect url
    state_csrf_token_cookie : str
        The token saved previously in the cookie
    """
    if state_csrf_token != state_csrf_token_cookie:
        raise UnauthorizedUser("Failed to validate state token")

    # Also, check that we 100% cached that token in the past
    cached_token = await cache.get(state_csrf_token)

    if not cached_token:
        raise UnauthorizedUser("Failed to validate against cached state token")

    await cache.delete(state_csrf_token)


async def create_internal_access_token(
    external_access_token: ExternalToken,
) -> str:
    """
    Creates a JWT access token to return to the user.

    Parameters
    ----------
    external_access_token : ExternalToken
        Azure access token

    Returns
    -------
    internal_access_token : str
        JWT encoded internal access token
    """
    to_encode = external_access_token.dict()
    return jwt_encode(to_encode, config.JWT_SECRET_KEY, algorithm=config.ALGORITHM)


async def validate_internal_access_token(internal_access_token: str) -> ExternalToken:
    """
    Checks the validity of an internal access token and decodes it.

    Parameters
    ----------
    internal_access_token : str
        JWT encoded internal access token

    Returns
    -------
    external_access_token : ExternalToken
        Azure access token
    """
    try:
        external_access_token = jwt_decode(
            internal_access_token, config.JWT_SECRET_KEY, algorithms=[config.ALGORITHM]
        )
        return ExternalToken(**external_access_token)

    except PyJWTError as exc:
        raise UnauthorizedUser(f"Failed to validate access token: {exc}")
