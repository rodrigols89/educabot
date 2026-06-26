# app/utils/evolution_parser.py

"""
Resumo do módulo:
Fornece utilitários para extração de informações de mensagens
recebidas pela Evolution API.

Descrição estendida:
Este módulo contém funções responsáveis por interpretar a
estrutura dos payloads enviados pela Evolution API e extrair
informações relevantes para processamento da aplicação.

O parser identifica o remetente da mensagem, extrai o conteúdo
textual e trata de forma diferente mensagens enviadas pelo
próprio sistema e mensagens recebidas de usuários.

Responsabilidades principais:
- Interpretar payloads da Evolution API
- Extrair telefone do remetente
- Extrair conteúdo textual da mensagem
- Diferenciar mensagens enviadas e recebidas
- Gerar logs de depuração do processamento

Componentes principais:
- parse_evolution_message

Dependências:
- typing.Any
- app.utils.logger.print_separator

Efeitos colaterais:
- Escreve logs de depuração na saída padrão

Entrada/Saída:
- Entrada: payload recebido da Evolution API
- Saída: telefone e conteúdo textual da mensagem

Estratégia de tratamento de erros:
- Utiliza valores padrão durante acesso ao payload
- Evita exceções de chaves inexistentes por meio de get()

Considerações de performance:
- Executa apenas operações simples de leitura em dicionários
- Não realiza acesso a banco de dados ou serviços externos

Notas de concorrência:
- Não mantém estado compartilhado
- Seguro para execução concorrente
- Logs podem ser intercalados em execuções simultâneas

Exemplo de uso:
phone, text = parse_evolution_message(payload)

if phone and text:
    process_message(phone, text)

Limitações:
- Processa apenas mensagens armazenadas em "conversation"
- Depende da estrutura específica da Evolution API
- Não interpreta mensagens multimídia

Versão/manutenção:
- Novos formatos de payload podem exigir atualização do parser
"""

from typing import Any


def parse_evolution_message(
    payload: dict[str, Any],
) -> tuple[str | None, str | None]:
    """
    Extrai telefone e conteúdo textual de uma mensagem da
    Evolution API.

    Args:
        payload (dict[str, Any]):
            Estrutura completa recebida da Evolution API.

    Returns:
        tuple[str | None, str | None]:
            Tupla contendo:

            - Telefone do remetente.
            - Conteúdo textual da mensagem.

            Tanto mensagens recebidas quanto mensagens enviadas
            pelo sistema retornam telefone e texto quando
            disponíveis.

    Raises:
        Nenhuma exceção é gerada diretamente pela função.

    Observações:
        A origem do telefone varia conforme o tipo da mensagem:

        - Mensagens recebidas utilizam o campo "senderPn".
        - Mensagens enviadas utilizam o campo "sender".

        Campos ausentes são substituídos por valores padrão.

    Efeitos colaterais:
        - Escreve logs de depuração na saída padrão.
        - Exibe informações sobre o processamento da mensagem.

    Exemplos:
        phone, text = parse_evolution_message(payload)

        print(phone)
        print(text)

        phone, text = parse_evolution_message(payload)

        if phone:
            process_message(phone, text)

        phone, text = parse_evolution_message(payload)

        if text == "/gas":
            execute_command(text)

    Avisos:
        A função assume que o payload segue o formato esperado
        pela Evolution API.

    Limitações:
        Processa apenas conteúdo textual presente no campo
        "conversation".
    """

    print("EVOLUTION PARSER PROCESS:")

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

        phone: str = payload.get(
            "sender",
            "",
        ).replace(
            "@s.whatsapp.net",
            "",
        )

        print("fromMe (True)")
        print(f"Phone: {phone}")
        print(f"Text: {text}")

        return phone, text

    phone: str = key.get(
        "senderPn",
        "",
    ).replace(
        "@s.whatsapp.net",
        "",
    )

    print("fromMe (False)")
    print(f"Phone: {phone}")
    print(f"Text: {text}")

    return phone, text
