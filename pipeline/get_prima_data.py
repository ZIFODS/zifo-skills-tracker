import requests
import time

# Define authentication details
auth_url = "https://primacrm.kebs.app/api/auth/authenticate/refreshTokenforApplication"
data_url = "https://primacrm.kebs.app/api/employee360/openApiDetails/getOpenApiSkills"

auth_payload = {
    "client_id": "a953a28f-bd90-471e-b2e3-d18c3ccd0dfd",
    "client_secret_id": "dbea593b-5c3c-4f0b-abc5-c6ea7093008c",
    "token_unique_id": "67de45ca-7f52-40f4-acc4-7fbf8f2442f0"
}

# Define retry settings
max_retries = 3
retry_delay = 2  # seconds to wait between retries


def get_bearer_token():
    for attempt in range(1, max_retries + 1):
        try:
            auth_response = requests.post(auth_url, json=auth_payload)
            if auth_response.status_code == 200:
                token = auth_response.json().get("access_token")
                if token:
                    print(f"Token retrieved on attempt {attempt}")
                    return token
                else:
                    print("Token not found in response, check response format.")
                    return None
            else:
                print(f"Auth failed with status {auth_response.status_code}: {auth_response.text}")
        except requests.RequestException as e:
            print(f"Auth request failed on attempt {attempt}: {e}")

        # Wait before retrying
        time.sleep(retry_delay)

    # If all attempts fail
    print("Failed to retrieve token after multiple attempts.")
    return None


# Function to retrieve data with retries
def get_data_with_token(token):
    headers = {
        "Authorization": f"Bearer {token}"
    }

    for attempt in range(1, max_retries + 1):
        try:
            data_response = requests.post(data_url, headers=headers)
            if data_response.status_code == 200:
                print(f"Data retrieved on attempt {attempt}")
                return data_response.json()
            else:
                print(f"Data retrieval failed with status {data_response.status_code}: {data_response.text}")
        except requests.RequestException as e:
            print(f"Data request failed on attempt {attempt}: {e}")

        # Wait before retrying
        time.sleep(retry_delay)

    # If all attempts fail
    print("Failed to retrieve data after multiple attempts.")
    return None


# Main script execution
token = get_bearer_token()
if token:
    data = get_data_with_token(token)
    if data:
        print("Retrieved data:", data)
    else:
        print("Data retrieval failed.")
else:
    print("Authentication failed, unable to retrieve data.")