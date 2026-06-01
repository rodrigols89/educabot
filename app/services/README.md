# `🧠 services/`

> **Aqui ficam as regras de negócio.**

Responsabilidades:

> Tomar decisões.

### `Exemplo`

Regra:

```text
Somente gestores podem criar pedidos.
```

Essa lógica NÃO deve ficar:

 - No endpoint
 - No repository

### `Exemplo visual`

```text
API
 │
 ▼
Service
 │
 ▼
Repository
 │
 ▼
Banco
```

## Conteúdo

 - [`command_service.py`](#command-service-py)
   - [`parse_command()`](#parse-command)
 - [`permission_service.py`](#permission-service-py)
   - [`validate_permission()`](#validate-permission)
 - [`pedido_service.py`](#pedido-service-py)
   - [`create_request()`](#create-request)
 - [`request_limit_service.py`](#request-limit-service-py)
   - [`validate_daily_request()`](#validate-daily-request)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="command-service-py"></div>

## `command_service.py`

> O arquivo `command_service.py` será responsável por interpretar comandos recebidos pelo sistema.





---

<div id="parse-command"></div>

## `parse_command()`

A função `parse_command()` vai ser responsável por converter:

```bash
/gas
```

em:

```json
{
    "tipo": "gas",
    "quantidade": 1
}
```

[command_service.py](command_service.py)
```python
from typing import Dict

from app.utils.regex import validate_request_command


def parse_command(command: str) -> Dict[str, int | str]:

    # Validate command format
    if not validate_request_command(command):
        raise ValueError("Invalid command format.")

    # Remove leading and trailing spaces
    cleaned_command = command.strip()

    # Split command into parts
    parts = cleaned_command.split()

    # Extract request type and quantity
    request_type = parts[0].replace("/", "")

    # Convert quantity to integer
    quantity = int(parts[1])

    # Return parsed request information
    return {
        "tipo": request_type,
        "quantidade": quantity,
    }
```




















---

<div id="permission-service-py"></div>

## `permission_service.py`

> O arquivo `permission_service.py` será responsável por validar permissões do gestor.





---

<div id="validate-permission"></div>

## `validate_permission()`

> A função `validate_permission()` verifica se o gestor possui permissão para determinado pedido.

[permission_service.py](permission_service.py)
```python
from app.models.gestor import Gestor


def validate_permission(
    gestor: Gestor,
    request_type: str,
) -> bool:

    if request_type == "gas":
        return gestor.pode_pedir_gas

    if request_type == "agua":
        return gestor.pode_pedir_agua

    return False
```




















---

<div id="pedido-service-py"></div>

## `pedido_service.py`

> O arquivo `pedido_service.py` será responsável por centralizar o fluxo principal de criação de pedidos.





---

<div id="create-request"></div>

## `create_request()`

A função `create_request()` centraliza toda a regra de negócio para criação de um pedido. Ela:

 - Recebe o comando enviado pelo gestor (ex.: /gas).
 - Extrai o tipo do pedido e a quantidade.
 - Verifica se o gestor possui permissão para solicitar aquele item.
 - Verifica se já existe um pedido da mesma categoria no dia atual.
 - Cria o objeto Pedido.
 - Salva o pedido no banco de dados.

[pedido_service.py](pedido_service.py)
```python
from sqlalchemy.orm import Session

from app.models.gestor import Gestor
from app.models.pedido import Pedido, RequestType
from app.services.command_service import parse_command
from app.services.permission_service import (
    validate_permission,
)
from app.services.request_limit_service import (
    validate_daily_request,
)


def create_request(
    db: Session,
    gestor: Gestor,
    command: str,
) -> Pedido:

    # Parse command and extract request data
    parsed_command = parse_command(command)

    # Extract request type (gas or agua)
    request_type = parsed_command["tipo"]

    # Extract requested quantity
    quantity = parsed_command["quantidade"]

    # Check whether the manager has permission
    # to create this type of request
    has_permission = validate_permission(
        gestor=gestor,
        request_type=request_type,
    )

    # Stop execution if the manager is not allowed
    # to request the selected category
    if not has_permission:
        raise ValueError(
            "Manager does not have permission "
            f"to request '{request_type}'."
        )

    # Check whether a request of the same type
    # has already been made today
    request_allowed = validate_daily_request(
        db=db,
        gestor_id=gestor.id,
        request_type=request_type,
    )

    # Stop execution if a request already exists
    # for the same category today
    if not request_allowed:
        raise ValueError(
            f"A '{request_type}' request has already "
            f"been made today."
        )

    # Create a new request instance
    pedido = Pedido(
        gestor_id=gestor.id,
        tipo=RequestType(request_type),
        quantidade=quantity,
    )

    # Add the request to the current database session
    db.add(pedido)

    # Persist changes to the database
    db.commit()

    # Reload the object with generated fields
    # such as id and timestamps
    db.refresh(pedido)

    # Return the created request
    return pedido
```




















---

<div id="request-limit-service-py"></div>

## `request_limit_service.py`

> O arquivo `request_limit_service.py` é responsável por implementar as regras de controle e limite de requisições da aplicação.

 - Ele verifica se um usuário, gestor ou recurso já atingiu a quantidade máxima de operações permitidas em um determinado período;
 - Ajudando a evitar abusos, sobrecarga do sistema e violações das regras de negócio.





---

<div id="validate-daily-request"></div>

## `validate_daily_request()`

> A função `validate_daily_request()` vai ser responsável por verificar se o gestor já realizou um pedido da mesma categoria no dia atual.

[request_limit_service.py](request_limit_service.py)
```python
from sqlalchemy.orm import Session

from app.repositories.pedido_repository import (
    exists_request_today,
)


def validate_daily_request(
    db: Session,
    gestor_id: int,
    request_type: str,
) -> bool:

    # Check if request already exists
    already_requested = exists_request_today(
        db=db,
        gestor_id=gestor_id,
        request_type=request_type,
    )

    return not already_requested
```

<details>

<summary>Explicação passo a passo (Step-by-Step)</summary>

<br/>

```python
already_requested = exists_request_today(
    db=db,
    gestor_id=gestor_id,
    request_type=request_type,
)
```

No código acima a função `exists_request_today()` consulta o banco e verifica se já existe um pedido hoje para:

 - o mesmo `gestor_id`
 - o mesmo `request_type` (`gas` ou `agua`)

Se encontrar um pedido, retorna:

```python
True
```

Se não encontrar:

```python
False
```

Depois, inverte o resultado:

```python
return not already_requested
```

| already_requested | retorno |
| ----------------- | ------- |
| True              | False   |
| False             | True    |

> **Por que essa inversão?**  
> Porque a `função exists_request_today()` responde uma pergunta diferente da função `validate_daily_request()`.

 - `exists_request_today()` - Quero saber se o gestor ja pediu gás/água hoje?
   - Se já pediu, retorna `True`.
   - Se ainda nao pediu, retorna `False`.
 - `validate_daily_request()` - Quero saber se o gestor pode pedir gás/água hoje?
   - Se `exists_request_today()` retornar `True`, nós não podemos fazer um novo pedido, ou seja, vamos retornar `False`.
   - Se `exists_request_today()` retornar `False`, podemos fazer um novo pedido, ou seja, vamos retornar `True`.

</details>

---


**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
