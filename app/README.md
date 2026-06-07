# `📁 app/`

A pasta `app/` é a raiz da aplicação. Ela funciona como o "container lógico" de todo o código do sistema.

> **NOTE:**  
> Em outras palavras, tudo que faz parte da API fica organizado dentro dela.

## Conteúdo

 - [`📡 api/`](#api-folder)
 - [`⚙️ core/`](#core-folder)
 - [`🗄️ db/`](#db-folder)
 - [`🏛️ models/`](#models-folder)
 - [`📚 repositories/`](#repositories-folder)
 - [`📦 schemas/`](#schemas-folder)
 - [`🧠 services/`](#services-folder)
 - [🔧 utils/`](#utils-folder)
 - [`🚀 main.py`](#main-py)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="api-folder"></div>

## `📡 api/`

 - A camada de entrada da aplicação.
 - É onde ficam os endpoints da API.
 - Ela **recebe requisições HTTP** e **devolve respostas HTTP**.






















---

<div id="core-folder"></div>

## `⚙️ core/`

 - Guarda configurações globais do sistema.
 - Tudo que é central para a aplicação fica aqui.






















---

<div id="db-folder"></div>

## `🗄️ db/`

> Camada responsável pela conexão com o Banco de Dados.

Responsabilidades:

 - Engine SQLAlchemy
 - Session
 - Base ORM






















---

<div id="models-folder"></div>

## `🏛️ models/`

 - Representa as tabelas do Banco de Dados.
 - Cada classe equivale a uma tabela.






















---

<div id="repositories-folder"></div>

## `📚 repositories/`

> Camada responsável por conversar diretamente com o banco.

Responsabilidades:

 - **Executar:**
   - SELECT
   - INSERT
   - UPDATE
   - DELETE






















---

<div id="schemas-folder"></div>

## `📦 schemas/`

> Modelos Pydantic usados para entrada e saída de dados da API.

Responsabilidades:

> Validar dados da API.






















---

<div id="services-folder"></div>

## `🧠 services/`

> **Aqui ficam as regras de negócio.**  
> É uma das camadas mais importantes.

Responsabilidades:

> Tomar decisões.

### `Exemplo`

Regra:

```text
Somente gestores podem criar pedidos.
```

Essa lógica NÃO deve ficar:

* no endpoint
* no repository

Ela fica no service.






















---

<div id="utils-folder"></div>

## `🔧 utils/`

> **Funções auxiliares reutilizáveis.**

Responsabilidades:

> Guardar coisas que podem ser usadas em vários lugares.

Exemplos:

* formatar telefone
* validar CPF
* gerar UUID
* datas





















---

<div id="main-py"></div>

## `🚀 main.py`

> **Responsável por inicializar a aplicação.**

 - É o ponto de entrada da aplicação.
 - Primeiro arquivo carregado pelo Uvicorn.

### `Exemplo visual`

```text
uvicorn app.main:app
          │
          ▼
       main.py
          │
          ▼
      FastAPI()
```

[main.py](main.py)
```python
from fastapi import FastAPI

from app.api.gestores import router as gestores_router
from app.api.health import router as health_router
from app.api.pedidos import router as pedidos_router
from app.api.webhook import router as webhook_router

app = FastAPI(
    title="WhatsApp Orders API",
    version="1.0.0",
)


app.include_router(gestores_router)
app.include_router(pedidos_router)
app.include_router(webhook_router)
app.include_router(health_router)
```

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
