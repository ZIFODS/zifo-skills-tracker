import requests
import time

from app.config import PRIMA_DATA_URL, PRIMA_AUTH_URL, PRIMA_AUTH_PAYLOAD

# Define authentication details
print(PRIMA_AUTH_PAYLOAD)
print(PRIMA_AUTH_URL, PRIMA_DATA_URL)
auth_url = PRIMA_AUTH_URL
data_url = PRIMA_DATA_URL

auth_payload = PRIMA_AUTH_PAYLOAD

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
        print("Retrieved data!")
    else:
        print("Data retrieval failed.")
else:
    print("Authentication failed, unable to retrieve data.")