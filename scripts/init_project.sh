#!/usr/bin/env bash
set -e

# ============================================================================
# Função para exibir separadores visuais no terminal
#
# Utilizada para melhorar a leitura da saída do script.
# ============================================================================

print_separator() {
    echo ""
    echo "============================================================================================"
    echo ""
}



# ============================================================================
# Diretório raiz do projeto
#
# Descobre automaticamente o diretório principal do projeto,
# independentemente de onde o script for executado.
#
# Exemplo:
# /home/user/educabot
# ============================================================================

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"



# ============================================================================
# Caminho do ambiente virtual
#
# Define onde o ambiente virtual Python deve existir.
#
# Exemplo:
# /home/user/educabot/.venv
# ============================================================================

VENV_DIR="$PROJECT_ROOT/.venv"



# ============================================================================
# Executáveis do ambiente virtual
#
# Cria atalhos para utilizar o Python e o Pip do ambiente virtual,
# garantindo que todos os comandos sejam executados isoladamente
# do sistema operacional.
# ============================================================================

VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"
VENV_ALEMBIC="$VENV_DIR/bin/alembic"



# ============================================================================
# Navegação para a raiz do projeto
#
# Garante que todos os comandos posteriores sejam executados a partir
# do diretório principal da aplicação.
# ============================================================================

cd "$PROJECT_ROOT"



# ============================================================================
# Carregamento das variáveis de ambiente
#
# Se existir um arquivo .env na raiz do projeto, suas variáveis serão
# carregadas para o ambiente atual do shell.
#
# Isso permite que DATABASE_URL, SECRET_KEY e outras configurações
# estejam disponíveis para o Alembic e para a aplicação.
# ============================================================================

if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi



echo "  🚀  Initializing the project..."

print_separator





# ============================================================================
# Atualização do sistema operacional
#
# Esta etapa atualiza a lista de pacotes disponíveis e instala as versões
# mais recentes dos pacotes já instalados no servidor.
#
# Objetivo:
# - Garantir correções de segurança.
# - Atualizar dependências do sistema.
# - Evitar problemas com pacotes desatualizados.
# ============================================================================

echo "  📦  Updating system packages..."

sudo apt-get update
sudo apt-get upgrade -y

echo "  ✅  System packages updated."

print_separator





# ============================================================================
# Verificação das dependências do Python
#
# Confirma que Python, Pip e o módulo de ambientes virtuais estão
# instalados no sistema.
#
# Caso algum deles não exista, o script realiza a instalação
# automaticamente.
# ============================================================================

echo "  🐍  Checking Python dependencies (Python3 + pip)..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "  📦  Installing python3..."
    sudo apt-get install -y python3
    echo "  ✅  Python3 installed."
fi

if ! command -v pip3 >/dev/null 2>&1; then
    echo "  📦  Installing python3-pip..."
    sudo apt-get install -y python3-pip
    echo "  ✅  Python3-pip installed."
fi

if ! dpkg -s python3-venv >/dev/null 2>&1; then
    echo "  📦  Installing python3-venv..."
    sudo apt-get install -y python3-venv
    echo "  ✅  Python3-venv installed."
fi

echo "  ✅  Python dependencies (Python3 + pip) ready."

print_separator





# ============================================================================
# Criação ou reutilização do ambiente virtual
#
# Verifica se o ambiente virtual já existe.
#
# Caso não exista:
# - cria um novo ambiente virtual Python.
#
# Caso exista:
# - reutiliza o ambiente já criado.
#
# O ambiente virtual permite instalar dependências do projeto sem
# afetar o Python global do sistema operacional.
# ============================================================================

echo "  🐍  Checking virtual environment..."

if [ ! -d "$VENV_DIR" ]; then
    echo "  📦  Virtual environment not found. Creating..."

    python3 -m venv "$VENV_DIR"

    echo "  ✅  Virtual environment created."
else
    echo "  ✅  Virtual environment already exists."
fi

print_separator





# ============================================================================
# Garantia de funcionamento do Pip
#
# Algumas distribuições Linux criam ambientes virtuais sem instalar
# automaticamente o Pip.
#
# O comando ensurepip garante que o gerenciador de pacotes esteja
# disponível dentro do ambiente virtual.
# ============================================================================

echo "  🛠️  Ensuring pip exists inside virtual environment..."

"$VENV_PYTHON" -m ensurepip --upgrade

echo "  ✅  Pip available inside virtual environment."

print_separator





# ============================================================================
# Atualização do Pip
#
# Instala a versão mais recente do gerenciador de pacotes Python.
#
# Benefícios:
# - Melhor compatibilidade.
# - Correções de bugs.
# - Melhor suporte a dependências modernas.
# ============================================================================

echo "  ⬆️  Upgrading pip..."

"$VENV_PYTHON" -m pip install --upgrade pip

echo "  ✅  Pip upgraded."

print_separator





# ============================================================================
# Instalação das dependências do projeto
#
# Caso exista um arquivo requirements.txt, todas as dependências
# necessárias para a aplicação serão instaladas ou atualizadas.
#
# Exemplos:
# - FastAPI
# - SQLAlchemy
# - Alembic
# - Pytest
# - Uvicorn
# ============================================================================

if [ -f "requirements.txt" ]; then
    echo "  📥  Installing dependencies..."

    "$VENV_PIP" install -U -v -r requirements.txt

    echo "  ✅  Dependencies installed."
else
    echo "  ⚠️  requirements.txt not found. Skipping dependency installation."
fi

print_separator





# ============================================================================
# Inicialização dos containers Docker
#
# Inicia todos os serviços definidos no docker-compose.yml
# em modo background.
#
# Serviços esperados:
# - PostgreSQL
# - Redis (caso utilizado)
# - Evolution API
#
# O parâmetro -d faz com que os containers sejam executados
# em segundo plano sem bloquear a execução do script.
#
# Equivalente a:
#
# docker compose up -d
# ============================================================================

echo "  🐳  Starting Docker containers..."

docker compose up -d

echo "  ✅  Containers started."

print_separator





# ============================================================================
# Aguarda PostgreSQL ficar disponível
#
# Após subir os containers, o banco pode levar alguns segundos para
# aceitar conexões.
#
# O loop abaixo somente continua quando o PostgreSQL estiver pronto.
# ============================================================================

echo "  ⏳  Waiting for PostgreSQL..."

until docker compose exec -T postgres pg_isready -U "$POSTGRES_USER" >/dev/null 2>&1
do
    sleep 1
done

echo "  ✅  PostgreSQL is ready."

print_separator
