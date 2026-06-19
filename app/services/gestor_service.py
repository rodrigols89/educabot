# app/services/gestor_service.py

from sqlalchemy.orm import Session

from app.models.gestor import Gestor
from app.repositories.gestor_repository import (
    get_gestor_by_phone,
)

def find_gestor(
    db: Session,
    phone: str,
) -> Gestor | None:
    """
    Find manager by phone number.
    """

    return get_gestor_by_phone(
        db=db,
        phone=phone,
    )
