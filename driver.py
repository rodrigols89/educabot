# driver.py

from app.db.session import SessionLocal
from app.repositories.gestor_repository import (
    get_gestor_by_phone,
)

db = SessionLocal()

try:

    gestor = get_gestor_by_phone(
        db=db,
        phone="5583996192515",
    )

    if gestor is None:
        print("Gestor não encontrado")

    else:
        print(type(gestor))
        print(f"Nome: {gestor.nome}")
        print(f"Telefone: {gestor.telefone}")
        print(f"Escola: {gestor.escola}")

finally:
    db.close()
