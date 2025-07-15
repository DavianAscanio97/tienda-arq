#!/usr/bin/env python3
"""
Script de inicio que configura todo automáticamente
"""
import os
import sys
import subprocess

def install_dependencies():
    """Instala las dependencias"""
    print("📦 Instalando dependencias...")
    
    requirements_files = [
        "requirements-psycopg2.txt",
        "requirements-psycopg.txt", 
        "requirements.txt",
        "requirements-flexible.txt"
    ]
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            try:
                result = subprocess.run([
                    sys.executable, "-m", "pip", "install", "-r", req_file
                ], capture_output=True, text=True, timeout=300)
                
                if result.returncode == 0:
                    print(f"✅ Dependencias instaladas desde {req_file}")
                    return True
                else:
                    print(f"❌ Error con {req_file}: {result.stderr}")
            except Exception as e:
                print(f"❌ Error instalando {req_file}: {e}")
    
    return False

def setup_database():
    """Configura la base de datos"""
    print("🔄 Configurando base de datos...")
    
    try:
        # Configurar DATABASE_URL si no está definida
        if not os.getenv('DATABASE_URL'):
            os.environ['DATABASE_URL'] = 'postgresql://arq_cloud_tienda_user:mGuWS9nVgNMJslIDPBOOMX3AEmoser6E@dpg-d1qq7ibipnbc73elodog-a.oregon-postgres.render.com:5432/arq_cloud_tienda?sslmode=require'
            print("✅ DATABASE_URL configurada")
        
        # Ejecutar configuración de base de datos
        result = subprocess.run([
            sys.executable, "setup-external-db.py"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Base de datos configurada")
            return True
        else:
            print(f"❌ Error configurando BD: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error en setup de BD: {e}")
        return False

def start_application():
    """Inicia la aplicación"""
    print("🚀 Iniciando aplicación...")
    
    try:
        from app import app
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    except Exception as e:
        print(f"❌ Error iniciando app: {e}")
        return False

def main():
    """Función principal"""
    print("🎯 Iniciando configuración automática...")
    print("=" * 50)
    
    # Paso 1: Instalar dependencias
    if not install_dependencies():
        print("❌ Error instalando dependencias")
        sys.exit(1)
    
    # Paso 2: Configurar base de datos
    if not setup_database():
        print("❌ Error configurando base de datos")
        sys.exit(1)
    
    # Paso 3: Iniciar aplicación
    print("\n🎉 Configuración completada!")
    print("🌐 Iniciando aplicación...")
    start_application()

if __name__ == "__main__":
    main() 