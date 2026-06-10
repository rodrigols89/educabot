"""
Evolution message schemas.
"""

from pydantic import BaseModel


class EvolutionMessage(BaseModel):
    """
    Normalized Evolution message.

    Attributes
    ----------
    phone : str
        Sender phone number.

    text : str
        Message content.
    """

    phone: str
    text: str
