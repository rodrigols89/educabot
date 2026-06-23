# `🏛️ models/`

 - Representa as tabelas do banco.
 - Cada classe equivale a uma tabela.

## Conteúdo

 - [`pedido.py`](#pedido-py)
   - [`class Pedido(Base)`](#class-pedido)
 - [`responsavel.py`](#responsavel-py)
   - [`class Responsavel(Base)`](#responsavel-class)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="pedido-py"></div>

## `pedido.py`

> O arquivo `pedido.py` vai ser responsável por registrar todos os pedidos realizados no sistema.

Essa tabela será utilizada para:

- auditoria
- histórico
- relatórios
- anti-spam
- controle diário





---

<div id="class-pedido"></div>

## `class Pedido(Base)`

> A classe `Pedido(Base)` vai ser responsável por representa um pedido realizado por alguém que tenha permissão no sistema.

[pedido.py](pedido.py)
```python
# app/models/pedido.py

from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
)
from sqlalchemy import (
    Enum as SqlEnum,
)
from sqlalchemy.orm import relationship

from app.db.base import Base


class TipoPedido(str, Enum):

    GAS = "GAS"
    AGUA = "AGUA"


class Pedido(Base):

    __tablename__ = "pedidos"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    responsavel_id = Column(
        Integer,
        ForeignKey("responsavel.id"),
        nullable=False,
    )

    tipo = Column(
        SqlEnum(
            TipoPedido,
            name="tipo_pedido",
        ),
        nullable=False,
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationship with order.
    responsavel = relationship("Responsavel", backref="pedidos")
```




















---

<div id="responsavel-py"></div>

## `responsavel.py`

> O arquivo `responsavel.py` é responsável por representar os responsáveis autorizados a utilizar o sistema.

Cada responsável poderá:

 - pedir gás
 - pedir água
 - ser ativado/desativado





---

<div id="responsavel-class"></div>

## `class Responsavel(Base)`

> A classe `Responsavel(Base)` vai ser responsável por mapear a tabela responsavel utilizando SQLAlchemy ORM.

Ela define:

- permissões
- telefone
- escola
- status

[responsavel.py](responsavel.py)
```python
# app/models/responsavel.py

from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
)

from app.db.base import Base


class Responsavel(Base):

    __tablename__ = "responsavel"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    nome = Column(
        String(255),
        nullable=False,
    )

    telefone = Column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )

    instituicao = Column(
        String(255),
        nullable=False,
    )

    pode_pedir_gas = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    pode_pedir_agua = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    ativo = Column(
        Boolean,
        default=True,
        nullable=False,
    )
```

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
