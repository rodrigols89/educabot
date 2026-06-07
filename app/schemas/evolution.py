"""
Evolution webhook schemas.

Provides normalized schemas for Evolution API payloads.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class EvolutionMessage(BaseModel):
    """
    Normalized Evolution message.

    Attributes
    ----------
    phone : str
        Sender phone number.

    text : str
        Extracted message text.

    name : str | None
        Sender display name.

    timestamp : datetime
        Message timestamp.

    from_me : bool
        Indicates if message was sent by the connected account.

    message_type : str
        Evolution message type.
    """

    phone: str = Field(...)
    text: str = Field(...)
    name: str | None = None
    timestamp: datetime
    from_me: bool
    message_type: str
