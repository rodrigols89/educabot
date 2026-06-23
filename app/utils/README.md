# `🔧 utils/`

> O diretório `🔧 utils/` é responsável por *"guardar coisas que podem ser usadas em vários lugares"*.

Por, exemplo:

 - Formatar telefone
 - Validar CPF
 - Gerar UUID

## Conteúdo

 - [`insert_responsavel_example.py`](#insert-responsavel-example.py)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="insert-responsavel-example.py"></div>

## `insert_responsavel_example.py`

> O script `insert_responsavel_example.py` é um modelo que pode ser utilizado para quem desejar inserir os responsáveis pelos pedidos automatimente (sem precisa utilizar a API).

[insert_responsavel_example.py](insert_responsavel_example.py)
```python
# app/utils/insert_responsavel_example.py

"""
From Root dir run the command below:
python -m app.utils.insert_responsavel_example
"""

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.responsavel import Responsavel

RESPONSAVEIS = [
    {
        "nome": "nome do responsavel",
        "telefone": "telefone do responsavel",
        "instituicao": "instituição do responsavel",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    }
]


def responsavel_exists(db: Session, telefone: str) -> bool:
    return (
        db.query(Responsavel)
        .filter(Responsavel.telefone == telefone)
        .first()
        is not None
    )


def insert_responsaveis() -> None:
    db: Session = SessionLocal()

    try:
        for data in RESPONSAVEIS:
            if responsavel_exists(db, data["telefone"]):
                continue

            db.add(Responsavel(**data))

        db.commit()
        print("Responsáveis inseridos com sucesso.")

    finally:
        db.close()


if __name__ == "__main__":
    insert_responsaveis()
```

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
