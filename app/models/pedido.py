"""
Pedido model module.

This module defines the database model responsible for storing
system requests made by managers.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Pedido(Base):
    """
    Request database model.

    Stores all requests performed by managers.

    Attributes
    ----------
    id : int
        Primary key identifier.

    gestor_id : int
        Associated manager identifier.

    tipo : str
        Request type.

    quantidade : int
        Requested quantity.

    criado_em : datetime
        Request creation timestamp.
    """

    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)

    gestor_id = Column(
        Integer,
        ForeignKey("gestores.id"),
        nullable=False,
    )

    tipo = Column(
        String(20),
        nullable=False,
    )

    quantidade = Column(
        Integer,
        nullable=False,
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationship with manager.
    gestor = relationship("Gestor")
