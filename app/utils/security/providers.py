import logging
from typing import Tuple

import requests
from msal import ConfidentialClientApplication

from app import config
from app.models.auth import ExternalToken, ExternalUser
from app.utils.exceptions import ProviderConnectionError, UnauthorizedUser
from app.utils.security.util import create_state_csrf_token

logger = logging.getLogger(__name__)


class AzureAuthProvider:
    """
    Azure authentication class for authenticating users and requesting user's information.
    """

    def __init__(self):
        self.msal_client = ConfidentialClientApplication(
            config.AZURE_CLIENT_ID,
            authority=config.AZURE_AUTHORITY,
            client_credential=config.AZURE_CLIENT_SECRET,
        )

    async def get_token(self, external_auth_code: str) -> ExternalToken:
        """
        Receives an authentication code from Microsoft Azure and exchanges it for an access token.

        Parameters
        ----------
        external_auth_code : str
            The authentication code received from Azure

        Returns
        -------
        ExternalToken
            A trimmed down access token object with the access token and the expiry time
        """
        # Request access_token from Azure
        result = self.msal_client.acquire_token_by_authorization_code(
            external_auth_code,
            redirect_uri=config.AZURE_REDIRECT_URI,
            scopes=["User.Read"],
        )

        access_token = result.get("access_token")
        expires_in = result.get("expires_in", 0)

        if not access_token or not expires_in:
            raise ProviderConnectionError(
                "Could not get Azure's access token. " "Please try again later."
            )

        return ExternalToken(access_token=access_token, expires_in=expires_in)

    async def get_user(self, external_access_token: ExternalToken) -> ExternalUser:
        """
        Receives an authentication token from Microsoft Azure and exchanges it for an access token.
        It then retrieves the user's details from the Azure user-info endpoint.

        Parameters
        ----------
        external_access_token : ExternalToken
            Azure access token

        Returns
        -------
        ExternalUser
            A user object with the details of the user's account from Azure
        """
        # Request user's information from Azure
        userinfo_response = requests.get(
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": "Bearer " + external_access_token.access_token},
        )

        response_data = userinfo_response.json()

        user_id = response_data.get("id")
        username = response_data.get("userPrincipalName")
        email = response_data.get("mail")

        if not user_id or not username or not email:
            raise UnauthorizedUser("User account not verified by Azure.")

        external_user = ExternalUser(id=user_id, email=email, username=username)

        return external_user

    async def get_request_uri(self) -> Tuple[str, str]:
        """
        Returns Microsoft authentication URL for sign in.

        Returns
        -------
        Tuple[str, str]
            request_uri: Sign in pop-up URL
            state_csrf_token: CSRF token
        """
        state_csrf_token = await create_state_csrf_token()

        request_uri = self.msal_client.get_authorization_request_url(
            scopes=["User.Read"],
            state=state_csrf_token,
            redirect_uri=config.AZURE_REDIRECT_URI,
        )

        return request_uri, state_csrf_token
