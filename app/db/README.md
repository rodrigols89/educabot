# `🗄️ db/`

> O diretório `🗄️ db/` é responsável por *"gerenciar (conexão) o banco de dados"*.

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

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

<details>

<summary>Explicação Passo a Passo (Step-by-Step)</summary>

<br/>

### `Entendendo a função create_engine()`

Primeiro, vamos entender a função `create_engine()`:

```python
engine = create_engine(settings.DATABASE_URL, echo=True)
```

 - **O que ela receebe?**
   - O principal que nós estamos passando como argumento é a string de conexão do banco de dados (URL).
 - **O que ela retorna?**
   - Retorna um objeto do tipo: `sqlalchemy.engine.Engine`
   - Oou simplesmente: `Engine`
 - **O que é um Engine?**
   - O `Engine` é o componente que:
     - Sabe como conectar ao banco;
     - Gerencia o pool de conexões;
     - Executa comandos SQL;
     - É utilizado pelas Sessions do SQLAlchemy.

**Visualmente:**

```bash
Aplicação
    ↓
Session
    ↓
Engine
    ↓
Banco de Dados
```

### `Entendendo a classe sessionmaker()`

> Enquanto o `engine` sabe como conectar ao banco, o `sessionmaker()` sabe como criar sessões que usarão essa conexão.

```python
create_engine()
      ↓
    Engine
      ↓
sessionmaker()
      ↓
 SessionLocal
      ↓
 Session()
```

> **Mas, o que é uma Session?**

Uma `Session` é o objeto que você usa para:

 - db.add(objeto)
 - db.query(Model)
 - db.commit()
 - db.rollback()
 - db.close()

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)
```

 - `bind=engine`
   - No código acima o mais importante é o `bind=engine`, que liga a sessão ao banco configurado pelo engine.
 - `autocommit=False`
   - *Significa:*
     - Nada será salvo automaticamente.
   - *Você precisa chamar:*
     - `db.commit()` -> Só o db.add não salva no Banco de Dados.
 - `autoflush=False`
   - Controla quando alterações pendentes são enviadas para o banco.

### `Entendendo a função get_db()`

```python
def get_db():

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

No código acima:

 - `db = SessionLocal()`
   - Primeiro, nó scriamos uma instância da `SessionLocal`.
   - Que nada mais é que uma referência para `sessionmaker()`.
 - `try:`
   - `yield db` -> Entrega sessão para quem chamou a função.
 - `finally:`
   - `db.close()` -> Fecha a sessão.

</details>

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
