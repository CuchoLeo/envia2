#!/bin/bash
# Script de instalación y verificación del Sistema de Seguimiento de OC

set -e  # Salir si hay error

echo "🚀 Instalando Sistema de Seguimiento de OC..."
echo "================================================"

# Verificar Python
echo "📌 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Python $PYTHON_VERSION encontrado"

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "📦 Creando entorno virtual..."
    python3 -m venv venv
    echo "✅ Entorno virtual creado"
fi

# Activar entorno virtual
echo "🔄 Activando entorno virtual..."
source venv/bin/activate

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip setuptools wheel --quiet

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt --quiet

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p logs static oc_files

# Copiar .env.example si no existe .env
if [ ! -f ".env" ]; then
    echo "📋 Creando archivo .env desde plantilla..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita el archivo .env con tus credenciales"
else
    echo "✅ Archivo .env ya existe"
fi

# Verificar configuración
echo ""
echo "🔍 Verificando configuración..."
python config.py

echo ""
echo "================================================"
echo "✅ Instalación completada exitosamente"
echo ""
echo "📝 Próximos pasos:"
echo "   1. Edita el archivo .env con tus credenciales"
echo "   2. Ejecuta: python app.py"
echo "   3. Abre: http://localhost:8001"
echo ""
echo "📚 Ver README.md para más información"
