from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
import os
import requests
import json
from scripts.utils import get_token

CREATE_SESSION_URL = os.environ['CREATE_SESSION_URL']


def session_from_rest(callback_url: str, introDisabled: bool = False):
    """
    Create a session from a REST API callback.

    Args:
        callback_url (str): The URL to which the callback should be made.
        introDisabled (bool, optional): Flag indicating whether the intro should be disabled. Defaults to False.

    Returns:
        dict: The response from the API call.

    Raises:
        HTTPException: If the API call returns a non-200 status code.

    Example usage:
        callback_url = "https://example.com/callback"
        introDisabled = False
        session_from_rest(callback_url, introDisabled)
    """

    # get token from IC auth service to use in API when creating session
    access_token = get_token()

    # here you can prepare your query params like steps and their order, session expiration, etc.
    # TODO: example of how to prepare steps - change this
    steps = [
        'FrontSide',
        'Vin',
    ]

    # add query_params to callbackUrl - any of yours custom parameters you want to pass
    # this is completely optional
    query_params = {
        'vehicleType': 'personal',
        'policyNum': 123,
    }

    # prepare callbackUrl
    req = requests.models.PreparedRequest()
    req.prepare_url(callback_url, query_params)
    callbackUrl = req.url

    # prepare body of POST request to create session - more info on Swagger
    payload_dict = {
        "callbackUrl": callbackUrl,
        "steps": steps,
        "introDisabled": introDisabled,
    }

    # send request to IC
    payload = json.dumps(payload_dict)
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST",
        CREATE_SESSION_URL,
        headers=headers,
        data=payload
    )

    # try catch errors in request
    if response.status_code != 200:
        print(response.text)
        raise HTTPException(
            409,
            detail=jsonable_encoder({
                "detail": response.text
            })
        )

    if 'application/json' in response.headers.get('Content-Type'):
        return response.json()
    raise HTTPException(
        409,
        detail=jsonable_encoder({
            "detail": response.text
        })
    )
