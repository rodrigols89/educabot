"""
Gestor repository module.

Provides database operations related to managers.
"""

from typing import Optional

from sqlalchemy.orm import Session

from app.models.gestor import Gestor


def get_gestor_by_phone(
    db: Session,
    phone: str,
) -> Optional[Gestor]:
    """
    Retrieve manager by phone number.

    Parameters
    ----------
    db : Session
        Active database session.

    phone : str
        Manager phone number.

    Returns
    -------
    Optional[Gestor]
        Manager instance if found.

    Examples
    --------
    >>> get_gestor_by_phone(db, "+558399999999")
    """

    return (
        db.query(Gestor)
        .filter(Gestor.telefone == phone)
        .first()
    )
