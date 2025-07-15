#!/usr/bin/env bash
set -e

echo "🚀 Iniciando build para Render..."

# Verificar versión de Python
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "🐍 Python version detectada: $python_version"

# Intentar usar Python 3.11 si está disponible
if command -v python3.11 &> /dev/null; then
    echo "✅ Python 3.11 encontrado, usando esta versión"
    PYTHON_CMD="python3.11"
elif [[ "$python_version" == "3.11"* ]]; then
    echo "✅ Python 3.11 ya está en uso"
    PYTHON_CMD="python3"
else
    echo "⚠️  Python 3.11 no encontrado, usando versión disponible: $python_version"
    PYTHON_CMD="python3"
fi

# Instalar dependencias
echo "📦 Instalando dependencias..."
$PYTHON_CMD -m pip install --upgrade pip
$PYTHON_CMD -m pip install -r requirements.txt

# Ejecutar scripts de configuración
echo "🔧 Configurando aplicación..."
$PYTHON_CMD setup.py

echo "🔄 Ejecutando migraciones..."
$PYTHON_CMD migrate.py

echo "👤 Creando usuario administrador..."
$PYTHON_CMD crear_admin.py

echo "✅ Build completado exitosamente!" 