"""
Request service module.

Centralizes request creation business rules.
"""

from sqlalchemy.orm import Session

from app.models.gestor import Gestor
from app.models.pedido import Pedido, RequestType
from app.services.command_service import parse_command
from app.services.permission_service import (
    validate_permission,
)
from app.services.request_limit_service import (
    validate_daily_request,
)


def create_request(
    db: Session,
    gestor: Gestor,
    command: str,
) -> Pedido:
    """
    Create a manager request.

    Parameters
    ----------
    db : Session
        Active database session.

    gestor : Gestor
        Manager instance.

    command : str
        Incoming request command.

    Returns
    -------
    Pedido
        Created request instance.

    Raises
    ------
    ValueError
        If validation fails.

    Examples
    --------
    >>> create_request(db, gestor, "/gas")
    """

    # Parse command and extract request data
    parsed_command = parse_command(command)

    # Extract request type (gas or agua)
    request_type = parsed_command["tipo"]

    # Extract requested quantity
    quantity = parsed_command["quantidade"]

    # Check whether the manager has permission
    # to create this type of request
    has_permission = validate_permission(
        gestor=gestor,
        request_type=request_type,
    )

    # Stop execution if the manager is not allowed
    # to request the selected category
    if not has_permission:
        raise ValueError(
            "Manager does not have permission "
            f"to request '{request_type}'."
        )

    # Check whether a request of the same type
    # has already been made today
    request_allowed = validate_daily_request(
        db=db,
        gestor_id=gestor.id,
        request_type=request_type,
    )

    # Stop execution if a request already exists
    # for the same category today
    if not request_allowed:
        raise ValueError(
            f"A '{request_type}' request has already "
            f"been made today."
        )

    # Create a new request instance
    pedido = Pedido(
        gestor_id=gestor.id,
        tipo=RequestType(request_type),
        quantidade=quantity,
    )

    # Add the request to the current database session
    db.add(pedido)

    # Persist changes to the database
    db.commit()

    # Reload the object with generated fields
    # such as id and timestamps
    db.refresh(pedido)

    # Return the created request
    return pedido
