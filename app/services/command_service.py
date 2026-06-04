"""
Command parsing service.

Responsible for interpreting incoming commands.
"""

from typing import Dict

from app.utils.regex import validate_request_command


def parse_command(command: str) -> Dict[str, int | str]:
    """
    Parse incoming request command.

    Parameters
    ----------
    command : str
        Incoming request command.

    Returns
    -------
    Dict[str, int | str]
        Parsed request information.

    Raises
    ------
    ValueError
        If command format is invalid.

    Examples
    --------
    >>> parse_command("/gas")
    {"tipo": "gas", "quantidade": 1}
    """

    # Validate command format
    if not validate_request_command(command):
        raise ValueError("Invalid command format.")

    # Remove leading and trailing spaces
    cleaned_command = command.strip()

    # Extract request type
    request_type = cleaned_command.replace("/", "")

    # Return parsed request information
    return {
        "tipo": request_type,
        "quantidade": 1,
    }
