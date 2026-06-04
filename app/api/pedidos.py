"""
Request endpoints module.

Provides API endpoints for request operations.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.gestor import Gestor
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoResponse
from app.services.pedido_service import create_request

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
)


@router.post(
    "",
    response_model=PedidoResponse,
    status_code=201,
)
def create_request_endpoint(
    payload: PedidoCreate,
    db: Session = Depends(get_db),
) -> Pedido:
    """
    Create a request manually.
    """

    gestor = (
        db.query(Gestor)
        .filter(Gestor.id == payload.gestor_id)
        .first()
    )

    if gestor is None:
        raise HTTPException(
            status_code=404,
            detail="Manager not found.",
        )

    try:
        return create_request(
            db=db,
            gestor=gestor,
            command=payload.comando,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[PedidoResponse],
)
def list_requests(
    db: Session = Depends(get_db),
) -> list[Pedido]:
    """
    List all requests.
    """

    return db.query(Pedido).all()
