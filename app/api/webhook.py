from typing import Any

from fastapi import APIRouter, Request

from app.services.command_service import (
    is_valid_command,
)
from app.utils.evolution_parser import (
    parse_evolution_message,
)

router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"],
)


@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    payload: dict[str, Any] = await request.json()

    phone, text = parse_evolution_message(
        payload
    )

    is_command: bool = is_valid_command(
        phone=phone,
        text=text,
    )

    print(
        f"Valid Command: {is_command}"
    )
    print(
        "========================================\n"
    )

    return {
        "status": "received"
    }
