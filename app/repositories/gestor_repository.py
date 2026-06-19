# app/repositories/gestor_repository.py

from sqlalchemy.orm import Session

from app.models.gestor import Gestor


def get_gestor_by_phone(
    db: Session,
    phone: str,
) -> Gestor | None:

    return (
        db.query(Gestor)
        .filter(
            Gestor.telefone == phone
        )
        .first()
    )

"""
driver.py

from sqlalchemy.orm import Session

from app.models.gestor import Gestor


def get_gestor_by_phone(
    db: Session,
    phone: str,
) -> Gestor | None:

    return (
        db.query(Gestor)
        .filter(
            Gestor.telefone == phone
        )
        .first()
    )
"""
