"""
Gestor repository.

Provides database access methods for Gestor entities.
"""

from sqlalchemy.orm import Session

from app.models.gestor import Gestor


def get_gestor_by_phone(
    db: Session,
    phone: str,
) -> Gestor | None:
    """
    Find gestor by phone number.

    Parameters
    ----------
    db : Session
        Database session.

    phone : str
        WhatsApp phone number.

    Returns
    -------
    Gestor | None
        Found gestor or None.

    Examples
    --------
    >>> get_gestor_by_phone(
    ...     db,
    ...     "5583999999999"
    ... )
    """

    return (
        db.query(Gestor)
        .filter(Gestor.telefone == phone)
        .first()
    )
