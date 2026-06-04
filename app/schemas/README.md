# `📦 schemas/`

> O diretório `📦 schemas/` contém os modelos Pydantic usados para entrada e saída de dados da API.

## Conteúdo

 - [`gestor.py`](#gestor-py)
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


**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
