# `🏛️ models/`

 - Representa as tabelas do banco.
 - Cada classe equivale a uma tabela.

### `Exemplo visual`

```text
Model SQLAlchemy
       │
       ▼
Tabela PostgreSQL
```

## Conteúdo

 - [`gestor.py`](#gestor-py)
   - [`class Gestor(Base)`](#class-gestor)
 - [`log.py`](#log-py)
   - [`class Log(Base)`](#class-log)
 - [`pedido.py`](#pedido-py)
   - [`class Pedido(Base)`](#class-pedido)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="gestor-py"></div>

## `gestor.py`

> O arquivo `gestor.py` é responsável por representar os gestores autorizados a utilizar
o sistema.

Cada gestor poderá:

 - pedir gás
 - pedir água
 - ser ativado/desativado





---

<div id="class-gestor"></div>

## `class Gestor(Base)`

> A classe `Gestor(Base)` vai ser responsável por mapear a tabela gestores utilizando SQLAlchemy ORM.

Ela define:

- permissões
- telefone
- escola
- status

[gestor.py](gestor.py)
```python
from sqlalchemy import Boolean, Column, Integer, String

from app.db.base import Base


class Gestor(Base):

    __tablename__ = "gestores"

    id = Column(Integer, primary_key=True, index=True)

    nome = Column(String(255), nullable=False)

    telefone = Column(
        String(20),
        nullable=False,
        unique=True,
        index=True,
    )

    escola = Column(String(255), nullable=False)

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

<div id="log-py"></div>

## `log.py`

> O arquivo `log.py` vai ser responsável por registrar logs operacionais e auditoria do sistema.

Essa tabela ajudará:

 - rastreabilidade
 - debug
 - segurança
 - auditoria administrativa





---

<div id="class-log"></div>

## `class Log(Base)`

> A classe `Log(Base)` vai ser responsável por representa um registro operacional do sistema.

[log.py](log.py)
```python
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.base import Base


class Log(Base):

    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    telefone = Column(
        String(20),
        nullable=False,
    )

    mensagem = Column(
        Text,
        nullable=False,
    )

    resposta = Column(
        Text,
        nullable=True,
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
```




















---

<div id="pedido-py"></div>

## `pedido.py`

> O arquivo `pedido.py` é Responsável por registrar todos os pedidos realizados no sistema.

Essa tabela será utilizada para:

- auditoria
- histórico
- relatórios
- anti-spam
- controle diário





---

<div id="class-pedido"></div>

## `class Pedido(Base)`

> A classe `Pedido(Base)` vai ser responsável por representa um pedido realizado por um gestor.

[pedido.py](pedido.py)
```python
from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Pedido(Base):

    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)

    gestor_id = Column(
        Integer,
        ForeignKey("gestores.id"),
        nullable=False,
    )

    tipo = Column(
        String(20),
        nullable=False,
    )

    quantidade = Column(
        Integer,
        nullable=False,
    )

    criado_em = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # Relationship with manager.
    gestor = relationship("Gestor")
```

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
