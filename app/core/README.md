# `⚙️ core/`

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

O módulo `config.py` é responsável por carregar variáveis de ambiente e centralizar configurações do projeto.




















---

<div id="class-settings"></div>

## `class Settings`

> A classe Settings centraliza as configurações da aplicação.

 - Ela carrega valores definidos no arquivo `.env` e os disponibiliza para o restante do sistema através de atributos:
   - Por exemplo: `DATABASE_URL`

[config.py](config.py)
```python
"""
Configuration module for application settings.

This module loads environment variables and provides
centralized configuration for the system.
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Application settings loader.

    Attributes
    ----------
    DATABASE_URL : str
        Database connection string.
    """

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")


# Settings class instance
settings = Settings()
```

---


**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
