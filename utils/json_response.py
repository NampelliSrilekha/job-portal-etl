import logging

logging.basicConfig(level=logging.DEBUG)
def success_response(message, data=None, status=200):
    """
    Generate a success response with a responseCode.
    
    :param message: Success message.
    :param data: Optional data to include in response.
    :param status: HTTP status code (default: 200).
    :return: JSON-formatted success response.
    """
    response = {
        "status": "success",
        "responseCode": status,
        "message": message,
        "data": data if data is not None else []  # Ensure data is an empty list if None
    }
    logging.debug(f"Response: {response}") 
    return response


def error_response(message, status=400):
    """
    Generate an error response with a responseCode.
    
    :param message: Error message.
    :param status: HTTP status code (default: 400).
    :return: JSON-formatted error response.
    """
    return {
        "status": "error",
        "responseCode": status,
        "message": message
    }


def object_to_json(obj, exclude_fields=None):
    """
    Convert an object to a JSON-compatible dictionary.

    :param obj: The object to convert.
    :param exclude_fields: List of fields to exclude from the JSON output.
    :return: JSON-compatible dictionary.
    """
    if not obj:
        return None

    if exclude_fields is None:
        exclude_fields = []

    return {
        key: value for key, value in obj.__dict__.items() if key not in exclude_fields
    }


def list_to_json(obj_list, exclude_fields=None):
    """
    Convert a list of objects to a list of JSON-compatible dictionaries.

    :param obj_list: List of objects to convert.
    :param exclude_fields: Fields to exclude from each object.
    :return: List of JSON-compatible dictionaries.
    """
    return [object_to_json(obj, exclude_fields) for obj in obj_list]