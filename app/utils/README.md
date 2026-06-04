# `🔧 utils/`

> O diretório `🔧 utils/` é responsável por *"guardar coisas que podem ser usadas em vários lugares"*.

Por, exemplo:

 - Formatar telefone
 - Validar CPF
 - Gerar UUID

## Conteúdo

 - [`regex.py`](#regex-py)
<!---
[WHITESPACE RULES]
- "20" Whitespace character.
--->




















---

<div id="regex-py"></div>

## `regex.py`

> O arquivo `regex.py` concentra **expressões regulares (Regex)** utilizadas pela aplicação para validação e extração de informações em textos.

 - Centralizar essas regras em um único local evita duplicação de código, facilita a manutenção e garante que todas as partes do sistema utilizem os mesmos padrões de validação.





---

<div id="validate-request-command"></div>

## `validate_request_command`

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
