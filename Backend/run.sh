#!/bin/bash
# Script para iniciar el backend Flask

echo "======================================="
echo "  AFND Simulator — Backend (Flask)"
echo "======================================="

cd "$(dirname "$0")"

# Instalar dependencias si no existen
if ! python -c "import flask" 2>/dev/null; then
    echo "Instalando dependencias..."
    pip install -r requirements.txt
fi

echo "Iniciando servidor en http://localhost:5000"
echo ""
python app.py
