"""
Log model module.

This module defines the database model responsible for storing
system logs and audit information.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.base import Base


class Log(Base):
    """
    System log database model.

    Stores operational logs and audit records.

    Attributes
    ----------
    id : int
        Primary key identifier.

    telefone : str
        Sender phone number.

    mensagem : str
        Incoming message content.

    resposta : str
        System response message.

    criado_em : datetime
        Log creation timestamp.
    """

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    telefone = Column(
        String(20),
        nullable=False,
    )

    mensagem = Column(
        Text,
        nullable=False,
    )

    resposta = Column(
        Text,
        nullable=True,
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
