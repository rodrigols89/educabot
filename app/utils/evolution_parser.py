# app/utils/evolution_parser.py

"""
Resumo do módulo:
Fornece utilitários para extração de informações de mensagens
recebidas pela Evolution API.

Descrição estendida:
Este módulo contém funções responsáveis por interpretar a
estrutura de payloads enviados pela Evolution API e extrair
informações relevantes para processamento da aplicação.

Atualmente, o módulo permite identificar se a mensagem foi
enviada pelo próprio sistema, além de recuperar telefone e
conteúdo textual da mensagem recebida.

Responsabilidades principais:
- Interpretar payloads da Evolution API
- Extrair telefone do remetente
- Extrair conteúdo textual da mensagem
- Ignorar mensagens enviadas pelo próprio sistema
- Gerar logs de depuração durante o processamento

Componentes principais:
- parse_evolution_message

Dependências:
- typing.Any

Efeitos colaterais:
- Escreve informações de depuração na saída padrão

Entrada/Saída:
- Entrada: payload recebido da Evolution API
- Saída: telefone e conteúdo da mensagem processada

Estratégia de tratamento de erros:
- Utiliza valores padrão durante acesso ao payload
- Evita exceções de chave inexistente por meio de get()

Considerações de performance:
- Operações de acesso a dicionários possuem custo baixo
- Não realiza processamento intensivo de dados

Notas de concorrência:
- Não mantém estado compartilhado
- Seguro para execução concorrente
- A saída de logs pode ser intercalada em múltiplas threads

Exemplo de uso:
phone, text = parse_evolution_message(payload)

if phone and text:
    process_message(phone, text)

Limitações:
- Processa apenas mensagens do tipo conversation
- Não interpreta mídias ou mensagens estruturadas
- Depende do formato específico da Evolution API

Versão/manutenção:
- Novos tipos de mensagem exigirão atualização do parser
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
            Tupla contendo telefone e texto da mensagem.

            Retorna:
            - (telefone, texto) para mensagens recebidas.
            - (None, None) para mensagens enviadas pelo sistema.

    Raises:
        Nenhuma exceção é gerada diretamente pela função.

    Observações:
        A função utiliza valores padrão durante a navegação no
        payload para evitar falhas quando campos estiverem
        ausentes.

    Efeitos colaterais:
        - Escreve logs de depuração na saída padrão.
        - Exibe informações sobre o processamento da mensagem.

    Exemplos:
        phone, text = parse_evolution_message(payload)

        if phone:
            print(phone)

        phone, text = parse_evolution_message(payload)

        if text:
            print(text)

        phone, text = parse_evolution_message(payload)

        if phone is None:
            print("Mensagem ignorada")

    Avisos:
        Mensagens enviadas pelo próprio sistema são ignoradas.

    Limitações:
        Processa apenas mensagens armazenadas no campo
        "conversation".
    """

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
