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

O módulo `config.py` é responsável por carregar variáveis de ambiente e centralizar configurações do projeto.




















---

<div id="class-settings"></div>

## `class Settings`

> A classe Settings centraliza as configurações da aplicação.

 - Ela carrega valores definidos no arquivo `.env` e os disponibiliza para o restante do sistema através de atributos:
   - Por exemplo: `DATABASE_URL`

[config.py](config.py)
```python
import os

from dotenv import load_dotenv

load_dotenv()


class Settings:

    DATABASE_URL: str = os.getenv("DATABASE_URL", "")


# Settings class instance
settings = Settings()
```

---


**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
