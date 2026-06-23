# `📚 repositories/`

> O diretório `📚 repositories/` é responsável por conversar diretamente com o banco de dados.

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

 - [`pedido_repository.py`](#pedido-repository-py)
   - [`create_pedido()`](#create-pedido)
   - [`get_today_pedido()`](#get-today-pedido)
 - [`responsavel_repository.py`](#responsavel-repository-py)
   - [`get_responsavel_by_phone()`](#get-responsavel-by-phone)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---


<div id="pedido-repository-py"></div>

## `pedido_repository.py`

> O arquivo `pedido_repository.py` vai ser responsável por centralizar consultas relacionadas a pedidos do sistema (Água ou Gás).





---

<div id="create-pedido"></div>

## `create_pedido()`

> A função `create_pedido()` vai ser responsável por criar um pedido no Banco de Dados.

[pedido_repository.py](pedido_repository.py)
```python
# app/repositories/pedido_repository.py

from sqlalchemy.orm import Session

from app.models.pedido import (
    Pedido,
)


def create_pedido(
    db: Session,
    pedido: Pedido,
) -> Pedido:

    db.add(pedido)
    db.commit()
    db.refresh(pedido)

    return pedido
```

<details>

<summary>driver.py</summary>

<br/>

> Aqui, nós vamos entender como essa função é (pode ser) utilizada.

Vamos começar criando (pegando) uma sessão com o nosso banco de dados:

```python
from app.db.session import SessionLocal

session = SessionLocal()
```

Agora, nós vamos criar uma instância do modelo [Pedido](../models/pedido.py):

```python
# driver.py
from app.db.session import SessionLocal

session = SessionLocal()

from app.models.responsavel import Responsavel
from app.models.pedido import Pedido, TipoPedido

pedido = Pedido(
    responsavel_id = 1,
    tipo=TipoPedido.GAS
)

print("Type:", type(pedido))
print("Resultado:", pedido)
```

**OUTPUT:**
```bash
Type: <class 'app.models.pedido.Pedido'>
Resultado: <app.models.pedido.Pedido object at 0x7206bfbfe390>
```

Ótimo, agora nós vamos passa para a função create_pedido() a sessão com o Banco de Dados e a instância do pedido que nós criamos (manualmente):

```python
# driver.py
from app.db.session import SessionLocal

session = SessionLocal()

from app.models.responsavel import Responsavel
from app.models.pedido import Pedido, TipoPedido

pedido = Pedido(
    responsavel_id = 1,
    tipo=TipoPedido.GAS
)

from app.repositories.pedido_repository import create_pedido

pedido_salvo = create_pedido(
    session,
    pedido
)

print("Type:", type(pedido_salvo))
print("Resultado:", pedido_salvo)
```

**OUTPUT:**
```bash
Type: <class 'app.models.pedido.Pedido'>
Resultado: <app.models.pedido.Pedido object at 0x76a73559cf20>
```

Agora, para acessar os campos do modelo (tabela) nós vamos utilizar o `"."`:>

```python
# driver.py
from app.db.session import SessionLocal

session = SessionLocal()

from app.models.responsavel import Responsavel
from app.models.pedido import Pedido, TipoPedido

pedido = Pedido(
    responsavel_id = 1,
    tipo=TipoPedido.GAS
)

from app.repositories.pedido_repository import create_pedido

pedido_salvo = create_pedido(
    session,
    pedido
)

if pedido_salvo:
    print("Pedido criado com sucesso!")
    print(f"ID: {pedido_salvo.id}")
    print(f"Responsável: {pedido_salvo.responsavel_id}")
    print(f"Tipo: {pedido_salvo.tipo}")
    print(f"Criado em: {pedido_salvo.criado_em}")
else:
    print("Algum problema foi encontrado ao criar seu pedido")
```

**OUTPUT:**
```bash
Pedido criado com sucesso!
ID: 3
Responsável: 1
Tipo: TipoPedido.GAS
Criado em: 2026-06-23 15:43:11.055460
```

</details>





---

<div id="get-today-pedido"></div>

## `get_today_pedido()`

> A função `get_today_pedido()` tem como responsabilidade verificar se quem está fazendo um pedido já realizou um pedido da mesma categoria no mesmo dia (Essa regra de negócio só permite um pedido de cada categoria por dia).

[pedido_repository.py](pedido_repository.py)
```python
# app/repositories/pedido_repository.py

from datetime import datetime

from sqlalchemy.orm import Session

from app.models.pedido import Pedido, TipoPedido


def get_today_pedido(
    db: Session,
    gestor_id: int,
    tipo: TipoPedido,
) -> Pedido | None:

    today = datetime.utcnow().date()

    return (
        db.query(Pedido)
        .filter(
            Pedido.gestor_id == gestor_id
        )
        .filter(
            Pedido.tipo == tipo
        )
        .filter(
            Pedido.criado_em >= today
        )
        .first()
    )
```


<details>

<summary>driver.py</summary>

<br/>

> Aqui, nós vamos entender como essa função é (pode ser) utilizada.

Vamos começar criando (pegando) uma sessão com o nosso banco de dados:

```python
from app.db.session import SessionLocal

session = SessionLocal()
```

Agora, nós vamos chamar a função `get_today_pedido()` e passa como argumento:

 - O `id` tem algum responsável que nós sabemos que existe no Banco de Dados.
 - Um `tipo de pedido (TipoPedido)` que nós também sabemos que existe no Banco de Dados.

```python
# driver.py
from app.db.session import SessionLocal

session = SessionLocal()

from app.repositories.pedido_repository import get_today_pedido
from app.models.responsavel import Responsavel
from app.models.pedido import Pedido, TipoPedido

pedido = get_today_pedido(
    session,
    responsavel_id=1,
    tipo=TipoPedido.GAS
)

print("Type:", type(pedido))
print("Resultado:", pedido)
```

**OUTPUT:**
```python
Type: <class 'app.models.pedido.Pedido'>
Resultado: <app.models.pedido.Pedido object at 0x7801222aef30>
```

> **NOTE:**  
> Ótimo, nós sabemos que deu certo porque nós não recebmos `None`, ou seja, nã tinhamos pedido do responsável hoje.

Sabendo das informações acima, nós podemos verificar os dados (campos) do pedido:

```python
# driver.py

from app.db.session import SessionLocal

session = SessionLocal()

from app.repositories.pedido_repository import get_today_pedido
from app.models.responsavel import Responsavel
from app.models.pedido import Pedido, TipoPedido

pedido = get_today_pedido(
    session,
    responsavel_id=1,
    tipo=TipoPedido.GAS
)

if pedido:
    print("Pedido encontrado para hoje!")
    print(f"ID: {pedido.id}")
    print(f"Responsável ID: {pedido.responsavel_id}")
    print(f"Tipo: {pedido.tipo}")
    print(f"Criado em: {pedido.criado_em}")
else:
    print("Nenhum pedido encontrado para hoje.")
```

**OUTPUT:**
```bash
Pedido encontrado para hoje!
ID: 1
Responsável ID: 1
Tipo: TipoPedido.GAS
Criado em: 2026-06-23 15:39:32.160001
```

</details>

















































































---

<div id="responsavel-repository-py"></div>

## `responsavel_repository.py`

> O arquivo `responsavel_repository.py` vai ser responsável por centralizar consultas relacionadas aos responsáveis pelo os pedidos.





---

<div id="get-responsavel-by-phone"></div>

## `get_responsavel_by_phone()`

> A função `get_responsavel_by_phone()` vai ser responsável por buscar um responsavel pelo telefone.

[responsavel_repository.py](responsavel_repository.py)
```python
# app/repositories/responsavel_repository.py

from sqlalchemy.orm import Session

from app.models.responsavel import Responsavel


def get_responsavel_by_phone(
    db: Session,
    phone: str,
) -> Responsavel | None:

    return (
        db.query(Responsavel)
        .filter(
            Responsavel.telefone == phone
        )
        .first()
    )
```

<details>

<summary>driver.py</summary>

<br/>

> Aqui, nós vamos entender como essa função é (pode ser) utilizada.

Vamos começar criando (pegando) uma sessão com o nosso banco de dados:

```python
from app.db.session import SessionLocal

session = SessionLocal()
```

Agora, vamos chamar a função `get_responsavel_by_phone()` e passar como argumento a sessão + o número de telefone que nós desejamos procurar:

```python
# driver.py

from app.db.session import SessionLocal

session = SessionLocal()

from app.repositories.responsavel_repository import get_responsavel_by_phone

responsavel = get_responsavel_by_phone(
    session,
    phone="558396241663",
)

print("Type:", type(responsavel))
print("Resultado:", responsavel)
```

**OUTPUT:**
```bash
Type: <class 'app.models.responsavel.Responsavel'>
Resultado: <app.models.responsavel.Responsavel object at 0x7626a45089e0>
```

**NOTE:**  
Vejam que nós temos um objeto do tipo, `Responsavel`, isso também significa que nossa consulta foi realizada com sucesso.

> **E se a consulta não fosse realizada com sucesso?**

Nós, teríamos a seguinte saída:

**OUTPUT:**
```bash
Type: <class 'NoneType'>
Resultado: None
```

> **E como acessar os campos da nossa classe (table)?**

Simples, veja a continuação do código abaixo:

```python
# driver.py

from app.db.session import SessionLocal

session = SessionLocal()

from app.repositories.responsavel_repository import get_responsavel_by_phone

responsavel = get_responsavel_by_phone(
    session,
    phone="558396241699",
)

if responsavel:
    print("Responsável encontrado:")
    print(f"ID: {responsavel.id}")
    print(f"Nome: {responsavel.nome}")
    print(f"Telefone: {responsavel.telefone}")
else:
    print("Responsável não encontrado.")
```

</details>

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
