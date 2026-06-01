"""
Permission validation service.

Responsible for validating manager permissions.
"""

from app.models.gestor import Gestor


def validate_permission(
    gestor: Gestor,
    request_type: str,
) -> bool:
    """
    Validate manager request permission.

    Parameters
    ----------
    gestor : Gestor
        Manager instance.

    request_type : str
        Request type.

    Returns
    -------
    bool
        True if permission is granted.

    Examples
    --------
    >>> validate_permission(gestor, "gas")
    True
    """

    if request_type == "gas":
        return gestor.pode_pedir_gas

    if request_type == "agua":
        return gestor.pode_pedir_agua

    return False
