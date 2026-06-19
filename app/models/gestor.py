# app/models/gestor.py

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)

from app.db.base import Base


class Gestor(Base):

    __tablename__ = "gestores"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    nome = Column(
        String(255),
        nullable=False,
    )

    telefone = Column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )

    instituicao = Column(
        String(255),
        nullable=False,
    )

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
