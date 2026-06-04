# `📦 schemas/`

> O diretório `📦 schemas/` contém os modelos Pydantic usados para entrada e saída de dados da API.

## Conteúdo

 - [`gestor.py`](#gestor-py)
 - [`pedido.py`](#pedido-py)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















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
