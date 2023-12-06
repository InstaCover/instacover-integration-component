import os
import requests
import urllib

GET_TOKEN_URL = os.environ['GET_TOKEN_URL']
CLIENT_ID = os.environ['CLIENT_ID']
CLIENT_SECRET = os.environ['CLIENT_SECRET']


def get_token():
    """
    Retrieves an access token for authentication.

    Returns:
        str: The access token required for authentication.
    """

    payload = f'grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={urllib.parse.quote_plus(CLIENT_SECRET)}&scope=categorization'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    response = requests.request(
        "POST",
        GET_TOKEN_URL,
        headers=headers,
        data=payload
    )
    rsp = response.json()
    try:
        access_token = rsp['access_token']
    except Exception:
        print('Error creating token:', rsp)

    return access_token
