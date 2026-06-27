# app/api/health.py

"""
Resumo do módulo:
Define o endpoint de verificação de saúde da aplicação.

Descrição estendida:
Este módulo disponibiliza um endpoint utilizado para verificar
se a API está em funcionamento e apta a receber requisições.

O endpoint pode ser utilizado por ferramentas de
monitoramento, balanceadores de carga, orquestradores e
processos de verificação de disponibilidade.

Responsabilidades principais:
- Expor o endpoint de verificação de saúde
- Informar o estado operacional da aplicação

Componentes principais:
- router
- health_check

Dependências:
- fastapi.APIRouter

Efeitos colaterais:
- Nenhum

Entrada/Saída:
- Entrada: requisição HTTP GET
- Saída: resposta JSON indicando o estado da aplicação

Estratégia de tratamento de erros:
- Não realiza tratamento explícito de erros
- Depende do tratamento padrão do FastAPI

Considerações de performance:
- Endpoint extremamente leve
- Não realiza acesso ao banco de dados
- Não consulta serviços externos

Notas de concorrência:
- Não mantém estado compartilhado
- Seguro para execução concorrente

Exemplo de uso:
GET /health

Resposta:
{
    "status": "ok"
}

Limitações:
- Verifica apenas se a aplicação está em execução
- Não valida dependências externas

Versão/manutenção:
- Novas verificações de saúde podem ser adicionadas conforme
  a evolução da aplicação.
"""

from fastapi import APIRouter

router = APIRouter(
    tags=["Healthcheck"],
)


@router.get("/health")
def health_check():
    """
    Retorna o estado de funcionamento da aplicação.

    Returns:
        dict[str, str]:
            Dicionário contendo o status atual da aplicação.

    Raises:
        Nenhuma exceção é gerada diretamente pela função.

    Observações:
        Este endpoint pode ser utilizado por sistemas de
        monitoramento para verificar a disponibilidade da API.

    Efeitos colaterais:
        Nenhum.

    Exemplos:
        GET /health

        Resposta:
        {
            "status": "ok"
        }

        if response.json()["status"] == "ok":
            print("API disponível")

    Avisos:
        O retorno indica apenas que a aplicação está em
        execução.

    Limitações:
        Não verifica conexões com banco de dados, Redis ou
        outros serviços externos.
    """

    return {"status": "ok"}
