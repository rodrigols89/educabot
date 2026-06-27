#!/usr/bin/env bash
set -e

# ============================================================================
# Função de separador visual
# ============================================================================
print_separator() {
    echo ""
    echo "============================================================================================"
    echo ""
}





# ============================================================================
# Diretório raiz do projeto
# ============================================================================
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"





# ============================================================================
# Ambiente virtual
# ============================================================================
VENV_DIR="$PROJECT_ROOT/.venv"
VENV_PYTHON="$VENV_DIR/bin/python"
VENV_PIP="$VENV_DIR/bin/pip"
VENV_ALEMBIC="$VENV_DIR/bin/alembic"

cd "$PROJECT_ROOT"





# ============================================================================
# Carrega .env (IMPORTANTE para DATABASE_URL e configs)
# ============================================================================
if [ -f ".env" ]; then
    set -a
    source .env
    set +a
fi

echo "  🚀  Initializing EducaBot..."
print_separator





# ============================================================================
# Atualização do sistema
# ============================================================================
echo "  📦  Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y
echo "  ✅  System updated"
print_separator





# ============================================================================
# Python dependencies
# ============================================================================
echo "  🐍  Checking Python dependencies..."

if ! command -v python3 >/dev/null 2>&1; then
    sudo apt-get install -y python3
fi

if ! command -v pip3 >/dev/null 2>&1; then
    sudo apt-get install -y python3-pip
fi

if ! dpkg -s python3-venv >/dev/null 2>&1; then
    sudo apt-get install -y python3-venv
fi

echo "  ✅  Python ready"
print_separator





# ============================================================================
# Virtualenv
# ============================================================================
echo "  🐍  Checking virtual environment..."

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "  ✅  Virtualenv created"
else
    echo "  ✅  Virtualenv already exists"
fi

print_separator





# ============================================================================
# Pip setup
# ============================================================================
echo "  🛠️  Ensuring pip..."

"$VENV_PYTHON" -m ensurepip --upgrade
"$VENV_PYTHON" -m pip install --upgrade pip

echo "  ✅  pip ready"
print_separator





# ============================================================================
# Dependencies
# ============================================================================
if [ -f "requirements.txt" ]; then
    echo "  📥  Installing dependencies..."
    "$VENV_PIP" install -U -r requirements.txt
    echo "  ✅  dependencies installed"
else
    echo "  ⚠️  requirements.txt not found"
fi

print_separator





# ============================================================================
# Docker startup
# ============================================================================
echo "  🐳  Starting Docker containers..."

docker compose up -d

echo "  ✅  Containers started"
print_separator





# ============================================================================
# Waiting PostgreSQL (CRÍTICO)
# ============================================================================
echo "  ⏳  Waiting PostgreSQL..."

until docker compose exec -T postgres pg_isready -U postgres -d postgres >/dev/null 2>&1
do
    sleep 1
done

# garante execução do init.sql
sleep 3

echo "  ✅  PostgreSQL ready"
print_separator





# ============================================================================
# Migrations
# ============================================================================
echo "  🔄  Running migrations..."

export DATABASE_URL="$DATABASE_URL"

"$VENV_ALEMBIC" upgrade head

echo "  ✅  Migrations completed"
print_separator





# ============================================================================
# Finalização
# ============================================================================
echo ""
echo "🎉 EducaBot initialized successfully!"
echo ""
echo "👉 Run server:"
echo "   make server"
echo ""
