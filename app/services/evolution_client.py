# ruff: noqa: PLW0717
# app/services/evolution_service.py

"""
Resumo do módulo:
Fornece integração com a Evolution API para envio de mensagens
via WhatsApp.

Descrição estendida:
Este módulo contém a lógica responsável por enviar mensagens
de texto para números de telefone utilizando a Evolution API.

A comunicação é realizada via requisição HTTP POST, com
autenticação baseada em chave de API e configuração definida
nas variáveis de ambiente.

Responsabilidades principais:
- Construir requisições para a Evolution API
- Enviar mensagens via WhatsApp
- Tratar respostas da API
- Registrar logs de requisição e resposta
- Tratar falhas de comunicação

Componentes principais:
- send_whatsapp_message

Dependências:
- requests
- app.core.config.settings

Efeitos colaterais:
- Realiza requisições HTTP externas
- Escreve logs de requisição e resposta na saída padrão

Entrada/Saída:
- Entrada: telefone e mensagem de texto
- Saída: booleano indicando sucesso ou falha do envio

Estratégia de tratamento de erros:
- Captura exceções genéricas durante a requisição HTTP
- Retorna False em caso de falha
- Evita propagação de erros externos

Considerações de performance:
- Requisições HTTP síncronas com timeout fixo de 30s
- Pode impactar performance em alto volume de envios

Notas de concorrência:
- Seguro para uso concorrente em múltiplas chamadas
- Dependente da estabilidade da API externa

Exemplo de uso:
success = send_whatsapp_message(
    phone="83999999999",
    message="Olá!"
)

Limitações:
- Não implementa retry automático
- Não valida formato do telefone
- Depende da disponibilidade da Evolution API

Versão/manutenção:
- Mudanças na API externa podem exigir atualização deste
  módulo
"""

import requests

from app.core.config import settings


def send_whatsapp_message(
    phone: str,
    message: str,
) -> bool:
    """
    Envia uma mensagem de texto via WhatsApp utilizando a
    Evolution API.

    Args:
        phone (str):
            Número de telefone do destinatário.

        message (str):
            Conteúdo textual da mensagem a ser enviada.

    Returns:
        bool:
            True se a mensagem foi enviada com sucesso (HTTP
            200 ou 201).

            False caso ocorra falha na requisição ou resposta
            inválida.

    Raises:
        Nenhuma exceção é propagada diretamente pela função.

    Observações:
        A URL da requisição é construída dinamicamente a partir
        das configurações do sistema (settings).

        A autenticação é realizada via header "apikey".

    Efeitos colaterais:
        - Realiza requisição HTTP externa.
        - Escreve logs detalhados de requisição e resposta.
        - Pode gerar logs de erro em caso de exceção.

    Exemplos:
        success = send_whatsapp_message(
            phone="83999999999",
            message="Olá!"
        )

        if success:
            print("Mensagem enviada")

        send_whatsapp_message(
            phone="00000000000",
            message="Teste"
        )

    Avisos:
        A função depende de serviço externo (Evolution API).

    Limitações:
        Não possui retry automático.
        Não valida o formato do telefone.
        Não garante entrega da mensagem, apenas envio HTTP.
    """

    url = (
        f"{settings.EVOLUTION_API_URL}"
        f"/message/sendText/"
        f"{settings.EVOLUTION_INSTANCE}"
    )

    payload = {
        "number": phone,
        "text": message,
    }

    headers = {
        "apikey": settings.AUTHENTICATION_API_KEY,
        "Content-Type": "application/json",
    }

    print("\nEVOLUTION REQUEST:")
    print(f"URL: {url}")
    print(f"PHONE: {phone}")
    print(f"PAYLOAD: {payload}")

    try:

        response = requests.post(
            url=url,
            json=payload,
            headers=headers,
            timeout=30,
        )

        print("\nEVOLUTION RESPONSE:")
        print(f"STATUS: {response.status_code}")
        print(f"BODY: {response.text}")

        return response.status_code in {
            200,
            201,
        }

    except Exception as error:

        print("\nEVOLUTION ERROR:")
        print(error)

        return False
