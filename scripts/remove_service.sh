#!/usr/bin/env bash
set -e

# scripts/remove_service.sh

SERVICE_NAME="educabot"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"

echo "🗑️ Removing EducaBot systemd service..."
echo "============================================================================================"

# ============================================================================
# STOP SERVICE
# ============================================================================

echo "🛑 Stopping service..."

sudo systemctl stop "${SERVICE_NAME}.service" || true

echo "✅ Service stopped."

echo "============================================================================================"

# ============================================================================
# DISABLE SERVICE
# ============================================================================

echo "⚙️ Disabling service..."

sudo systemctl disable "${SERVICE_NAME}.service" || true

echo "✅ Service disabled."

echo "============================================================================================"

# ============================================================================
# REMOVE SERVICE FILE
# ============================================================================

echo "🗑️ Removing service file..."

sudo rm -f "$SERVICE_FILE"

echo "✅ Service file removed."

echo "============================================================================================"

# ============================================================================
# RELOAD SYSTEMD
# ============================================================================

echo "🔄 Reloading systemd..."

sudo systemctl daemon-reload
sudo systemctl daemon-reexec

echo "✅ Systemd reloaded."

echo ""
echo "🎉 EducaBot service removed successfully!"
echo ""
