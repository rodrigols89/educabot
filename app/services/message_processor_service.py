"""
Message processing service.

Handles incoming WhatsApp messages and
routes them to business rules.
"""

from app.schemas.evolution import EvolutionMessage


def process_message(
    message: EvolutionMessage,
) -> str:
    """
    Process incoming WhatsApp message.

    Parameters
    ----------
    message : EvolutionMessage
        Parsed Evolution message.

    Returns
    -------
    str
        Processing result message.

    Examples
    --------
    >>> process_message(message)
    'Command received'
    """

    # Ignore messages sent by ourselves
    if message.from_me:
        return "Ignored own message"

    # Ignore empty messages
    if not message.text:
        return "Empty message"

    # Command detection
    if message.text.startswith("/"):
        return "Command received"

    return "Not a command"
