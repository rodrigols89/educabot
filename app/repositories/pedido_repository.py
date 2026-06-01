"""
Pedido repository module.

Provides database operations related to requests.
"""

from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.pedido import Pedido


def exists_request_today(
    db: Session,
    gestor_id: int,
    request_type: str,
) -> bool:
    """
    Check if a request already exists today.

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
        True if request already exists.

    Examples
    --------
    >>> exists_request_today(db, 1, "gas")
    True
    """

    # Get "start" and "end" of day
    start_of_day = datetime.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    # Get "end" of day
    end_of_day = start_of_day + timedelta(days=1)

    # Check if request already exists
    return (
        db.query(Pedido)
        .filter(Pedido.gestor_id == gestor_id)
        .filter(Pedido.tipo == request_type)
        .filter(Pedido.criado_em >= start_of_day)
        .filter(Pedido.criado_em < end_of_day)
        .first()
        is not None
    )
