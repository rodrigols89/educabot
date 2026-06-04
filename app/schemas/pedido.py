"""
Pedido schemas module.

Provides request and response schemas.
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PedidoCreate(BaseModel):
    """
    Manual request creation schema.
    """

    gestor_id: int
    comando: str


class PedidoResponse(BaseModel):
    """
    Request response schema.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int
    gestor_id: int
    tipo: str
    quantidade: int
    criado_em: datetime
