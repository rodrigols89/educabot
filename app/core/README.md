# `⚙️ core/`

> O diretório `⚙️ core/` é responsável por *"guarda configurações globais do sistema"*.

## Conteúdo

 - [`config.py`](#config-py)
   - [`class Settings`](#class-settings)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="config-py"></div>

## `config.py`

> O arquivo `config.py` centraliza todas as configurações da aplicação carregadas a partir dos arquivos `.env`.

Ele fornece acesso a:

 - PostgreSQL
 - Evolution API
 - futuras configurações do sistema





---

<div id="class-settings"></div>

## `class Settings`

> A classe Settings centraliza as configurações da aplicação.

 - Ela carrega valores definidos no arquivo `.env` e os disponibiliza para o restante do sistema através de atributos:
   - Por exemplo: `DATABASE_URL`

[config.py](config.py)
```python
# app/core/config.py

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "",
    )

    CONFIG_SESSION_PHONE_VERSION: str = os.getenv(
        "CONFIG_SESSION_PHONE_VERSION",
        "",
    )

    AUTHENTICATION_API_KEY: str = os.getenv(
        "AUTHENTICATION_API_KEY",
        "",
    )

    DATABASE_PROVIDER: str = os.getenv(
        "DATABASE_PROVIDER",
        "",
    )

    DATABASE_CONNECTION_URI: str = os.getenv(
        "DATABASE_CONNECTION_URI",
        "",
    )

    CACHE_REDIS_URI: str = os.getenv(
        "CACHE_REDIS_URI",
        "",
    )

    CACHE_REDIS_PREFIX_KEY: str = os.getenv(
        "CACHE_REDIS_PREFIX_KEY",
        "",
    )

    EVOLUTION_API_URL: str = os.getenv(
        "EVOLUTION_API_URL",
        "http://localhost:8080",
    )

    EVOLUTION_INSTANCE: str = os.getenv(
        "EVOLUTION_INSTANCE",
        "",
    )


settings = Settings()
```

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
