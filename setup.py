#!/usr/bin/env python3
"""
Script de configuración inicial para Render
"""
import os
import sys

def setup_environment():
    """Configura el entorno para Render"""
    print("🔧 Configurando entorno para Render...")
    
    # Verificar variables de entorno críticas
    required_vars = ['DATABASE_URL']
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️  Variables de entorno faltantes: {missing_vars}")
        print("Esto es normal en desarrollo local")
    else:
        print("✅ Variables de entorno configuradas correctamente")
    
    # Verificar Python version
    python_version = sys.version_info
    print(f"🐍 Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major == 3 and python_version.minor >= 11:
        print("✅ Versión de Python compatible")
    elif python_version.major == 3 and python_version.minor == 13:
        print("⚠️  Python 3.13 detectado - usando psycopg3 para compatibilidad")
    else:
        print("⚠️  Se recomienda Python 3.11+ para mejor compatibilidad")
    
    # Verificar si psycopg está disponible
    try:
        import psycopg
        print("✅ psycopg3 disponible")
    except ImportError:
        try:
            import psycopg2
            print("✅ psycopg2 disponible")
        except ImportError:
            print("❌ Error: No se encontró psycopg o psycopg2")
            return False
    
    return True

if __name__ == "__main__":
    setup_environment() 