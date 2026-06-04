"""
Gestor schemas module.

Provides request and response schemas for manager operations.
"""

from pydantic import BaseModel, ConfigDict


class GestorCreate(BaseModel):
    """
    Manager creation schema.
    """

    nome: str
    telefone: str
    escola: str
    pode_pedir_gas: bool
    pode_pedir_agua: bool


class GestorResponse(BaseModel):
    """
    Manager response schema.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    telefone: str
    escola: str
    pode_pedir_gas: bool
    pode_pedir_agua: bool
    ativo: bool
