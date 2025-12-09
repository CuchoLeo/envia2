#!/bin/bash

# Script de gestión del sistema de seguimiento de OC
# Permite iniciar, detener y verificar el estado del sistema

# Colores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar el estado del sistema
mostrar_estado() {
    echo ""
    echo "============================================================"
    echo "  📊 ESTADO DEL SISTEMA DE SEGUIMIENTO DE OC"
    echo "============================================================"
    echo ""

    # Verificar si app.py está corriendo
    APP_PID=$(pgrep -f "python.*app\.py" | head -n 1)

    if [ -n "$APP_PID" ]; then
        echo -e "   ${GREEN}✅ Sistema ACTIVO${NC}"
        echo ""
        echo "   Procesos en ejecución:"
        ps aux | grep -E "(app\.py|email_monitor|scheduler)" | grep -v grep | while read line; do
            PID=$(echo $line | awk '{print $2}')
            CMD=$(echo $line | awk '{for(i=11;i<=NF;i++) printf $i" "; print ""}')
            echo -e "   ${GREEN}•${NC} PID $PID: $CMD"
        done

        # Verificar puerto web
        if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo ""
            echo -e "   ${GREEN}🌐 Dashboard accesible en:${NC} http://localhost:8000"
        fi
    else
        echo -e "   ${YELLOW}⚠️  Sistema DETENIDO${NC}"
    fi

    echo ""
    echo "============================================================"
    echo ""
}

# Función para iniciar el sistema
iniciar_sistema() {
    echo ""
    echo "============================================================"
    echo "  🚀 INICIANDO SISTEMA DE SEGUIMIENTO DE OC"
    echo "============================================================"
    echo ""

    # Verificar si ya está corriendo
    if pgrep -f "python.*app\.py" > /dev/null; then
        echo -e "   ${YELLOW}⚠️  El sistema ya está en ejecución${NC}"
        echo ""
        mostrar_estado
        return 1
    fi

    # Iniciar el sistema
    echo "   🔄 Iniciando aplicación..."
    nohup python app.py > logs/sistema.log 2>&1 &
    APP_PID=$!

    # Esperar un momento
    sleep 3

    # Verificar si inició correctamente
    if ps -p $APP_PID > /dev/null 2>&1; then
        echo -e "   ${GREEN}✅ Sistema iniciado exitosamente (PID: $APP_PID)${NC}"
        echo ""
        echo -e "   ${GREEN}🌐 Dashboard:${NC} http://localhost:8000"
        echo -e "   ${GREEN}📋 Logs:${NC} tail -f logs/sistema.log"
    else
        echo -e "   ${RED}❌ Error al iniciar el sistema${NC}"
        echo ""
        echo "   Revisa el archivo de logs para más detalles:"
        echo "   tail -n 50 logs/sistema.log"
        return 1
    fi

    echo ""
    echo "============================================================"
    echo ""
}

# Función para detener el sistema
detener_sistema() {
    echo ""
    echo "   Ejecutando script de detención..."
    echo ""

    if [ "$1" == "--force" ]; then
        python detener_sistema.py --force
    else
        python detener_sistema.py
    fi
}

# Función para reiniciar el sistema
reiniciar_sistema() {
    echo ""
    echo "============================================================"
    echo "  🔄 REINICIANDO SISTEMA DE SEGUIMIENTO DE OC"
    echo "============================================================"
    echo ""

    detener_sistema --force
    sleep 2
    iniciar_sistema
}

# Función para mostrar logs en tiempo real
mostrar_logs() {
    echo ""
    echo "============================================================"
    echo "  📋 LOGS DEL SISTEMA (Ctrl+C para salir)"
    echo "============================================================"
    echo ""

    if [ -f "logs/sistema.log" ]; then
        tail -f logs/sistema.log
    else
        echo -e "   ${YELLOW}⚠️  No se encontró el archivo de logs${NC}"
        echo ""
    fi
}

# Función para mostrar ayuda
mostrar_ayuda() {
    echo ""
    echo "============================================================"
    echo "  📖 GESTIÓN DEL SISTEMA DE SEGUIMIENTO DE OC"
    echo "============================================================"
    echo ""
    echo "  Uso: ./gestionar_sistema.sh [COMANDO]"
    echo ""
    echo "  Comandos disponibles:"
    echo ""
    echo "    start     - Inicia el sistema"
    echo "    stop      - Detiene el sistema"
    echo "    restart   - Reinicia el sistema"
    echo "    status    - Muestra el estado actual"
    echo "    logs      - Muestra logs en tiempo real"
    echo "    help      - Muestra esta ayuda"
    echo ""
    echo "  Ejemplos:"
    echo ""
    echo "    ./gestionar_sistema.sh start"
    echo "    ./gestionar_sistema.sh status"
    echo "    ./gestionar_sistema.sh restart"
    echo ""
    echo "============================================================"
    echo ""
}

# Menú principal
case "$1" in
    start)
        iniciar_sistema
        ;;
    stop)
        detener_sistema
        ;;
    restart)
        reiniciar_sistema
        ;;
    status)
        mostrar_estado
        ;;
    logs)
        mostrar_logs
        ;;
    help|--help|-h)
        mostrar_ayuda
        ;;
    *)
        echo ""
        echo -e "   ${RED}❌ Comando no reconocido: $1${NC}"
        mostrar_ayuda
        exit 1
        ;;
esac
