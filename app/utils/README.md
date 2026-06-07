# `🔧 utils/`

> O diretório `🔧 utils/` é responsável por *"guardar coisas que podem ser usadas em vários lugares"*.

Por, exemplo:

 - Formatar telefone
 - Validar CPF
 - Gerar UUID

## Conteúdo

 - [`evolution_parser.py`](#evolution-parser-py)
 - [`regex.py`](#regex-py)
   - [`validate_request_command()`](#validate-request-command)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="evolution-parser-py"></div>

## `evolution_parser.py`

> O arquivo `evolution_parser.py` conterá funções utilitárias para converter payloads da Evolution em schemas internos da aplicação.

Criamos em `/utils` porque futuramente essa lógica poderá ser reutilizada por:

 - webhook
 - testes
 - workers
 - processamento assíncrono

[evolution_parser.py](evolution_parser.py)
```python
from datetime import UTC, datetime
from typing import Any

from app.schemas.evolution import EvolutionMessage


def extract_message_text(
    message_data: dict[str, Any],
) -> str:

    if "conversation" in message_data:
        return message_data["conversation"]

    if "extendedTextMessage" in message_data:
        return (
            message_data["extendedTextMessage"]
            .get("text", "")
        )

    return ""


def parse_evolution_message(
    payload: dict[str, Any],
) -> EvolutionMessage:

    data: dict[str, Any] = payload["data"]

    sender: str = payload.get(
        "sender",
        "",
    )

    phone: str = sender.replace(
        "@s.whatsapp.net",
        "",
    )

    text: str = extract_message_text(
        data["message"]
    )

    return EvolutionMessage(
        phone=phone,
        text=text,
        name=data.get("pushName"),
        timestamp=datetime.fromtimestamp(
            data["messageTimestamp"],
            tz=UTC,
        ),
        from_me=data["key"]["fromMe"],
        message_type=data["messageType"],
    )
```

Se tudo ocorrer bem você receberá uma mensagem parecida com essa no terminal quando alguém ou você enviar uma mensagem:

**OUTPUT:**
```bash
=== EVOLUTION MESSAGE ===
Phone: 558393885557
Name: Rodrigo Leite 😎
Text: Aqueles códigos eu não te mandei aqui? Sumiram!
Type: extendedTextMessage
From Me: True
Timestamp: 2026-06-07 15:26:34+00:00
=========================
```




















---

<div id="regex-py"></div>

## `regex.py`

> O arquivo `regex.py` concentra **expressões regulares (Regex)** utilizadas pela aplicação para validação e extração de informações em textos.

 - Centralizar essas regras em um único local evita duplicação de código, facilita a manutenção e garante que todas as partes do sistema utilizem os mesmos padrões de validação.





---

<div id="validate-request-command"></div>

## `validate_request_command()`

A função `validate_request_command()` vai ser responsável por validar comandos como:

 - /gas
 - /agua

Ela garante:

 - Formato válido
 - Quantidade numérica:
   - Por enquanto, não vamos tratar isso, apenas 1 unidade por pedido será aceito por dia
 - Comando permitido

### `Código Completo`

[regex.py](regex.py)
```python
import re

REQUEST_COMMAND_PATTERN = r"^\/(gas|agua)$"


def validate_request_command(command: str) -> bool:

    return bool(
        re.match(
            REQUEST_COMMAND_PATTERN,
            command.strip(),
        )
    )
```

<details>

<summary>Explicação Passo a Passo (Step-by-Step)</summary>

<br/>

Vamos começar entendendo o regex abaixo:

```python
r"^\/(gas|agua)$"
```

 - `^ -> início da string`
   - ✅ Aceita = `/gas`
   - ❌ Não aceita = `abc /gas` (porque existe texto antes do comando)
 - `\/ -> caractere "/"`
   - Representa literalmente: `/ (barra)`
   - Significa: A correspondência deve ser um caractere "/"
 - `(gas|agua) -> palavra "gas" OU "agua"`
   - Significa: Aceite `"gas"` OU `"agua"`.
   - O operador `|` funciona como um `OR`.
 - `$ -> fim da string`

Continuando, vamos entender o `re.match()` que recebeu como parâmetro:

> **NOTE:**  
> A função `re.match()` serve para verificar se um texto corresponde a um padrão Regex.

 - `REQUEST_COMMAND_PATTERN`
   - Padrão Regex que será utilizado na função `re.match()`.
 - `command.strip()`
   - Formata a string removendo espaços do início e do fim da string.
   - Suponha que o usuário enviou:
     - `"   /gas   "`
   - O método `command.strip()` remove espaços do início e do fim da string.
     - `"/gas"`

> **E o retorno da função `re.match()`?**

 - `True`
   - Se o comando for válido -> a função `re.match()` retorna `True`.
 - `False`
   - Se o comando for inválido, a função `re.match()` retorna `False`

> **NOTE:**  
> Como o retorno da função é do tipo `bool`, vamos retornar `True` ou `False` com a função  `validate_request_command()`.

</details>

---

**Rodrigo** **L**eite da **S**ilva - **rodrigols89**
