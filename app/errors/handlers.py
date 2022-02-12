from flask import jsonify
from flask import json
from werkzeug.http import HTTP_STATUS_CODES
from werkzeug.exceptions import HTTPException


def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    print(e)
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({"code": e.code, "name": e.name})
    response.content_type = "application/json"
    return response


def error_response(status_code: int, message=None) -> str:
    """
    A catch all function which returns the error code and message back to the user

    Parameters
    ----------
    status_code : int
        The HTTP status code
    message : str, optional
        The error message, by default None

    Returns
    -------
    str
        A JSON object containing the error information and HTTP code
    """
    payload = {"error": HTTP_STATUS_CODES.get(status_code, "Unknown error")}

    if message:
        payload["msg"] = message

    response = jsonify(payload)
    response.status_code = status_code

    return response


def bad_request(message: str) -> str:
    """
    Returns a 400 error code when a bad request has been made

    Parameters
    ----------
    message : str
        The error message

    Returns
    -------
    str
        A JSON object containing the error message and a 400 HTTP code
    """
    return error_response(400, message)


def not_found(message: str) -> str:
    """
    Returns a 404 error code when a object not found

    Parameters
    ----------
    message : str
        The error message

    Returns
    -------
    str
        A JSON object containing the error message and a 404 HTTP code
    """
    return error_response(404, message)
