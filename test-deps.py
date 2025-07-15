#!/usr/bin/env python3
"""
Script para probar diferentes configuraciones de dependencias
"""
import subprocess
import sys
import os

def test_requirements_file(requirements_file):
    """Prueba si un archivo de requirements se puede instalar"""
    print(f"🧪 Probando {requirements_file}...")
    
    try:
        # Intentar instalar las dependencias
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", requirements_file
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {requirements_file} - INSTALACIÓN EXITOSA")
            return True
        else:
            print(f"❌ {requirements_file} - ERROR:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {requirements_file} - TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {requirements_file} - ERROR: {e}")
        return False

def main():
    """Prueba todos los archivos de requirements"""
    print("🚀 Iniciando pruebas de dependencias...")
    
    requirements_files = [
        "requirements.txt",
        "requirements-psycopg.txt", 
        "requirements-psycopg2.txt",
        "requirements-flexible.txt"
    ]
    
    working_files = []
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            if test_requirements_file(req_file):
                working_files.append(req_file)
        else:
            print(f"⚠️  {req_file} - NO EXISTE")
    
    print("\n📊 RESULTADOS:")
    if working_files:
        print("✅ Archivos que funcionan:")
        for file in working_files:
            print(f"   - {file}")
        
        print(f"\n🎯 RECOMENDACIÓN: Usa {working_files[0]}")
        
        # Crear un archivo de recomendación
        with open("RECOMMENDED_REQUIREMENTS.txt", "w") as f:
            f.write(f"# Usar este archivo: {working_files[0]}\n")
            f.write(f"# Copia el contenido de {working_files[0]} aquí\n")
        
    else:
        print("❌ Ningún archivo de requirements funcionó")
        print("💡 Intenta con versiones más específicas")

if __name__ == "__main__":
    main() 