def is_valid_command(
    phone: str | None,
    text: str | None,
) -> bool:

    # Ignored messages (fromMe=True)
    if phone is None and text is None:
        return False

    # Empty messages
    if not text:
        return False

    # Normalize text
    text = text.strip().lower()

    # Supported commands
    return text in (
        "/gas",
        "/agua",
    )
