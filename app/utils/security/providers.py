import logging
from typing import Tuple

import requests
from msal import ConfidentialClientApplication

from app import config
from app.models.auth import ExternalAuthToken, ExternalUser
from app.utils.exceptions import ProviderConnectionError, UnauthorizedUser
from app.utils.security.util import create_state_csrf_token

logger = logging.getLogger(__name__)


class AzureAuthProvider:
    """Azure authentication class for authenticating users and requesting user's information"""

    async def get_user(self, auth_token: ExternalAuthToken) -> ExternalUser:
        """Receives an authentication token from Microsoft Azure and exchanges it for an access token.
        It then retrieves the user's details from the Azure user-info endpoint.

        Parameters
        ----------
        auth_token : ExternalAuthToken
            The authentication token received from Azure

        Returns
        -------
        ExternalUser
            A user object with the details of the user's account as it is stored in Azure
        """
        msal_client = ConfidentialClientApplication(
            config.AZURE_CLIENT_ID,
            authority=config.AZURE_AUTHORITY,
            client_credential=config.AZURE_CLIENT_SECRET,
        )

        # Request access_token from Azure
        try:
            result = msal_client.acquire_token_by_authorization_code(
                auth_token.code,
                redirect_uri=config.AZURE_REDIRECT_URL,
                scopes=["User.Read"],
            )

            access_token = result["access_token"]

        except Exception as exc:
            raise ProviderConnectionError(
                f"Could not get Azure's access token: {repr(exc)}"
            )

        # Request user's information from Azure
        userinfo_response = requests.get(
            # Currently userinfo_endpoint only returns "sub". We need to use /v1.0/me for other info
            "https://graph.microsoft.com/v1.0/me",
            headers={"Authorization": "Bearer " + access_token},
        )

        response_data = userinfo_response.json()
        username = response_data.get("userPrincipalName")
        if not username:
            raise UnauthorizedUser("User account not verified by Azure.")

        email = response_data.get("mail")
        if not email:
            raise UnauthorizedUser("User account not verified by Azure.")

        sub_id = result["id_token_claims"]["sub"]

        external_user = ExternalUser(
            email=email, username=username, external_sub_id=sub_id
        )

        return external_user

    async def get_request_uri(self) -> Tuple[str, str]:
        """Returns Microsoft authentication URL for sign in.

        Returns
        -------
        Tuple[str, str]
            request_uri: Sign in pop-up URL
            state_csrf_token: CSRF token
        """
        msal_client = ConfidentialClientApplication(
            config.AZURE_CLIENT_ID,
            authority=config.AZURE_AUTHORITY,
            client_credential=config.AZURE_CLIENT_SECRET,
        )

        state_csrf_token = await create_state_csrf_token()

        request_uri = msal_client.get_authorization_request_url(
            scopes=["User.Read"],
            state=state_csrf_token,
            redirect_uri=config.AZURE_REDIRECT_URL,
        )

        return request_uri, state_csrf_token
