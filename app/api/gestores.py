from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.gestor import Gestor
from app.schemas.gestor import GestorCreate, GestorResponse

router = APIRouter(
    prefix="/gestores",
    tags=["Gestores"],
)


@router.post(
    "",
    response_model=GestorResponse,
    status_code=201,
)
def create_manager(
    payload: GestorCreate,
    db: Session = Depends(get_db),
) -> Gestor:
    """
    Create a new manager.

    Parameters
    ----------
    payload : GestorCreate
        Manager creation payload.

    Returns
    -------
    Gestor
        Created manager.
    """

    # Gestor model instance
    gestor = Gestor(**payload.model_dump())
    db.add(gestor)  # add to db
    db.commit()  # save
    db.refresh(gestor)  # refresh

    return gestor


@router.get(
    "",
    response_model=list[GestorResponse],
)
def list_managers(
    db: Session = Depends(get_db),
) -> list[Gestor]:
    """
    List all managers.

    Returns
    -------
    list[Gestor]
        Registered managers.
    """

    return db.query(Gestor).all()
