"""
Daily request validation service.

Provides request limitation rules.
"""

from sqlalchemy.orm import Session

from app.repositories.pedido_repository import (
    exists_request_today,
)


def validate_daily_request(
    db: Session,
    gestor_id: int,
    request_type: str,
) -> bool:
    """
    Validate daily request availability.

    Parameters
    ----------
    db : Session
        Active database session.

    gestor_id : int
        Manager identifier.

    request_type : str
        Request category.

    Returns
    -------
    bool
        True if request is allowed.

    Examples
    --------
    >>> validate_daily_request(db, 1, "gas")
    True
    """

    # Check if request already exists
    already_requested = exists_request_today(
        db=db,
        gestor_id=gestor_id,
        request_type=request_type,
    )

    return not already_requested
