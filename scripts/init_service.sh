#!/usr/bin/env bash
set -e


# ============================================================================
# Root directory
# ============================================================================

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"


# ============================================================================
# Variables
# ============================================================================

SERVICE_NAME="educabot"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

APP_MODULE="app.main:app"
HOST="0.0.0.0"
PORT="8001"

VENV_UVICORN="$PROJECT_ROOT/.venv/bin/uvicorn"


# ============================================================================
# Start
# ============================================================================

echo "  🚀  Initializing systemd service..."


# ============================================================================
# Verify uvicorn exists
# ============================================================================

if [ ! -f "$VENV_UVICORN" ]; then
    echo "  ❌  Uvicorn not found:"
    echo "  $VENV_UVICORN"
    exit 1
fi

echo "============================================================================================"


# ============================================================================
# Create service file
# ============================================================================

echo "  📝  Creating service file..."

sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=EducaBot
After=network.target

[Service]
Type=simple
WorkingDirectory=$PROJECT_ROOT

ExecStart=$VENV_UVICORN $APP_MODULE --host $HOST --port $PORT

Restart=always
RestartSec=5

User=$(whoami)

[Install]
WantedBy=multi-user.target
EOF

echo "  ✅  Service file created."

echo "============================================================================================"


# ============================================================================
# Reload systemd
# ============================================================================

echo "  🔄  Reloading systemd..."

sudo systemctl daemon-reexec
sudo systemctl daemon-reload

echo "  ✅  Systemd reloaded."

echo "============================================================================================"


# ============================================================================
# Enable service
# ============================================================================

echo "  ⚙️  Enabling service..."

sudo systemctl enable "${SERVICE_NAME}.service"

echo "  ✅  Service enabled."

echo "============================================================================================"


# ============================================================================
# Restart service
# ============================================================================

echo "  🚀  Starting service..."

sudo systemctl restart "${SERVICE_NAME}.service"

echo "  ✅  Service started."

echo "============================================================================================"


# ============================================================================
# Show status
# ============================================================================

echo ""
echo "  📊  Service status:"
echo ""

sudo systemctl status "${SERVICE_NAME}.service" --no-pager

echo "============================================================================================"


echo ""
echo "  🎉  Service initialization complete!"
echo ""
echo "Useful commands:"
echo ""
echo "  sudo systemctl restart ${SERVICE_NAME}"
echo "  sudo systemctl stop ${SERVICE_NAME}"
echo "  sudo systemctl status ${SERVICE_NAME}"
echo "  sudo journalctl -u ${SERVICE_NAME} -f"
echo ""
