# `📡 api/`

 - A camada de entrada da aplicação.
 - É onde ficam os endpoints da API.
 - Ela **recebe requisições HTTP** e **devolve respostas HTTP**.

## Conteúdo

 - [health.py](#health-py)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="health-py"></div>

## `health.py`

> Este arquivo define um endpoint de verificação de *saúde da API (/health)*.

 - Ele é utilizado para confirmar rapidamente se a aplicação está em execução e respondendo corretamente às requisições, sendo muito útil para monitoramento, testes e validações de infraestrutura.

[health.py](health.py)
```python
"""
Healthcheck endpoint module.
Used to verify if the API is running correctly.
"""

from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Health check endpoint.

    Returns
    -------
    dict
        API status confirmation.

    Examples
    --------
    >>> GET /health
    {"status": "ok"}
    """
    return {"status": "ok"}
```

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
