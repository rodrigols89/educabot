# app/utils/evolution_parser.py

from typing import Any


def parse_evolution_message(
    payload: dict[str, Any],
) -> tuple[str | None, str | None]:

    data: dict[str, Any] = payload.get(
        "data",
        {}
    )

    key: dict[str, Any] = data.get(
        "key",
        {}
    )

    message: dict[str, Any] = data.get(
        "message",
        {}
    )

    from_me: bool = key.get(
        "fromMe",
        False,
    )

    text: str = message.get(
        "conversation",
        "",
    )

    if from_me:
        print(
            "\n========================================"
        )
        print("WHATSAPP MESSAGE")
        print("========================================")
        print("Your (True)")
        print(f"Text: {text}")
        print("========================================\n")

        return None, None

    phone: str = key.get(
        "senderPn",
        "",
    ).replace(
        "@s.whatsapp.net",
        "",
    )

    print(
        "\n========================================"
    )
    print("WHATSAPP MESSAGE")
    print("========================================")
    print(f"Phone: {phone}")
    print(f"Text: {text}")
    print(
        "========================================"
    )

    return phone, text
