"""
Regex utility module.

Provides reusable regex validation helpers for command parsing.
"""

import re

REQUEST_COMMAND_PATTERN = r"^\/(gas|agua)\s+\d+$"


def validate_request_command(command: str) -> bool:
    """
    Validate request command format.

    Parameters
    ----------
    command : str
        Incoming request command.

    Returns
    -------
    bool
        True if command format is valid.

    Examples
    --------
    >>> validate_request_command("/gas 2")
    True
    """

    return bool(
        re.match(
            REQUEST_COMMAND_PATTERN,
            command.strip(),
        )
    )
