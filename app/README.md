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

### `Exemplo visual`

```text
Cliente
   │
   ▼
/api
   │
   ▼
service
```





















---

<div id="core-folder"></div>

## `⚙️ core/`

 - Guarda configurações globais do sistema.
 - Tudo que é central para a aplicação fica aqui.

### `Exemplo visual`

```text
           core
          / | \
         /  |  \
        /   |   \
settings    |    logging
            |
           auth
```





















---

<div id="db-folder"></div>

## `🗄️ db/`

> Camada responsável pela conexão com o banco.

Responsabilidades:

 - Engine SQLAlchemy
 - Session
 - Base ORM

### `Exemplo visual`

```text
Application
     │
     ▼
    db
     │
     ▼
 PostgreSQL
```





















---

<div id="models-folder"></div>

## `🏛️ models/`

 - Representa as tabelas do banco.
 - Cada classe equivale a uma tabela.

### `Exemplo visual`

```text
Model SQLAlchemy
       │
       ▼
Tabela PostgreSQL
```





















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

### `Exemplo visual`

```text
Service
   │
   ▼
Repository
   │
   ▼
Banco
```





















---

<div id="schemas-folder"></div>

## `📦 schemas/`

> Modelos Pydantic usados para entrada e saída de dados da API.

Responsabilidades:

> Validar dados da API.

### `Exemplo visual`

```text
JSON recebido
      │
      ▼
Schema
      │
      ▼
Service
```





















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

> **Ponto de entrada da aplicação.**  
> É o primeiro arquivo carregado pelo Uvicorn.

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

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
