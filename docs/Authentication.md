# Microsoft Authentication

This app utilises Microsoft authentication to allow users to sign in to the app, avoiding the need for users to remember a separate set of login credentials.

## Overview

When a user logs in, they are redirected to the Microsoft login page. Once they have logged in, they are redirected back to the app, where the app validates the token and creates a session for the user.

Authentication was implemented in the FastAPI backend using the Python `msal` library. This was done to avoid storing the client ID and client secret in the frontend, which would be exposed to the user.

## Set up

Setting up this app for Microsoft authentication required an app to be registered in the Azure AD Portal. The app was registered as a `web app` using the steps outlined [here](https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app). Only users from within the organisation are able to log into this app.

In doing so, the app was assigned a client ID and client secret. These are used to authenticate the app when it requests a token from the Microsoft authentication service. A redirect URI was also set up, which is used to redirect the user back to the app after they have logged in.

The following environment variables are used to configure the app for Microsoft authentication:

```
AZURE_CLIENT_ID
AZURE_CLIENT_SECRET
AZURE_TENANT_ID
AZURE_REDIRECT_URI
```

Additional environment variables are also required for the whole authentication flow. These are:

```
JWT_SECRET_KEY
SESSION_SECRET_KEY
```

## Flow

Four endpoints were created to handle authentication:

### `/login`

This endpoint is used to redirect the user to the Microsoft login page. The user is provided with the external authentication URL along with a custom `state` parameter, which is used to validate the response from the login page.

### `/callback`

Once the user has entered their credentials and logged in, they are redirected back to this endpoint in the app. This is the endpoint that is defined by the `AZURE_REDIRECT_URI`. The app validates the `state` parameter stored in the response cookie, and then requests an access token from the Microsoft authentication service using the authentication code that is returned as a query parameter.

This external access token is then encoded with `jwt` to form an internal access token that is used to authenticate the user. This internal access token is stored in a HttpOnly cookie, which is then used to validate the user's session.

The endpoint finishes by returning a redirect response to the frontend, which contains the internal access token cookie.

NOTE: This redirect reponse is necessary because the frontend is not permitted to perform a GET request on the external authentication URL supplied by the previous `/login` endpoint. A CORS error is thrown by Microsoft because the request is being performed by a different origin. The frontend must instead **_navigate_** to the external authentication URL, which is why the redirect response is necessary.

### `/logout`

This endpoint is used to log the user out of the app. It clears the internal access token cookie, which invalidates the user's session.

### `/me`

This endpoint is used to retrieve the user's details. The endpoint is only accessible to authenticated users.

### Any other request

For all other requests, the internal access token must be a cookie in the request. If the cookie is not present, or the cookie is invalid, the request is denied and the frontend should handle a redirect to the login page.

With every request, the internal access token is decoded to generate the external access token. Validation of this external access token still needs to be configured but for now, the ability to decode the token using the app's `JWT_SECRET_KEY` is sufficient.
