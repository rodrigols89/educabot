# `📚 repositories/`

> O diretório `📚 repositories/` é responsável por conversar diretamente com o banco.

A partir dele que nós executamos queries, como:

 - SELECT
 - INSERT
 - UPDATE
 - DELETE

### `Exemplo visual`

```text
Service (Regras de negócio)
   │
   ▼
Repository (Consulta/Query)
   │
   ▼
Banco de Dados
```

## Conteúdo

 - [`gestor_repository.py`](#gestor-repository-py)
   - [`get_gestor_by_phone()`](#get-gestor-by-phone)
 - [`pedido_repository.py`](#pedido-repository-py)
   - [`exists_request_today()`](#exists-request-today)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="gestor-repository-py"></div>

## `gestor_repository.py`

> Esse arquivo `gestor_repository.py` vai ser responsável por centralizar consultas relacionadas a gestores.





---

<div id="get-gestor-by-phone"></div>

## `get_gestor_by_phone()`

> A função `get_gestor_by_phone()` vai ser responsável por buscar um gestor pelo telefone.

[gestor_repository.py](gestor_repository.py)
```python
from sqlalchemy.orm import Session

from app.models.gestor import Gestor


def get_gestor_by_phone(
    db: Session,
    phone: str,
) -> Gestor | None:

    return (
        db.query(Gestor)
        .filter(Gestor.phone == phone)
        .first()
    )

```




















---

<div id="pedido-repository-py"></div>

## `pedido_repository.py`

> O arquivo `pedido_repository.py` vai ser responsável por centralizar consultas relacionadas a pedidos.





---

<div id="exists-request-today"></div>

## `exists_request_today()`

> A função `exists_request_today()` vai ser responsável por verificar se já existe um pedido de determinada categoria realizado pelo gestor na data atual.

[pedido_repository.py](pedido_repository.py)
```python
from datetime import datetime
from datetime import timedelta

from sqlalchemy.orm import Session

from app.models.pedido import Pedido


def exists_request_today(
    db: Session,
    gestor_id: int,
    request_type: str,
) -> bool:

    # Get "start" and "end" of day
    start_of_day = datetime.utcnow().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    # Get "end" of day
    end_of_day = start_of_day + timedelta(days=1)

    # Check if request already exists
    return (
        db.query(Pedido)
        .filter(Pedido.gestor_id == gestor_id)
        .filter(Pedido.tipo == request_type)
        .filter(Pedido.criado_em >= start_of_day)
        .filter(Pedido.criado_em < end_of_day)
        .first()
        is not None
    )
```

<details>

<summary>Explicação Passo a Passo (Step-by-Step)</summary>

<br/>

```python
start_of_day = datetime.utcnow().replace(
    hour=0,
    minute=0,
    second=0,
    microsecond=0,
)
```

 - `datetime.utcnow()`
   - Retorna a data e hora atual em UTC (Tempo Universal Coordenado).
   - Por exemplo: `datetime(2026, 6, 1, 16, 35, 42, 123456)`
   - Representando: `01/06/2026 16:35:42.123456 UTC`
 - `replace()`
   - O método replace() cria um novo objeto datetime alterando apenas os campos informados.

```python
end_of_day = start_of_day + timedelta(days=1)
```

 - `timedelta(days=1)`
   - `timedelta` representa uma diferença de tempo.

```python
return (
    db.query(Pedido)
    .filter(Pedido.gestor_id == gestor_id)
    .filter(Pedido.tipo == request_type)
    .filter(Pedido.criado_em >= start_of_day)
    .filter(Pedido.criado_em < end_of_day)
    .first()
    is not None
)
```

 - Consulta a tabela `Pedido` para verificar se já existe hoje um pedido do tipo informado (gas ou agua) para o gestor informado.
 - Se encontrar pelo menos um registro, retorna `True`; caso contrário, retorna `False`.

Ou ainda mais resumido:

Verifica se o gestor já fez hoje um pedido da categoria informada. Retorna `True` se existir e `False` se não existir.

**Resultado SQL aproximado:**

```python
SELECT *
FROM pedido
WHERE gestor_id = 5
  AND tipo = 'gas'
  AND criado_em >= '2026-06-01 00:00:00'
  AND criado_em < '2026-06-02 00:00:00'
```

</details>

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
