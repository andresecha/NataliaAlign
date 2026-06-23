#!/bin/bash
echo "==============================================="
echo "   Iniciando Alineamiento Multilingüe de Poesía"
echo "==============================================="

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python 3 no está instalado en este ordenador."
    echo "En Mac: Abre la Terminal y escribe 'xcode-select --install' o descárgalo desde python.org"
    echo "En Linux: Abre la terminal y usa 'sudo apt install python3 python3-venv'"
    read -p "Presiona Enter para salir..."
    exit 1
fi

# Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
    echo "Configurando la herramienta por primera vez (esto tomará unos minutos)..."
    python3 -m venv venv
fi

# Activar el entorno
source venv/bin/activate

echo "Verificando dependencias..."
pip install -r requirements.txt > /dev/null 2>&1

echo "¡Todo listo! Abriendo la aplicación en tu navegador..."
streamlit run app.py
