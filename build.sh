#!/usr/bin/env bash
# exit on error
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones de base de datos
python actualizar_db.py

# Crear usuario administrador si no existe
python crear_admin.py 