# `🗄️ db/`

> Camada responsável pela conexão com o Banco de Dados.

Responsabilidades:

 - Engine SQLAlchemy
 - Session
 - Base ORM

### `Exemplo visual`

```text
Application
     │
     ▼
    db
     │
     ▼
 PostgreSQL
```

## Conteúdo

 - [`base.py`](#base-py)
 - [`session.py`](#session-py)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="base-py"></div>

## `base.py`

> Este arquivo define a classe **base (Base)** utilizada por todos os modelos do SQLAlchemy.

Ao herdar de `Base`, uma classe passa a ser reconhecida pelo ORM como uma tabela do banco de dados, permitindo que o SQLAlchemy e o Alembic gerenciem automaticamente sua estrutura e relacionamentos.

[base.py](base.py)
```python
"""
SQLAlchemy base configuration module.

Defines the declarative base used by all models.
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()
```




















---

<div id="session-py"></div>

## `session.py`

> Este arquivo é responsável por **configurar a conexão com o banco de dados** e **criar sessões do SQLAlchemy**.

 - As sessões são utilizadas para executar operações como consultas, inserções, atualizações e exclusões de registros.
 - Além disso, a função `get_db()` fornece uma sessão de banco de dados de forma segura, garantindo que ela seja fechada automaticamente ao final de cada uso.

[session.py](session.py)
```python
"""
Database session manager.

Provides SQLAlchemy engine and session factory.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    Provide database session dependency.

    Yields
    ------
    Session
        SQLAlchemy session instance.

    Examples
    --------
    >>> db = next(get_db())
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
