# app/core/config.py

"""
Resumo do módulo:
Centraliza o carregamento e a disponibilização das configurações
da aplicação.

Descrição estendida:
Este módulo carrega as variáveis de ambiente utilizando
python-dotenv e disponibiliza uma instância única da classe
Settings para acesso às configurações da aplicação.

As configurações abrangem conexão com banco de dados, Redis,
Evolution API, fornecedores e demais parâmetros utilizados
pelos serviços da aplicação.

Responsabilidades principais:
- Carregar variáveis de ambiente
- Centralizar configurações da aplicação
- Disponibilizar uma instância compartilhada de Settings
- Converter variáveis para tipos apropriados quando necessário

Componentes principais:
- Settings
- settings

Dependências:
- os
- dotenv.load_dotenv

Efeitos colaterais:
- Carrega variáveis do arquivo .env durante a importação do
  módulo

Entrada/Saída:
- Entrada: variáveis de ambiente do sistema e do arquivo .env
- Saída: configuração centralizada da aplicação

Estratégia de tratamento de erros:
- Utiliza valores padrão quando uma variável não está definida
- Não realiza validações de consistência das configurações

Considerações de performance:
- As configurações são carregadas apenas durante a importação
  do módulo
- O acesso aos atributos ocorre em memória

Notas de concorrência:
- A instância compartilhada é utilizada apenas para leitura
- Seguro para uso concorrente desde que as configurações não
  sejam modificadas em tempo de execução

Exemplo de uso:
api_url = settings.EVOLUTION_API_URL

database = settings.DATABASE_URL

Limitações:
- Não valida formatos de URLs ou telefones
- Não verifica ausência de configurações obrigatórias

Versão/manutenção:
- Novas configurações devem ser adicionadas à classe Settings
- Alterações exigem atualização do arquivo .env
"""

import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """
    Resumo da classe:
    Armazena as configurações globais da aplicação.

    Propósito:
    Centralizar o acesso às variáveis de ambiente utilizadas
    pelos diferentes componentes do sistema.

    Atributos:
        DATABASE_URL (str):
            URL de conexão com o banco de dados.

        CONFIG_SESSION_PHONE_VERSION (str):
            Configuração da versão da sessão telefônica.

        AUTHENTICATION_API_KEY (str):
            Chave utilizada para autenticação na Evolution API.

        DATABASE_PROVIDER (str):
            Provedor do banco de dados.

        DATABASE_CONNECTION_URI (str):
            URI de conexão com o banco de dados.

        CACHE_REDIS_URI (str):
            URI de conexão com o Redis.

        CACHE_REDIS_PREFIX_KEY (str):
            Prefixo utilizado nas chaves do Redis.

        EVOLUTION_API_URL (str):
            URL base da Evolution API.

        EVOLUTION_INSTANCE (str):
            Nome da instância da Evolution API.

        SUPPLIER_GAS_NAME (str):
            Nome do fornecedor de gás.

        SUPPLIER_GAS_PHONE (str):
            Telefone do fornecedor de gás.

        SUPPLIER_WATER_NAME (str):
            Nome do fornecedor de água.

        SUPPLIER_WATER_PHONE (str):
            Telefone do fornecedor de água.

        SUPPLIER_SECRETARIAT_WATER_NAME (str):
            Nome do fornecedor da secretaria.

        SUPPLIER_SECRETARIAT_WATER_PHONE (str):
            Telefone do fornecedor da secretaria.

    Visão geral dos métodos:
        Não possui métodos próprios.
        Atua como um objeto de configuração.

    Observações:
        Os valores são carregados durante a criação da
        instância da classe.

    Exemplo de uso:
        api_url = settings.EVOLUTION_API_URL

        redis_uri = settings.CACHE_REDIS_URI

    Notas sobre concorrência:
        A classe é utilizada apenas para leitura e pode ser
        compartilhada entre múltiplas threads.

    Considerações de design:
        Centraliza todas as configurações da aplicação em um
        único objeto, facilitando manutenção e reutilização.
    """

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "",
    )

    CONFIG_SESSION_PHONE_VERSION: str = os.getenv(
        "CONFIG_SESSION_PHONE_VERSION",
        "",
    )

    AUTHENTICATION_API_KEY: str = os.getenv(
        "AUTHENTICATION_API_KEY",
        "",
    )

    DATABASE_PROVIDER: str = os.getenv(
        "DATABASE_PROVIDER",
        "",
    )

    DATABASE_CONNECTION_URI: str = os.getenv(
        "DATABASE_CONNECTION_URI",
        "",
    )

    CACHE_REDIS_URI: str = os.getenv(
        "CACHE_REDIS_URI",
        "",
    )

    CACHE_REDIS_PREFIX_KEY: str = os.getenv(
        "CACHE_REDIS_PREFIX_KEY",
        "",
    )

    EVOLUTION_API_URL: str = os.getenv(
        "EVOLUTION_API_URL",
        "http://localhost:8080",
    )

    EVOLUTION_INSTANCE: str = os.getenv(
        "EVOLUTION_INSTANCE",
        "",
    )

    SUPPLIER_GAS_NAME: str = os.getenv(
        "SUPPLIER_GAS_NAME",
        "",
    )

    SUPPLIER_GAS_PHONE: str = os.getenv(
        "SUPPLIER_GAS_PHONE",
        "",
    )

    SUPPLIER_WATER_NAME: str = os.getenv(
        "SUPPLIER_WATER_NAME",
        "",
    )

    SUPPLIER_WATER_PHONE: str = os.getenv(
        "SUPPLIER_WATER_PHONE",
        "",
    )

    SUPPLIER_SECRETARIAT_WATER_NAME: str = os.getenv(
        "SUPPLIER_SECRETARIAT_WATER_NAME",
        "",
    )

    SUPPLIER_SECRETARIAT_WATER_PHONE: str = os.getenv(
        "SUPPLIER_SECRETARIAT_WATER_PHONE",
        "",
    )


settings = Settings()
