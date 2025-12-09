#!/bin/bash
#
# run_script.sh - Wrapper para ejecutar scripts del proyecto
#
# Configura automáticamente PYTHONPATH y ejecuta el script solicitado
#
# Uso:
#   ./run_script.sh scripts/database/limpiar_base_datos.py
#   ./run_script.sh scripts/testing/check_inbox.py --help
#

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Banner
echo ""
echo "============================================"
echo "  🚀 Script Runner - Sistema OC"
echo "============================================"
echo ""

# Verificar que se proporcionó un script
if [ $# -eq 0 ]; then
    echo -e "${RED}❌ Error: Debes especificar un script para ejecutar${NC}"
    echo ""
    echo "Uso: ./run_script.sh <ruta_al_script> [argumentos]"
    echo ""
    echo "Ejemplos:"
    echo "  ./run_script.sh scripts/database/limpiar_base_datos.py"
    echo "  ./run_script.sh scripts/database/limpiar_base_datos.py --stats"
    echo "  ./run_script.sh scripts/testing/check_inbox.py"
    echo ""
    exit 1
fi

SCRIPT_PATH="$1"
shift  # Remover el primer argumento, el resto son args del script

# Verificar que el script existe
if [ ! -f "$SCRIPT_PATH" ]; then
    echo -e "${RED}❌ Error: El script '$SCRIPT_PATH' no existe${NC}"
    echo ""
    echo "Verifica la ruta del script. Debe ser relativa a la raíz del proyecto."
    echo ""
    exit 1
fi

# Verificar que estamos en la raíz del proyecto
if [ ! -f "database.py" ] || [ ! -d "src" ]; then
    echo -e "${YELLOW}⚠️  Advertencia: No pareces estar en la raíz del proyecto${NC}"
    echo ""
    echo "Este script debe ejecutarse desde la raíz del proyecto (envia2/)"
    echo ""
    read -p "¿Continuar de todas formas? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Operación cancelada."
        exit 1
    fi
fi

# Verificar que el entorno virtual está activado
# Acepta tanto VIRTUAL_ENV (virtualenv/venv) como CONDA_DEFAULT_ENV (conda/miniconda)
if [ -z "$VIRTUAL_ENV" ] && [ -z "$CONDA_DEFAULT_ENV" ]; then
    echo -e "${YELLOW}⚠️  Advertencia: No se detectó un entorno virtual activo${NC}"
    echo ""
    echo "Recomendación: Activa el entorno virtual primero:"
    echo "  source venv/bin/activate  # virtualenv/venv"
    echo "  conda activate <nombre>   # conda/miniconda"
    echo ""
    read -p "¿Continuar de todas formas? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Operación cancelada."
        exit 1
    fi
elif [ -n "$CONDA_DEFAULT_ENV" ]; then
    echo -e "${GREEN}✅ Entorno conda detectado: $CONDA_DEFAULT_ENV${NC}"
    echo ""
fi

# Ejecutar el script con PYTHONPATH configurado
echo -e "${GREEN}▶️  Ejecutando: $SCRIPT_PATH${NC}"
echo ""

# Configurar PYTHONPATH y ejecutar
export PYTHONPATH=.
python "$SCRIPT_PATH" "$@"

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Script ejecutado exitosamente${NC}"
else
    echo -e "${RED}❌ El script terminó con código de error: $EXIT_CODE${NC}"
fi
echo ""

exit $EXIT_CODE
