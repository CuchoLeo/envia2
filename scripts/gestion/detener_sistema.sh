#!/bin/bash

# Script para detener el sistema de seguimiento de OC
# Versión Bash - Simple y rápida

echo ""
echo "============================================================"
echo "  🛑 DETENIENDO SISTEMA DE SEGUIMIENTO DE OC"
echo "============================================================"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contador de procesos detenidos
DETENIDOS=0

# Función para detener un proceso
detener_proceso() {
    local NOMBRE=$1
    local PATTERN=$2

    echo -n "   🔍 Buscando $NOMBRE... "

    # Buscar PIDs
    PIDS=$(pgrep -f "$PATTERN")

    if [ -z "$PIDS" ]; then
        echo -e "${YELLOW}No encontrado${NC}"
        return 0
    fi

    COUNT=$(echo "$PIDS" | wc -l | tr -d ' ')
    echo -e "${GREEN}Encontrado ($COUNT procesos)${NC}"

    # Detener cada PID
    for PID in $PIDS; do
        # Verificar que no sea el script actual
        if [ $PID -ne $$ ]; then
            echo -n "      🛑 Deteniendo PID $PID... "

            # Enviar SIGTERM
            kill -15 $PID 2>/dev/null

            # Esperar hasta 5 segundos
            for i in {1..10}; do
                if ! kill -0 $PID 2>/dev/null; then
                    echo -e "${GREEN}✅ Detenido${NC}"
                    DETENIDOS=$((DETENIDOS + 1))
                    break
                fi
                sleep 0.5
            done

            # Si sigue vivo, forzar
            if kill -0 $PID 2>/dev/null; then
                echo -n -e "${YELLOW}Forzando... ${NC}"
                kill -9 $PID 2>/dev/null
                sleep 0.5
                if ! kill -0 $PID 2>/dev/null; then
                    echo -e "${GREEN}✅ Terminado${NC}"
                    DETENIDOS=$((DETENIDOS + 1))
                else
                    echo -e "${RED}❌ Error${NC}"
                fi
            fi
        fi
    done

    echo ""
}

# Detener componentes del sistema
echo "📋 Deteniendo componentes del sistema..."
echo ""

detener_proceso "FastAPI (app.py)" "app.py"
detener_proceso "Monitor de Email" "email_monitor.py"
detener_proceso "Scheduler" "scheduler.py"
detener_proceso "Uvicorn" "uvicorn"

# Verificar si quedan procesos
echo "📋 Verificación final..."
echo ""

RESTANTES=$(pgrep -f "(app\.py|email_monitor\.py|scheduler\.py)" | grep -v $$ | wc -l | tr -d ' ')

if [ "$RESTANTES" -eq 0 ]; then
    echo -e "   ${GREEN}✅ Sistema completamente detenido${NC}"
else
    echo -e "   ${YELLOW}⚠️  Quedan $RESTANTES procesos activos${NC}"
    echo ""
    echo "   Procesos restantes:"
    pgrep -fa "(app\.py|email_monitor\.py|scheduler\.py)" | grep -v $$ | while read line; do
        echo "   • $line"
    done
fi

echo ""
echo "============================================================"
echo "  Resumen: $DETENIDOS procesos detenidos"
echo "============================================================"
echo ""
