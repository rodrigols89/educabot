# `📡 api/`

 - A camada de entrada da aplicação.
 - É onde ficam os endpoints da API.
 - Ela **recebe requisições HTTP** e **devolve respostas HTTP**.

## Conteúdo

 - [`gestores.py`](#gestores-py)
   - [`create_manager`](#create-manager)
   - [`list_managers`](#list-managers)
 - [`health.py`](#health-py)
 - [`pedidos.py`](#pedidos-py)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="gestores-py"></div>

## `gestores.py`

> O arquivo `gestores.py` será responsável pelos endpoints relacionados aos gestores.





---

<div id="create-manager"></div>

## `create_manager`

> Endpoint responsável por cria um novo gestor no sistema.

[gestores.py](gestores.py)
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.gestor import Gestor
from app.schemas.gestor import GestorCreate, GestorResponse

router = APIRouter(
    prefix="/gestores",
    tags=["Gestores"],
)


@router.post(
    "",
    response_model=GestorResponse,
    status_code=201,
)
def create_manager(
    payload: GestorCreate,
    db: Session = Depends(get_db),
) -> Gestor:

    gestor = Gestor(**payload.model_dump())
    db.add(gestor)  # add to db
    db.commit()  # save
    db.refresh(gestor)  # refresh

    return gestor
```

<details>

<summary>Explicação Passo a Passo (Step-by-Step)</summary>

<br/>

```python
router = APIRouter(
    prefix="/gestores",
    tags=["Gestores"],
)
```

 - `APIRouter()`
   - Cria um agrupador de rotas do FastAPI.
   - É usado para organizar endpoints relacionados em módulos separados.
   - Facilita a manutenção e divisão da API.
 - `prefix="/gestores"`
   - Define um prefixo automático para todas as rotas do router.
   - Faz com que todas as URLs comecem com `/gestores`.
   - Exemplo: `@router.post("")` vira `POST /gestores`.
 - `tags=["Gestores"]`
   - Organiza as rotas na documentação Swagger/OpenAPI.
   - Cria uma seção chamada `Gestores`.
   - Ajuda a separar visualmente os endpoints por categoria.

```python
@router.post(
    "",
    response_model=GestorResponse,
    status_code=201,
)
```

* `response_model=GestorResponse`
  * Define o schema utilizado na resposta da API.
  * Garante que apenas os campos definidos em `GestorResponse` sejam enviados.
* `status_code=201`
  * Define o código HTTP retornado em caso de sucesso.
  * O código `201 Created` indica que um novo recurso foi criado.
  * É o status recomendado para operações de cadastro (`POST`).

```python
def create_manager(
    payload: GestorCreate,
    db: Session = Depends(get_db),
) -> Gestor:
```

* `payload: GestorCreate`
  * Recebe os dados enviados pelo cliente no corpo da requisição.
  * O FastAPI converte automaticamente o JSON para um objeto `GestorCreate`.
  * Também realiza validação dos dados recebidos.
* `db: Session = Depends(get_db)`
  * Recebe uma sessão do banco de dados criada pela função `get_db`.
  * Utiliza o sistema de injeção de dependências do FastAPI.
  * Permite executar operações no banco dentro da rota.
* `-> Gestor`
  * Indica que a função retorna um objeto do tipo `Gestor`.
  * É uma anotação de tipo (type hint).
  * Ajuda na documentação e na análise estática do código.

```python
gestor = Gestor(**payload.model_dump())
db.add(gestor)
db.commit()
db.refresh(gestor)

return gestor
```

* `gestor = Gestor(**payload.model_dump())`
  * Cria uma instância do modelo `Gestor`.
  * Converte os dados do schema Pydantic em um dicionário.
  * Preenche automaticamente os atributos do objeto.
* `db.add(gestor)`
  * Adiciona o objeto à sessão atual do SQLAlchemy.
  * Marca o registro para ser inserido no banco.
  * **Ainda não salva os dados definitivamente.**
* `db.commit()`
  * Confirma a transação atual.
  * Executa o `INSERT` no banco de dados.
  * Persiste as alterações de forma definitiva.
* `db.refresh(gestor)`
  * Recarrega os dados do objeto a partir do banco.
  * Atualiza campos gerados automaticamente, como o `id`.
  * Garante que o objeto esteja sincronizado com o banco.
* `return gestor`
  * Retorna o gestor recém-criado.
  * O FastAPI converte o objeto para JSON na resposta.
  * Os dados retornados seguem o `response_model` definido na rota.

</details>





---

<div id="list-managers"></div>

## `list_managers`

> Endpoint responsável por listar os gestores cadastrados no sistema.

[gestores.py](gestores.py)
```python

@router.get(
    "",
    response_model=list[GestorResponse],
)
def list_managers(
    db: Session = Depends(get_db),
) -> list[Gestor]:
    """
    List all managers.

    Returns
    -------
    list[Gestor]
        Registered managers.
    """

    return db.query(Gestor).all()
```


















---

<div id="health-py"></div>

## `health.py`

> Este arquivo define um endpoint de verificação de *saúde da API (/health)*.

[health.py](health.py)
```python
from fastapi import APIRouter

router = APIRouter(
    tags=["Healthcheck"],
)


@router.get("/health")
def health_check():
    return {"status": "ok"}
```


















---

<div id="pedidos-py"></div>

## `pedidos.py`

> Este arquivo define um endpoint de criação de pedidos.

[pedidos.py](pedidos.py)
```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.gestor import Gestor
from app.models.pedido import Pedido
from app.schemas.pedido import PedidoCreate, PedidoResponse
from app.services.pedido_service import create_request

router = APIRouter(
    prefix="/pedidos",
    tags=["Pedidos"],
)


@router.post(
    "",
    response_model=PedidoResponse,
    status_code=201,
)
def create_request_endpoint(
    payload: PedidoCreate,
    db: Session = Depends(get_db),
) -> Pedido:

    gestor = (
        db.query(Gestor)
        .filter(Gestor.id == payload.gestor_id)
        .first()
    )

    if gestor is None:
        raise HTTPException(
            status_code=404,
            detail="Manager not found.",
        )

    try:
        return create_request(
            db=db,
            gestor=gestor,
            command=payload.comando,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc


@router.get(
    "",
    response_model=list[PedidoResponse],
)
def list_requests(
    db: Session = Depends(get_db),
) -> list[Pedido]:
    """
    List all requests.
    """

    return db.query(Pedido).all()
```

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
