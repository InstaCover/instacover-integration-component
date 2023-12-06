import os
import traceback
import urllib.request
from typing import List

TEMP_FOLDER = os.getenv('TEMP_FOLDER', '/tmp')


def clear_temp_files(session_id: str) -> None:
    """
    Clears temporary files associated with a given session ID.

    Parameters:
        - session_id (str): The ID of the session for which temporary files need to be cleared.

    Returns:
        None
    """
    for filepath in os.listdir(TEMP_FOLDER):
        if filepath.startswith(f'{session_id}_image_'):
            os.remove(os.path.join(TEMP_FOLDER, filepath))


def download_photos(photos: List[dict], session_id: str) -> List[str]:
    """
    Downloads photos from a list of dictionaries containing photo information.

    Args:
        photos (List[dict]): A list of dictionaries containing photo information.
        session_id (str): The session ID.

    Returns:
        List[str]: A list of filepaths where the downloaded photos are saved.
    """
    filepaths = []

    for i, photo in enumerate(photos):
        download_filepath = os.path.join(TEMP_FOLDER, f"{session_id}_image_{i}_.jpg")
        filepaths.append(download_filepath)
        if os.path.exists(download_filepath):
            continue

        try:
            urllib.request.urlretrieve(photo['link'], download_filepath)
        except urllib.error.URLError:
            detail = "Cannot download session photos from storage"
            print(detail)
            raise Exception(detail)

    return filepaths


def receive_response(finished_session_response: dict):
    """
    Process the response of a finished session.

    Args:
        finished_session_response (dict): A dictionary representing the response of a finished session.

    Returns:
        None

    Raises:
        KeyError: If the 'sessionId' key is not present in the finished_session_response dictionary.

    Notes:
        - This function retrieves the session ID from the finished_session_response dictionary.
        - It sorts the 'photos' list in the finished_session_response dictionary based on the 'createdAt' key in ascending order.
        - The sorted 'photos' list is then passed to the download_photos function along with the session ID.
        - Business rules can be checked and additional actions can be performed in the section indicated in the code.
        - After the photos have been uploaded to the system, the temporary files are cleared using the clear_temp_files function.
    """

    # get sessionID
    session_id = finished_session_response['sessionId']

    # iterate through photos and download them to your machine
    finished_session_response["photos"].sort(key=lambda item: item['createdAt'], reverse=False)
    download_photos(finished_session_response['photos'], session_id)

    # check business rules here, add conditions on fraud behavior, send emails to clients etc. here

    # clear temp files of photos after beeing uploaded to your system
    clear_temp_files(session_id)


def finished_session_from_rest(ic_response: dict, background_tasks):
    """
    Calls the 'receive_response' function asynchronously to process the 'ic_response' received from the REST API.

    Args:
        ic_response (dict): The response received from the REST API.
        background_tasks: The background tasks object used to add the 'receive_response' task.

    Returns:
        bool: True if the 'receive_response' task is successfully added to the background tasks, False otherwise.
    """
    try:
        # calling it like this will process the function receive_response asynchonously,
        # so the API can return faster and is not blocking
        background_tasks.add_task(
            receive_response,  # function
            ic_response,  # function params
        )
    except Exception:
        print(traceback.format_exc())
        return False

    return True
