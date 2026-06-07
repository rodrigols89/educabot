# `📦 schemas/`

> O diretório `📦 schemas/` contém os modelos Pydantic usados para entrada e saída de dados da API.

## Conteúdo

 - [`evolution.py`](#evolution-py)
 - [`gestor.py`](#gestor-py)
 - [`pedido.py`](#pedido-py)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="evolution-py"></div>

## `evolution.py`

> O arquivo `evolution.py` será responsável por transformar o payload complexo enviado pela Evolution API em um objeto simples e tipado.

Atualmente o webhook recebe algo parecido com:

```json
{
  "event": "messages.upsert",
  "data": {
    "key": {
      "remoteJid": "5583999999999@s.whatsapp.net"
    },
    "pushName": "Maria Silva",
    "message": {
      "conversation": "/gas"
    },
    "messageTimestamp": 1749110000
  }
}
```

Sem schema você precisaria fazer:

```python
payload["data"]["key"]["remoteJid"]
payload["data"]["message"]["conversation"]
```

Com o schema:

```python
webhook.phone
webhook.message
webhook.name
webhook.timestamp
```

[evolution.py](evolution.py)
```python
from datetime import datetime

from pydantic import BaseModel, Field


class EvolutionMessage(BaseModel):

    phone: str = Field(...)
    text: str = Field(...)
    name: str | None = None
    timestamp: datetime
    from_me: bool
    message_type: str
```




















---

<div id="gestor-py"></div>

## `gestor.py`

> O arquivo `gestor.py` contém os modelos Pydantic usados para contratos de entrada e saída dos gestores.

[gestor_schemas.py](gestor_schemas.py)
```python
from pydantic import BaseModel, ConfigDict


class GestorCreate(BaseModel):

    nome: str
    telefone: str
    escola: str
    pode_pedir_gas: bool
    pode_pedir_agua: bool


class GestorResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    nome: str
    telefone: str
    escola: str
    pode_pedir_gas: bool
    pode_pedir_agua: bool
    ativo: bool
```




















---

<div id="pedido-py"></div>

## `pedido.py`

> O arquivo `pedido.py` contém os modelos Pydantic usados para contratos da API de pedidos.

[pedido.py](pedido.py)
```python
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PedidoCreate(BaseModel):

    gestor_id: int
    comando: str


class PedidoResponse(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    id: int
    gestor_id: int
    tipo: str
    quantidade: int
    criado_em: datetime
```

---


**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
