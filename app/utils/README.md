# `🔧 utils/`

> O diretório `🔧 utils/` é responsável por *"guardar coisas que podem ser usadas em vários lugares"*.

Por, exemplo:

 - Formatar telefone
 - Validar CPF
 - Gerar UUID

## Conteúdo

 - [`evolution_parser.py`](#evolution-parser-py)
 - [`insert_responsavel_example.py`](#insert-responsavel-example.py)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="evolution-parser-py"></div>

## `evolution_parser.py`

> O arquivo `evolution_parser.py` vai ser responsável por aplicar parsers nos dados que vem da *Evolution API*.

[evolution_parser.py](evolution_parser.py)
```python
# app/utils/evolution_parser.py

from typing import Any


def parse_evolution_message(
    payload: dict[str, Any],
) -> tuple[str | None, str | None]:

    data: dict[str, Any] = payload.get(
        "data",
        {}
    )

    key: dict[str, Any] = data.get(
        "key",
        {}
    )

    message: dict[str, Any] = data.get(
        "message",
        {}
    )

    from_me: bool = key.get(
        "fromMe",
        False,
    )

    text: str = message.get(
        "conversation",
        "",
    )

    if from_me:
        print("\n========================================")
        print("EVOLUTION PARSER PROCESS")
        print("========================================")
        print("fromMe (True)")
        print(f"Text: {text}")
        print("========================================\n")

        return None, None

    phone: str = key.get(
        "senderPn",
        "",
    ).replace(
        "@s.whatsapp.net",
        "",
    )

    print("\n========================================")
    print("EVOLUTION PARSER PROCESS")
    print("========================================")
    print("fromMe (False)")
    print(f"Phone: {phone}")
    print(f"Text: {text}")
    print("========================================")

    return phone, text
```

<details>

<summary>Explicação Passo a Passo (Step-by-Step)</summary>

<br/>

> Aqui, nós vamos entender como essa função é (pode ser) utilizada.

Bem, para essa versão do Evolution Go que nós estamos trabalhando quando alguém envia nós recebemos um JSON parecido com esse:

```json
{
  "event": "messages.upsert",
  "instance": "educabot",
  "data": {
    "key": {
      "remoteJid": "168582063366331@lid",
      "fromMe": false,
      "id": "3EB06F9FD670807D6E4597",
      "senderPn": "558396241663@s.whatsapp.net"
    },
    "pushName": "Deus, meu refugio",
    "status": "DELIVERY_ACK",
    "message": {
      "messageContextInfo": {
        "deviceListMetadata": {
          "senderKeyHash": "0I4ZvIC7QjWF6A==",
          "senderTimestamp": "1781564354",
          "senderAccountType": "E2EE",
          "receiverAccountType": "E2EE",
          "recipientKeyHash": "qOe97S5e60w6cw==",
          "recipientTimestamp": "1782250066"
        },
        "deviceListMetadataVersion": 2,
        "messageSecret": "YqfQ1oIM0hyCCfrcGxUAZoiIvrBY1ePUR34R+3g+8BU=",
        "limitSharingV2": {
          "trigger": "UNKNOWN",
          "initiatedByMe": false
        }
      },
      "conversation": "Boa noite."
    },
    "contextInfo": {
      "ephemeralSettingTimestamp": "1779497722",
      "disappearingMode": {
        "initiator": "CHANGED_IN_CHAT",
        "trigger": "CHAT_SETTING",
        "initiatedByMe": true
      }
    },
    "messageType": "conversation",
    "messageTimestamp": 1782254348,
    "instanceId": "51349292-4f0f-4324-b5cb-662ae76d385a",
    "source": "web"
  },
  "destination": "http://172.17.0.1:8000/webhook/evolution",
  "date_time": "2026-06-23T19:39:08.809Z",
  "sender": "558393885557@s.whatsapp.net",
  "server_url": "http://localhost:8080",
  "apikey": "8kL29xPq7mN4vZsT1yRwC5"
}

INFO:     172.18.0.4:56594 - "POST /webhook/evolution HTTP/1.1" 200 OK
```

 - `data -> key -> "fromMe"`
   - Indica se foi você (True) ou não (False) quem enviou a mensagem.
 - `data -> key -> "senderPn"`
   - Esse campo só aparece quando você recebe uma mensage, pois é o número de telefone de quem enviou a mensage.

Sabendo disso, nós vamos manipular esse JSON a nosso favor:

```python
data: dict[str, Any] = payload.get(
    "data",
    {}
)
```

No código acima nós estamos utilizando o método `get()` para pegar exatamente a chave `data`:

```python
{
    "key": {...},
    "pushName": "Deus, meu refugio",
    "message": {...},
    ...
}

Vai virar isso:

data = {
    "key": {...},
    "pushName": "Deus, meu refugio",
    "message": {...},
    ...
}
```

> **NOTE:**  
> A mesma lógica vai ser utilizada nas outras partes que utilizam a função `get()`.

```python
phone: str = key.get(
    "senderPn",
    "",
).replace(
    "@s.whatsapp.net",
    "",
)
```

Já no código acima nós estamos:

 - Pegando o campo `"senderPn"` da chave `key` (com `.get()`)
 - E substituindo `"@s.whatsapp.net"` por um caractere vazio:
   - Ou seja, estamos removendo `"@s.whatsapp.net"`
   - Logo, só vai ficar o número de telefone de quem enviou a mensagem

> **NOTE:**  
> As demais partes do código acredito que já estejam muito explícitas e não precisem de mais explicações.

</details>




















---

<div id="insert-responsavel-example.py"></div>

## `insert_responsavel_example.py`

> O script `insert_responsavel_example.py` é um modelo que pode ser utilizado para quem desejar inserir os responsáveis pelos pedidos automatimente (sem precisa utilizar a API).

[insert_responsavel_example.py](insert_responsavel_example.py)
```python
# app/utils/insert_responsavel_example.py

"""
From Root dir run the command below:
python -m app.utils.insert_responsavel_example
"""

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.responsavel import Responsavel

RESPONSAVEIS = [
    {
        "nome": "nome do responsavel",
        "telefone": "telefone do responsavel",
        "instituicao": "instituição do responsavel",
        "pode_pedir_gas": True,
        "pode_pedir_agua": True,
    }
]


def responsavel_exists(db: Session, telefone: str) -> bool:
    return (
        db.query(Responsavel)
        .filter(Responsavel.telefone == telefone)
        .first()
        is not None
    )


def insert_responsaveis() -> None:
    db: Session = SessionLocal()

    try:
        for data in RESPONSAVEIS:
            if responsavel_exists(db, data["telefone"]):
                continue

            db.add(Responsavel(**data))

        db.commit()
        print("Responsáveis inseridos com sucesso.")

    finally:
        db.close()


if __name__ == "__main__":
    insert_responsaveis()
```

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
