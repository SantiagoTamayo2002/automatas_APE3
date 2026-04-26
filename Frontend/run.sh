#!/bin/bash
# Script para iniciar el frontend React

echo "======================================="
echo "  AFND Simulator — Frontend (React)"
echo "======================================="

cd "$(dirname "$0")"

if [ ! -d "node_modules" ]; then
    echo "Instalando dependencias npm..."
    npm install
fi

echo "Iniciando servidor en http://localhost:5173"
echo "Asegúrate de que el backend Flask esté corriendo en :5000"
echo ""
npm run dev
