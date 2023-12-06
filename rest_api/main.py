import os
import fastapi
import logging
from fastapi import FastAPI, Request, BackgroundTasks
from rest_api.types.types import CreateSessionResponse, SessionParams
from scripts.finished_session_handler import finished_session_from_rest
from scripts.session_creator import session_from_rest


app = FastAPI()


# Define the filter for healthz EP - we do not want to spam logs with healtz requests
class EndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/healthz"


@app.get('/healthz', status_code=fastapi.status.HTTP_200_OK, include_in_schema=False)
def healthz():
    """
    A health check endpoint that returns a 200 OK response with the content 'ok'.

    Parameters:
        None

    Returns:
        fastapi.Response: The HTTP response object with the content 'ok'.
    """
    return fastapi.Response(content='ok')


@app.get("/create-session", response_model=CreateSessionResponse)
async def create_session(
    introDisabled: bool = False  # only example here - you can connect any parameter here to modify the session
):
    """
    Creates a session by making a GET request to the "/create-session" endpoint.

    Parameters:
        introDisabled (bool, optional): A flag indicating whether the intro is disabled for the session. Defaults to False.

    Returns:
        CreateSessionResponse: An object representing the response from the "/create-session" endpoint.
    """
    callback_url = os.getenv('CALLBACK_URL')

    create_session_response = session_from_rest(callback_url, introDisabled)
    print(create_session_response)
    # example response to pass types test of CreateSessionResponse
    # {
    #     "link": "https://instacar.dev.instacover.ai/clpts2bi80009t001ga3843dks",
    #     "sessionId": "clpts2bi80009t001ga3843dks",
    #     "expireAt": null
    # }

    return create_session_response


@app.post("/finish-session")
async def finish_session(
    request: Request,  # request object itself
    session_params: SessionParams,  # body of response
    background_tasks: BackgroundTasks  # this is here as a functionality of fastapi to process the request asynchronously
    # TODO: add any of your custom query params here
):
    """
    Finish the session and process the request asynchronously.

    Parameters:
        - request (Request): The request object itself.
        - session_params (SessionParams): The body of the response.
        - background_tasks (BackgroundTasks): This is here as a functionality of FastAPI to process the request asynchronously.

    Returns:
        - bool: True if the session is finished successfully.
    """
    session_params = session_params.dict()

    print(session_params)

    # TODO: connect your code here - downloading of photos, business rules, upload to your systems, etc.
    # example of such code with use of background_tasks
    finished_session_from_rest(
        session_params,
        background_tasks
    )

    return True  # to process the request asynchronously
