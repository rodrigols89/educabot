# `🧠 services/`

> **Aqui ficam as regras de negócio.**

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
Service (Regras de negócio)
 │
 ▼
Repository (Consulta/Query)
 │
 ▼
Banco de Dados
```

## Conteúdo

 - [`command_service.py`](#command-service-py)
   - [`is_valid_command()`](#is-valid-command)
 - [`evolution_client.py`](#evolution-client-py)
   - [`send_whatsapp_message()`](#send-whatsapp-message)
 - [`notification_service.py`](#notification-service-py)
   - [`build_supplier_message()`](#build-supplier-message)
 - [`pedido_service.py`](#pedido-service-py)
   - [`create_order()`](#create-order)
 - [`responsavel_service.py`](#responsavel-service-py)
   - [`check_responsavel()`](#check-responsavel)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="command-service-py"></div>

## `command_service.py`

> O arquivo `command_service.py` será responsável por interpretar comandos recebidos pelo sistema.





---

<div id="is-valid-command"></div>

## `is_valid_command()`

> A função `is_valid_command()` tem como maior objetivo validar se o texto recebido se enquadra em um comando válido `/gas` ou `/agua`.

[command_service.py](command_service.py)
```python
# app/services/command_service.py

from app.utils.logger import print_separator


def is_valid_command(
    text: str | None,
) -> bool:

    print_separator()
    print("COMMAND VALIDATION PROCESS:")

    # Empty messages
    if not text:
        print("A mensagem (text) de alguma maneira veio vazia (None)")
        return False

    # Normalize text
    text = text.strip().lower()

    # Supported commands
    is_valid = text in {
        "/gas",
        "/agua",
    }

    if is_valid:
        print(f"Comando válido: {text}")
    else:
        print(f"Comando inválido: {text}")

    return is_valid
```

> **NOTE:**  
> O operador `"in"` retorna sempre um `bool`:  
> - `"/gas" in ("/gas", "/agua")   # True`
> - `"/teste" in ("/gas", "/agua") # False`




















---

<div id="evolution-client-py"></div>

## `evolution_client.py`

> Ele é a camada de integração com a Evolution API (WhatsApp).

Ele NÃO sabe nada sobre:

 - pedidos
 - responsáveis
 - regras de negócio
 - validação

Ele só sabe uma coisa:

> **“Como enviar mensagens via Evolution API”**





---

<div id="send-whatsapp-message"></div>

## `send_whatsapp_message()`

A função `` só tem uma responsabilidade:

> **Enviar uma mensagem de texto via WhatsApp usando a Evolution API.**

[evolution_client.py](evolution_client.py)
```python
# ruff: noqa: PLW0717
# app/services/evolution_service.py

import requests

from app.core.config import settings


def send_text_message(
    phone: str,
    message: str,
) -> bool:

    url = (
        f"{settings.EVOLUTION_API_URL}"
        f"/message/sendText/"
        f"{settings.EVOLUTION_INSTANCE}"
    )

    payload = {
        "number": phone,
        "text": message,
    }

    headers = {
        "apikey": settings.AUTHENTICATION_API_KEY,
        "Content-Type": "application/json",
    }

    print("\nEVOLUTION REQUEST:")
    print(f"URL: {url}")
    print(f"PHONE: {phone}")
    print(f"PAYLOAD: {payload}")

    try:

        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        print("\nEVOLUTION RESPONSE:")
        print(f"STATUS: {response.status_code}")
        print(f"BODY: {response.text}")

        return response.status_code in {
            200,
            201,
        }

    except Exception as error:

        print("\nEVOLUTION ERROR:")
        print(error)

        return False
```

<details>

<summary>Explicação Passo a Passo (Step-by-Step)</summary>

<br/>

> Aqui, nós vamos entender como essa função é (pode ser) utilizada.

De início o que foi feito foi montar uma URL que vai apontar para o nosso serviço no Evolution API (Não para a nossa API do FastAPI):

```python
url = (
    f"{settings.EVOLUTION_API_URL}"
    f"/message/sendText/"
    f"{settings.EVOLUTION_INSTANCE}"
)
```

> **NOTE:**  
> O código acima equivale a gerar a seguinte URL: [http://localhost:8080/message/sendText/educabot](http://localhost:8080/message/sendText/educabot)

A nossa função `send_whatsapp_message()` sempre vai receber:

 - Um número de telefone.
 - Uma mensagem (que vai ser o nosso comando).

Vamos criar um **payload** para enviar esses dados pelo a nossa URL que nós criamos para o *Evolution API*:

```python
payload = {
    "number": phone,
    "text": message,
}
```

Nós também vamos precisar de `headers` que vão junto da nossa requisição `request` para o *evolution API*:

```python
headers = {
    "apikey": settings.AUTHENTICATION_API_KEY,
    "Content-Type": "application/json",
}
```

Agora, nós vamos utilizar tudo o que foi feito até agora para enviar uma requisição do tipo `POST` para o *Evolution API*:

```python
response = requests.post(
    url=url,
    json=payload,
    headers=headers,
    timeout=30,
)
```

Por fim, nós retornamos o `status_code` da requisição:

```python
return response.status_code in {
    200,
    201,
}
```

### `DÚVIDA`

> **Como o Evolution API sabe que com os dados que eu enviei, ele deveria mandar uma mensagem para alguém?**

Quando nós chamamos um endpoint fixo:

```bash
POST /message/sendText/educabot
```

> 👉 Isso (sendText) já define a ação: **enviar texto**

</details>




















---

<div id="notification-service-py"></div>

## `notification_service.py`

> Este módulo centraliza a configuração dos fornecedores responsáveis pelo atendimento de pedidos e a construção das mensagens enviadas a eles.





---

<div id="build-supplier-message"></div>

## `build_supplier_message()`

> A função `build_supplier_message()` vai ser responsável por:

 - **Pegar o número de telefone do forcenecedor específico do pedido:**
   - Esse número vai ser retornado na função.
 - **Montar uma mensagem específica para esse fornecedor:**
   - Essa mensagem vai ser retornada na função.

[notification_service.py](notification_service.py)
```python
# app/services/notification_service.py

from app.core.config import settings
from app.models.pedido import TipoPedido
from app.models.responsavel import Responsavel

SUPPLIERS = {
    TipoPedido.GAS: {
        "name": settings.SUPPLIER_GAS_NAME,
        "phone": settings.SUPPLIER_GAS_PHONE,
    },
    TipoPedido.AGUA: {
        "name": settings.SUPPLIER_WATER_NAME,
        "phone": settings.SUPPLIER_WATER_PHONE,
    },
}


def build_supplier_message(
    responsavel: Responsavel,
    tipo: TipoPedido,
) -> tuple[str, str]:

    print("\nCHOOSE SUPPLIER/MESSAGE PROCESS:")

    supplier = SUPPLIERS[tipo]

    is_secretariat_water = (
        tipo == TipoPedido.AGUA
        and responsavel.telefone
        in settings.SECRETARIAT_PHONES
    )

    if is_secretariat_water:
        supplier = {
            "name": (
                settings.SUPPLIER_SECRETARIAT_WATER_NAME
            ),
            "phone": (
                settings.SUPPLIER_SECRETARIAT_WATER_PHONE
            ),
        }

    if tipo == TipoPedido.GAS:
        quantidade = "1"
        item = "botijão de gás"

    elif is_secretariat_water:
        quantidade = "2"
        item = "galões de água"

    else:
        quantidade = "1"
        item = "pipa d'água"

    message = (
        f"Bom dia!\n"
        f"{quantidade} {item} para a {responsavel.instituicao}, por favor.\n"
        f"Responsável pelo pedido: {responsavel.nome}.\n"
        f"Telefone para contato: {responsavel.telefone}."
    )

    print(
        f"Pedido de {quantidade} {item} será enviado para "
        f"{supplier['name']} ({supplier['phone']})"
    )

    print(
        f"Mensagem enviada:\n"
        f"{message}"
    )

    return (
        supplier["phone"],
        message,
    )
```




















---

<div id="pedido-service-py"></div>

## `pedido_service.py`

> O arquivo `pedido_service.py` é responsável por garantir todas as regras de negócio relacionada a pedidos.





---

<div id="create-order"></div>

## `create_order()`

A função `create_order()` vai ser responsável por todo o processo de criação de pedido para um *responsável* autorizado, como:

 - Identificar o tipo de pedido.
 - Verificar se o responsável já fez um pedido desse tipo no mesmo dia:
   - Se o usuário já tiver feito um pedido desse tipo no mesmo dia ele vai retornar `None` + o tip do pedido.
 - Se o responsável não tiver feito um pedido desse tipo no mesmo dia:
   - Vai salvar o pedido no Banco de Dados.
   - Retornar o `pedido (objeto)` + o `tipo`

[pedido_service.py](pedido_service.py)
```python
# app/services/pedido_service.py

from sqlalchemy.orm import Session

from app.models.pedido import Pedido, TipoPedido
from app.models.responsavel import Responsavel
from app.repositories.pedido_repository import (
    create_pedido,
    get_today_pedido,
)


def create_order(
    db: Session,
    responsavel: Responsavel,
    command: str,
) -> tuple[Pedido | None, TipoPedido]:

    print("\nCREATE ORDER PROCESS:")

    request_type = command.replace("/", "").upper()
    tipo = TipoPedido[request_type]

    existing_request = get_today_pedido(
        db=db,
        responsavel_id=responsavel.id,
        tipo=tipo,
    )

    # 🚫 já existe pedido dessa categoria hoje
    if existing_request:
        print(f"Você já fez um pedido dessa categoria ({tipo}) hoje.")
        return None, tipo

    pedido = Pedido(
        responsavel_id=responsavel.id,
        tipo=tipo,
    )

    pedido = create_pedido(
        db=db,
        pedido=pedido,
    )

    print(f"Pedido ({tipo}) criado com sucesso!")

    return pedido, tipo
```




















---

<div id="responsavel-service-py"></div>

## `responsavel_service.py`

> O arquivo `command_service.py` será responsável por garantir regras de negócios relacionadas aos responsáveis pelo os pedidos.





---

<div id="check-responsavel"></div>

## `check_responsavel()`

> A função `check_responsavel()` vai garantir que apenas usuários cadastrados e ativos no sistema tenham permissão de fazer pedidos.

Ela vai retornar:

 - `None`
   - Quando o responsável (número) pelo pedido não estiver cadastrado.
   - Quando o responsável (número) pelo pedido não estiver ativo no sistema.
 - `responsavel`
   - Quando o usuário estiver cadastrado **e (^, conjunção)** ativo no sistema.

[responsavel_service.py](responsavel_service.py)
```python
from sqlalchemy.orm import Session

from app.models.responsavel import Responsavel
from app.repositories.responsavel_repository import (
    get_responsavel_by_phone,
)


def check_responsavel(
    db: Session,
    phone: str,
) -> Responsavel | None:

    print("\nVALIDATE ORDER OWNER PROCESS:")

    responsavel = get_responsavel_by_phone(
        db=db,
        phone=phone,
    )

    if responsavel is None:
        print("Responsável pelo pedido não encontrado/cadastrado.")
        return None

    if not responsavel.ativo:
        print("Responsável não está ativo no sistema.")
        return None

    print("O responsável pelo pedido está ativo.")
    print(f"Nome: {responsavel.nome}")
    print(f"Telefone: {responsavel.telefone}")
    print(f"Instituição: {responsavel.instituicao}")

    return responsavel
```

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
