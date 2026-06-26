# `📡 api/`

 - A camada de entrada da aplicação.
 - É onde ficam os endpoints da API.
 - Ela **recebe requisições HTTP** e **devolve respostas HTTP**.

## Conteúdo

 - [`webhook.py`](#webhook-py)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="webhook-py"></div>

## `webhook.py`

> O arquivo `webhook.py` será responsável por *receber os eventos enviados pela Evolution API*.

Sempre que alguém enviar uma mensagem para o WhatsApp conectado à Evolution, a Evolution fará uma requisição HTTP para sua API:

```bash
WhatsApp
    ↓
Evolution API
    ↓
POST /webhook/evolution
    ↓
FastAPI
```

[webhook.py](webhook.py)
```python
# app/api/webhook.py

from typing import Any

from fastapi import APIRouter, Request

from app.db.session import SessionLocal
from app.models.pedido import TipoPedido
from app.services.command_service import is_valid_command
from app.services.evolution_client import send_whatsapp_message
from app.services.notification_service import build_supplier_message
from app.services.pedido_service import create_order
from app.services.responsavel_service import check_responsavel
from app.utils.evolution_parser import parse_evolution_message
from app.utils.logger import print_separator

router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"],
)


@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    print("\n")
    print_separator()

    payload: dict[str, Any] = await request.json()

    phone, text = parse_evolution_message(payload=payload)

    is_command = is_valid_command(text=text)

    if not is_command:
        print_separator()
        return {"status": "received"}

    session = SessionLocal()

    try:
        responsavel = check_responsavel(
            db=session,
            phone=phone,
        )

        if responsavel is None:
            print_separator()
            return {"status": "received"}

        pedido, tipo = create_order(
            db=session,
            responsavel=responsavel,
            command=text,
        )

        if pedido is None:
            tipo_nome = (
                "gás" if tipo == TipoPedido.GAS else "água"
            )

            message = (
                f"⚠️ Você já fez um pedido de {tipo_nome} hoje.\n"
                "Por favor, aguarde o atendimento do seu pedido atual."
            )

            send_whatsapp_message(
                phone=phone,
                message=message,
            )
            print_separator()
            return {"status": "received"}

        supplier_phone, message = build_supplier_message(
            responsavel=responsavel,
            tipo=pedido.tipo,
        )

        sent = send_whatsapp_message(
            phone=supplier_phone,
            message=message,
        )

        print("SUPPLIER MSG CHEKING:")

        if sent:

            print("Mensagem enviada ao forncedor com sucesso!")

            confirmation_message = (
                "✅ Seu pedido foi realizado com sucesso!"
            )

            send_whatsapp_message(
                phone=phone,
                message=confirmation_message,
            )

        else:

            print("Não foi possível enviar sua mensagem ao fornecedor.")

            unconfirmation_message = (
                "Não foi possível enviar sua mensagem ao fornecedor.\n"
                "Por favor, entre em contato com Rodrigo."
            )

            send_whatsapp_message(
                phone=phone,
                message=unconfirmation_message,
            )

    finally:
        session.close()

    print_separator()

    return {"status": "received"}
```

<details>

<summary>Explicação Passo a Passo (Step-by-Step)</summary>

<br/>

Para implementar esse endpoint vamos começar criando uma rota simples que vai apenas retornar um dicionários de strings (como um JSON):

```python
from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/webhook",
    tags=["Webhook"],
)


@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    return {"status": "received"}
```

> **NOTE:**  
> Vejam que nós estamos trabalhando de modo **assíncrono (async)**.

Sabendo que essa função (endpoint) vai receber um `request`, vamos capturar esse `request` de forma *assíncrona*:

```python
from typing import Any

@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    payload: dict[str, Any] = await request.json()

    return {"status": "received"}
```

**NOTE:**  
Se você der um print na saída desse `payload`, verá algo como isso (para essa versão do Evolution Go):

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

Os campos mais importantes (para essa aplicação) do JSON acima são:

 - `data -> key -> "fromMe"`
   - `"fromMe": true`
     - Indica que foi eu mesmo quem enviei a mensagem.
   - `"fromMe": false`
     - Indica que alguém enviou uma mensagem para mim.

A partir dessas informações nós vamos chamar a função `parse_evolution_message()` que será responsável por:

 - Identificar se a mensagem foi enviada por mim ou não (com o cmapo fromMe).
 - Pegar o número de quem enviou a mensagem + a mensagem enviada.

```python
from app.utils.evolution_parser import parse_evolution_message

@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    print("\n")
    print_separator()

    payload: dict[str, Any] = await request.json()

    phone, text = parse_evolution_message(payload=payload)

    print_separator()

    return {"status": "received"}
```

Ótimo, agora sabendo que nós sempre vamos receber um número de telefone e uma mensagem, vamos começar verificando se a mensagem que nós recebemos representar um comando válido:

 - `/gas`
 - `/agua`

Para isso, vamos utilizar a função `is_valid_command()` que retorna:

 - `True`
   - Quando o comando é válido.
 - `False`
   - Quando o comando é inválido.

```python
from app.services.command_service import is_valid_command
from app.utils.evolution_parser import parse_evolution_message

@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    print("\n")
    print_separator()

    payload: dict[str, Any] = await request.json()

    phone, text = parse_evolution_message(payload=payload)

    is_command = is_valid_command(text=text)

    print_separator()

    return {"status": "received"}
```

Com essa informação o próximo passo agora será parar a função (endpoint) quando receber um **comando inválido (is_command=False)**:

```python
from app.services.command_service import is_valid_command

@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    print("\n")
    print_separator()

    payload: dict[str, Any] = await request.json()

    phone, text = parse_evolution_message(payload=payload)

    is_command = is_valid_command(text=text)

    if not is_command:
        print_separator()
        return {"status": "received"}

    print_separator()

    return {"status": "received"}
```

Ótimo, agora **se o comando for válido (is_command=True)** nós vamos:

 - Abrir uma conexão (sessão) com o Banco de Dados.
 - Verificar se o responsável (número) pelo pedido está cadastrado no Banco de Dados.
 - Por fim, vamos validar se o responsável está ativo, ou seja, tem permissão para fazer o pedido:
   - **Se ele não estiver ativo ou cadastrado vamos parar a função (endpoint).**

```python
from app.services.responsavel_service import check_responsavel

@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    ...

    session = SessionLocal()

    try:
        responsavel = check_responsavel(
            db=session,
            phone=phone,
        )

        if responsavel is None:
            print_separator()
            return {"status": "received"}
    finally:
        session.close()

    print_separator()

    return {"status": "received"}
```

A função `check_responsavel()` vai retornar:

 - `None`
   - Se o responsável pelo pedido não estiver ativo ou cadastrado no sistema.
 - `Responsável`
   - Se ele estiver cadastrado **e (^, conjunção)** ativo no sistema.

O próximo passo agora vai ser criar um pedido para esse `responsavel` que passou na validação:

```python
@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    ...

    session = SessionLocal()

    try:
        responsavel = check_responsavel(
            db=session,
            phone=phone,
        )

        if responsavel is None:
            print_separator()
            return {"status": "received"}

        pedido, tipo = create_order(
            db=session,
            responsavel=responsavel,
            command=text,
        )

    finally:
        session.close()

    print_separator()

    return {"status": "received"}
```

A função `create_order()` vai nós retornar:

 - `pedido`
   - Esse pedido vai ser `None` se já houver um pedido dessa categoria no dia de hoje.
   - Senão, nós vamos ter o resultado do pedido salvo no Banco de Dados.
 - `tipo`
   - Se nós chegamos até aqui é porque o tipo do pedido foi validado como um comando válido:
     - `/gas`
     - `/agua`
   - Nesse caso ele nunca será `None`.

Com essas 2 novas informações (pedido e tipo) nós podemos *deduzir* o seguinte:

> Primeiro, se o **pedido** for `None` significa que já foi feito um pedido dessa categoria hoje.

Logo, vamos parar a função (endpoint) e enviar uma mensagem para quem fez o pedido dizendo que ela já fez um pedido desse tipo hoje:

```python
from app.models.pedido import TipoPedido
from app.services.evolution_service import send_whatsapp_message
from app.services.pedido_service import create_order


@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    ...

    session = SessionLocal()

    try:
        
        ...

        pedido, tipo = create_order(
            db=session,
            responsavel=responsavel,
            command=text,
        )

        if pedido is None:
            tipo_nome = (
                "gás" if tipo == TipoPedido.GAS else "água"
            )

            message = (
                f"⚠️ Você já fez um pedido de {tipo_nome} hoje.\n"
                "Por favor, aguarde o atendimento do seu pedido atual."
            )

            send_whatsapp_message(
                phone=phone,
                message=message,
            )
            print_separator()
            return {"status": "received"}

    finally:
        session.close()

    print_separator()

    return {"status": "received"}
```

Ótimo! Agora, se algum responsável que já tiver feito um pedido da mesma categoria (tipo) no mesmo dia realizar uma nova solicitação, receberá a seguinte mensagem no WhatsApp:

```text
⚠️ Você já fez um pedido de água hoje.
Por favor, aguarde o atendimento do seu pedido atual.
```

> E se ele não fez nenhuma pedido dessa categoria?

Bem, então nós vamos:

 - **Chamar a função `build_supplier_message()`:**
   - Que tem como objetivo criar uma mensagem específica para cada fornecedor de acordo com o tipo do pedido.
   - Essa função retorna:
     - O contato do fornecedor.
     - A mensagem específica para esse tipo de serviço (categoria).
 - **Enviar essa mensagem para o fornecedor específico do serviço (categoria):**
   - Lembrando que a função `send_whatsapp_message()` sempre recebe o número de telefone para quem enviar uma mensagem + a mensagem que será enviada.

```python
from app.db.session import SessionLocal
from app.models.pedido import TipoPedido
from app.services.evolution_service import send_text_message
from app.services.pedido_service import create_order
from app.services.notification_service import build_supplier_message


@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    ...

    session = SessionLocal()

    try:
        responsavel = check_responsavel(
            db=session,
            phone=phone,
        )

        if responsavel is None:
            print_separator()
            return {"status": "received"}

        pedido, tipo = create_order(
            db=session,
            responsavel=responsavel,
            command=text,
        )

        if pedido is None:
            tipo_nome = (
                "gás" if tipo == TipoPedido.GAS else "água"
            )

            message = (
                f"⚠️ Você já fez um pedido de {tipo_nome} hoje.\n"
                "Por favor, aguarde o atendimento do seu pedido atual."
            )

            send_whatsapp_message(
                phone=phone,
                message=message,
            )
            print_separator()
            return {"status": "received"}

        supplier_phone, message = build_supplier_message(
            responsavel=responsavel,
            tipo=pedido.tipo,
        )

        sent = send_whatsapp_message(
            phone=supplier_phone,
            message=message,
        )

    finally:
        session.close()

    print_separator()

    return {"status": "received"}
```

Ótimo, conseguimos enviar uma mensagem para um fornecedor específico com uma mensagem específico.

> **É só isso? NÃO!**  
> Agora, nós precisamos notificar a quem fez o pedido que seu pedido foi realizado com sucesso.

Bem, como nós sabemos a função `send_whatsapp_message()` vai nos retornar os seguintes cenários:

 - `True`
   - Se a mensagem foi enviada com sucesso (HTTP 200 ou 201).
 - `False`
   - Caso ocorra falha na requisição ou resposta inválida.

Sabendo disso, nós vamos fazer o seguinte:

 - **Se `sent` for `True` nós vamos:**
   - Enviar uma mensagem para o usuário dizendo que seu pedido foi realizado com sucesso.
 - **Senão:**
   - Houve, algum problema ao contactar o fornecedor e vamos mandar uma mensagem para quem fez o pedido entrar em contato com o responsável pelo suporte ao sistema.

```python
# app/api/webhook.py

@router.post("/evolution")
async def evolution_webhook(
    request: Request,
) -> dict[str, str]:

    ...


        if sent:

            print("Mensagem enviada ao forncedor com sucesso!")

            confirmation_message = (
                "✅ Seu pedido foi realizado com sucesso!"
            )

            send_whatsapp_message(
                phone=phone,
                message=confirmation_message,
            )

        else:

            print("Não foi possível enviar sua mensagem ao fornecedor.")

            unconfirmation_message = (
                "Não foi possível enviar sua mensagem ao fornecedor.\n"
                "Por favor, entre em contato com Rodrigo."
            )

            send_whatsapp_message(
                phone=phone,
                message=unconfirmation_message,
            )

    finally:
        session.close()

    print_separator()

    return {"status": "received"}
```

</details>

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
