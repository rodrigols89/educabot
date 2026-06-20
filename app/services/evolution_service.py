# app/services/evolution_service.py

import requests

from app.core.config import settings


def send_text_message(
    phone: str,
    message: str,
) -> bool:

    url = (
        f"{settings.EVOLUTION_API_URL}"
        f"/message/sendText/"
        f"{settings.EVOLUTION_INSTANCE}"
    )

    payload = {
        "number": phone,
        "text": message,
    }

    headers = {
        "apikey": settings.AUTHENTICATION_API_KEY,
        "Content-Type": "application/json",
    }

    print(
        "\n========================================"
    )
    print("EVOLUTION REQUEST")
    print(
        "========================================"
    )
    print(f"URL: {url}")
    print(f"PHONE: {phone}")
    print(f"PAYLOAD: {payload}")
    print(
        "========================================"
    )

    try:

        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        print(
            "\n========================================"
        )
        print("EVOLUTION RESPONSE")
        print(
            "========================================"
        )
        print(
            f"STATUS: {response.status_code}"
        )
        print(
            f"BODY: {response.text}"
        )
        print(
            "========================================\n"
        )

        return response.status_code in (
            200,
            201,
        )

    except Exception as error:

        print(
            "\n========================================"
        )
        print("EVOLUTION ERROR")
        print(
            "========================================"
        )
        print(error)
        print(
            "========================================\n"
        )

        return False

"""
# driver.py

from app.services.evolution_service import (
    send_text_message,
)

success = send_text_message(
    phone="558393858828",
    message=(
        "Teste de envio "
        "pelo EducaBot"
    ),
)

print(
    "\n========================================"
)

print(
    "RESULTADO"
)

print(
    "========================================"
)

print(
    f"Mensagem enviada: {success}"
)

print(
    "========================================\n"
)
"""
