# `💼 clients/`

## Conteúdo

 - [`evolution_client.py`](#evolution-client-py)
   - [`send_text_message()`](#send-text-message)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="evolution-client-py"></div>

## `evolution_client.py`

 - Esse arquivo é um `cliente HTTP`.
 - Ele serve para **conversar com a Evolution API**.

Pense nele assim:

```bash
FastAPI
   ↓
evolution_client.py -> send_text_message()
   ↓
Evolution API
   ↓
WhatsApp
```





---

<div id="send-text-message"></div>

## `send_text_message()`

> A função `send_text_message()` envia uma mensagem de texto para um determinado número no WhatsApp (diferente do que você registrou no Evolution API).

Por exemplo:

```python
send_text_message(
    phone="5583999999999",
    text="Hello World!",
)
```

[evolution_client.py](evolution_client.py)
```python
from typing import Any

import requests

from app.core.config import settings


def send_text_message(
    phone: str,
    text: str,
) -> dict[str, Any]:

    url: str = (
        f"{settings.EVOLUTION_API_URL}"
        f"/message/sendText/"
        f"{settings.EVOLUTION_INSTANCE}"
    )

    payload: dict[str, Any] = {
        "number": phone,
        "textMessage": {
            "text": text,
        },
    }

    headers: dict[str, str] = {
        "apikey": settings.EVOLUTION_API_KEY,
        "Content-Type": "application/json",
    }

    response = requests.post(
        url=url,
        json=payload,
        headers=headers,
        timeout=30,
    )

    print("\n=== EVOLUTION RESPONSE ===")
    print(response.status_code)
    print(response.text)
    print("==========================\n")

    response.raise_for_status()

    return response.json()
```

<details>

<summary>Explicação Passo a Passo (Step-by-Step)</summary>

<br/>

> Agora vamos explicar algumas partes importantes do código acima.

### `Montando a URL`

```python
url: str = (
    f"{settings.EVOLUTION_API_URL}"
    f"/message/sendText/"
    f"{settings.EVOLUTION_INSTANCE}"
)
```

O código acima montar a URL que será chamada na Evolution API, por exemplo:

```python
url = (
    "http://localhost:8080"
    "/message/sendText/"
    "educabot"
)
```

Resultado:

 - [http://localhost:8080/message/sendText/educabot](http://localhost:8080/message/sendText/educabot)

### `Montando o Payload`

```python
payload: dict[str, Any] = {
    "number": phone,
    "textMessage": {
        "text": text,
    },
}
```

O código acima montar o `JSON` que será enviado para a Evolution.

Supondo que nós enviamos a seguinte mensagem:

```python
send_text_message(
    phone="5583996241663",
    text="Bom dia!"
)
```

O resultado seria:

```json
{
    "number": "5583996241663",
    "textMessage": {
        "text": "Bom dia!"
    }
}
```

### `Montando os Headers`

```python
headers: dict[str, str] = {
    "apikey": settings.EVOLUTION_API_KEY,
    "Content-Type": "application/json",
}
```

### `Enviando a Requisição`

```python
response = requests.post(
    url=url,
    json=payload,
    headers=headers,
    timeout=30,
)
```

> O código acima envia *uma requisição HTTP POST*.

Equivalente ao curl:

```bash
curl -X POST \
  http://localhost:8080/message/sendText/educabot \
  -H "apikey: 8kL29xPq7mN4vZsT1yRwC5" \
  -H "Content-Type: application/json" \
  -d '{
    "number": "5583996241663",
    "textMessage": {
      "text": "Bom dia!"
    }
  }'
```

> **O que retorna?**  
> O requests devolve um objeto `Response`.

Por exemplo:

```bash
<Response [200]>
```

### `Verificando se a Requisição foi bem-sucedida`

```python
response.raise_for_status()
```

> O código acima verificar se deu erro.

**Cenário 1 (Sucesso):**

```bash
Status:
- 200
- 201

Nada acontece.
O programa continua.
```

**Cenário 2 (Erro):**

```bash
Status:
- 400
- 401
- 500

Então:
response.raise_for_status() gera uma exceção.

Exemplo:
requests.exceptions.HTTPError
```

### `Retornando o Resultado`

```python
return response.json()
```

> O código acima **transforma** o `JSON` recebido da Evolution em um `dicionário Python` - `json()`.

Imagine que o retorno da Evolution seja:

```json
{
  "key": {
    "remoteJid": "558396241663@s.whatsapp.net",
    "fromMe": true,
    "id": "3EB03881DBEAC46254107F"
  },
  "message": {
    "extendedTextMessage": {
      "text": "Bom dia!"
    }
  },
  "messageTimestamp": "1780868638",
  "status": "PENDING"
}
```

Isso será transformado em algo parecido com isso:

```json
{
    "key": {
        "remoteJid":
            "558396241663@s.whatsapp.net",
        "fromMe": True,
        "id": "3EB03881DBEAC46254107F",
    },
    "message": {
        "extendedTextMessage": {
            "text": "Bom dia!",
        },
    },
    "messageTimestamp": "1780868638",
    "status": "PENDING",
}
```

### `Fluxo completo`

```bash
send_text_message()
       │
       ▼
Monta URL
       │
       ▼
http://localhost:8080/message/sendText/educabot
       │
       ▼
Monta payload
       │
       ▼
{
  "number": "5583996241663",
  "textMessage": {
      "text": "Bom dia!"
  }
}
       │
       ▼
requests.post(...)
       │
       ▼
Evolution API
       │
       ▼
WhatsApp
       │
       ▼
Resposta JSON
       │
       ▼
response.json()
       │
       ▼
dict[str, Any]
       │
       ▼
return
```

</details>

<details>

<summary>Teste</summary>

<br/>

Para testar essa função você pode criar um arquivo chamado `driver.py` na raiz do projeto e executar o seguinte código:

```python
# driver.py

from app.clients.evolution_client import (
    send_text_message,
)

response = send_text_message(
    phone="5583996241663",
    text="Hello World!",
)

print(response)
```

**No WhatsApp**: `5583996241663`
```bash
Hello World!
```

**No terminal:**
```
=== EVOLUTION RESPONSE ===
201
{"key":{"remoteJid":"558396241663@s.whatsapp.net","fromMe":true,"id":"3EB0EAB557613B285C5837"},"message":{"extendedTextMessage":{"text":"Hello World!"}},"messageTimestamp":"1780873653","status":"PENDING"}
==========================

{'key': {'remoteJid': '558396241663@s.whatsapp.net', 'fromMe': True, 'id': '3EB0EAB557613B285C5837'}, 'message': {'extendedTextMessage': {'text': 'Hello World!'}}, 'messageTimestamp': '1780873653', 'status': 'PENDING'}
```

> **NOTE:**  
> Porém, no servidor do FastAPI não vai mostrar nada porque nós não estamos passando por lá, estamos enviando diretamente para a Evolution API.

Outra maneiras de testar se está funcionando corretamente é utilizando a ferramente `curl`:

```bash
curl -X POST \
  http://localhost:8080/message/sendText/educabot \
  -H "Content-Type: application/json" \
  -H "apikey: 8kL29xPq7mN4vZsT1yRwC5" \
  -d '{
    "number": "5583996241663",
    "textMessage": {
      "text": "Hello World!"
    }
  }'
```

**OUTPUT:**
```bash
{"key":{"remoteJid":"558396241663@s.whatsapp.net","fromMe":true,"id":"3EB03EC402F089AD0DCE86"},"message":{"extendedTextMessage":{"text":"Hello World!"}},"messageTimestamp":"1780875143","status":"PENDING"}%
```

> **NOTE:**  
> Vejam que nós `estamos enviando uma requisição POST` direto para o serviço da Evolution API (na porta 8080) e não no FastAPI (que rota na porta 8000).

</details>

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
