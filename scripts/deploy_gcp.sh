#!/bin/bash
# Script de despliegue en Google Cloud Platform
# Despliega el Sistema de Seguimiento de OC en GCP Compute Engine

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Despliegue de Sistema de Seguimiento OC en GCP${NC}"
echo "========================================================="

# Parámetros
PROJECT_ID=${1}
INSTANCE_NAME=${2:-"oc-seguimiento"}
ZONE=${3:-"us-central1-a"}
MACHINE_TYPE=${4:-"e2-small"}

if [ -z "$PROJECT_ID" ]; then
    echo -e "${RED}❌ Error: Debes proporcionar el PROJECT_ID${NC}"
    echo "Uso: $0 <PROJECT_ID> [INSTANCE_NAME] [ZONE] [MACHINE_TYPE]"
    echo "Ejemplo: $0 my-project-123 oc-seguimiento us-central1-a e2-small"
    exit 1
fi

echo "Proyecto: $PROJECT_ID"
echo "Instancia: $INSTANCE_NAME"
echo "Zona: $ZONE"
echo "Tipo máquina: $MACHINE_TYPE"
echo ""

# Verificar gcloud instalado
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}❌ gcloud CLI no está instalado${NC}"
    echo "Instala desde: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Configurar proyecto
echo -e "${YELLOW}📋 Configurando proyecto...${NC}"
gcloud config set project $PROJECT_ID

# Crear instancia si no existe
echo -e "${YELLOW}🖥️  Creando instancia...${NC}"
if gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE &>/dev/null; then
    echo -e "${YELLOW}⚠️  La instancia $INSTANCE_NAME ya existe${NC}"
    read -p "¿Deseas recrearla? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Eliminando instancia existente..."
        gcloud compute instances delete $INSTANCE_NAME --zone=$ZONE --quiet
    else
        echo "Usando instancia existente..."
    fi
fi

if ! gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE &>/dev/null; then
    echo "Creando nueva instancia..."
    gcloud compute instances create $INSTANCE_NAME \
        --zone=$ZONE \
        --machine-type=$MACHINE_TYPE \
        --image-family=ubuntu-2204-lts \
        --image-project=ubuntu-os-cloud \
        --boot-disk-size=20GB \
        --boot-disk-type=pd-standard \
        --tags=http-server,https-server \
        --metadata=startup-script='#!/bin/bash
            apt-get update
            apt-get install -y python3.10 python3.10-venv python3-pip git
            echo "Instance ready for deployment"
        '

    echo -e "${GREEN}✅ Instancia creada${NC}"
    echo "Esperando que la instancia esté lista..."
    sleep 30
fi

# Obtener IP externa
EXTERNAL_IP=$(gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format="get(networkInterfaces[0].accessConfigs[0].natIP)")
echo -e "${GREEN}📍 IP externa: $EXTERNAL_IP${NC}"

# Crear regla de firewall para puerto 8001
echo -e "${YELLOW}🔥 Configurando firewall...${NC}"
if ! gcloud compute firewall-rules describe allow-oc-seguimiento &>/dev/null; then
    gcloud compute firewall-rules create allow-oc-seguimiento \
        --allow=tcp:8001 \
        --source-ranges=0.0.0.0/0 \
        --target-tags=http-server \
        --description="Allow access to OC Seguimiento system"
    echo -e "${GREEN}✅ Regla de firewall creada${NC}"
else
    echo "Regla de firewall ya existe"
fi

# Subir archivos
echo -e "${YELLOW}📤 Subiendo archivos...${NC}"
gcloud compute scp --recurse --zone=$ZONE \
    ./* $INSTANCE_NAME:~/oc-seguimiento/ \
    --exclude=".git/*" \
    --exclude="venv/*" \
    --exclude="*.pyc" \
    --exclude="__pycache__/*" \
    --exclude="logs/*" \
    --exclude=".env"

# Ejecutar setup en la instancia
echo -e "${YELLOW}⚙️  Configurando aplicación en la instancia...${NC}"
gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command="
    cd ~/oc-seguimiento
    python3.10 -m venv venv
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    mkdir -p logs static oc_files

    # Crear servicio systemd
    sudo tee /etc/systemd/system/oc-seguimiento.service > /dev/null <<EOF
[Unit]
Description=Sistema de Seguimiento OC
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/oc-seguimiento
Environment=\"PATH=/home/$USER/oc-seguimiento/venv/bin\"
ExecStart=/home/$USER/oc-seguimiento/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Habilitar servicio
    sudo systemctl daemon-reload
    sudo systemctl enable oc-seguimiento
"

echo ""
echo -e "${GREEN}=========================================================${NC}"
echo -e "${GREEN}✅ Despliegue completado exitosamente${NC}"
echo -e "${GREEN}=========================================================${NC}"
echo ""
echo "📝 Próximos pasos:"
echo ""
echo "1. Conectarse a la instancia:"
echo "   gcloud compute ssh $INSTANCE_NAME --zone=$ZONE"
echo ""
echo "2. Configurar credenciales:"
echo "   cd ~/oc-seguimiento"
echo "   cp .env.example .env"
echo "   nano .env"
echo ""
echo "3. Iniciar el servicio:"
echo "   sudo systemctl start oc-seguimiento"
echo "   sudo systemctl status oc-seguimiento"
echo ""
echo "4. Ver logs:"
echo "   sudo journalctl -u oc-seguimiento -f"
echo ""
echo "5. Acceder a la aplicación:"
echo "   http://$EXTERNAL_IP:8001"
echo ""
echo "📚 Para más información, consulta README.md"
