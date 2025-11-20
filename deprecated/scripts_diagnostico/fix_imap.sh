#!/bin/bash
# Script para corregir el error de IMAP

echo "🔧 Corrigiendo error de IMAP..."
echo "================================"

# Activar entorno virtual si existe
if [ -d "venv" ]; then
    echo "📦 Activando entorno virtual..."
    source venv/bin/activate
fi

# Desinstalar versión vieja
echo "🗑️  Desinstalando IMAPClient antiguo..."
pip uninstall -y imapclient

# Instalar versión nueva
echo "📥 Instalando IMAPClient 3.0.1..."
pip install imapclient==3.0.1

# Reinstalar dependencias por si acaso
echo "🔄 Reinstalando todas las dependencias..."
pip install -r requirements.txt

echo ""
echo "✅ Corrección completada!"
echo ""
echo "🧪 Probando conexión IMAP..."
python test_imap.py
