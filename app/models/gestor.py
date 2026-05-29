"""
Gestor model module.

This module defines the database model responsible for storing
authorized managers that can interact with the system.
"""

from sqlalchemy import Boolean, Column, Integer, String

from app.db.base import Base


class Gestor(Base):
    """
    Manager database model.

    Stores information about authorized managers and their
    permissions within the system.

    Attributes
    ----------
    id : int
        Primary key identifier.

    nome : str
        Manager full name.

    telefone : str
        Unique manager phone number.

    escola : str
        School associated with the manager.

    pode_pedir_gas : bool
        Defines if the manager can request gas.

    pode_pedir_agua : bool
        Defines if the manager can request water.

    ativo : bool
        Indicates if the manager is active.
    """

    __tablename__ = "gestores"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(255), nullable=False)

    telefone = Column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )

    escola = Column(String(255), nullable=False)

    pode_pedir_gas = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    pode_pedir_agua = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    ativo = Column(
        Boolean,
        default=True,
        nullable=False,
    )
