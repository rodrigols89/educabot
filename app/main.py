# app/main.py

"""
Resumo do módulo:
Inicializa a aplicação FastAPI e registra os endpoints da API.

Descrição estendida:
Este módulo representa o ponto de entrada da aplicação. Ele é
responsável por criar a instância principal do FastAPI e
registrar todos os roteadores utilizados pelo sistema.

Atualmente, são registrados os endpoints de verificação de
saúde da aplicação e de recebimento de webhooks da Evolution
API.

Responsabilidades principais:
- Inicializar a aplicação FastAPI
- Configurar informações da API
- Registrar os roteadores da aplicação

Componentes principais:
- app

Dependências:
- fastapi.FastAPI
- app.api.health
- app.api.webhook

Efeitos colaterais:
- Cria a instância principal da aplicação
- Registra os endpoints disponíveis

Entrada/Saída:
- Entrada: requisições HTTP recebidas pelo servidor ASGI
- Saída: respostas HTTP produzidas pelos roteadores

Estratégia de tratamento de erros:
- Não realiza tratamento explícito de exceções
- Depende do tratamento padrão do FastAPI

Considerações de performance:
- A inicialização ocorre apenas durante o carregamento da
  aplicação
- O registro dos roteadores possui custo desprezível

Notas de concorrência:
- A instância do FastAPI é compartilhada entre as requisições
- O gerenciamento de concorrência é realizado pelo servidor
  ASGI utilizado

Exemplo de uso:
uvicorn app.main:app --reload

Limitações:
- Apenas registra os componentes da aplicação
- Não implementa regras de negócio

Versão/manutenção:
- Novos endpoints devem ser registrados neste módulo por meio
  de include_router().
"""

from fastapi import FastAPI

from app.api.health import router as health_check
from app.api.webhook import router as webhook_router

app = FastAPI(
    title="EducatBot - WhatsApp Orders API",
    version="1.0.0",
)

app.include_router(health_check)
app.include_router(webhook_router)
