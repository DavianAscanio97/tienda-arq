#!/usr/bin/env python3
"""
Script que se ejecuta después del despliegue para configurar la base de datos
"""
import os
import sys
import time

def post_deploy_setup():
    """Configura la aplicación después del despliegue"""
    print("🚀 Iniciando configuración post-despliegue...")
    
    # Esperar un poco para que la base de datos esté lista
    time.sleep(5)
    
    try:
        # Importar después de que las dependencias estén instaladas
        from app import app, db
        from sqlalchemy import text, inspect
        
        with app.app_context():
            print("🔄 Configurando base de datos...")
            
            # Crear tablas
            db.create_all()
            print("✅ Tablas creadas")
            
            # Verificar y agregar columnas si es necesario
            inspector = inspect(db.engine)
            if 'usuarios' in inspector.get_table_names():
                existing_columns = [col['name'] for col in inspector.get_columns('usuarios')]
                
                if 'email' not in existing_columns:
                    db.session.execute(text("""
                        ALTER TABLE usuarios 
                        ADD COLUMN email VARCHAR(120) UNIQUE NOT NULL DEFAULT 'usuario@example.com'
                    """))
                    print("✅ Columna 'email' agregada")
                
                if 'is_admin' not in existing_columns:
                    db.session.execute(text("""
                        ALTER TABLE usuarios 
                        ADD COLUMN is_admin BOOLEAN DEFAULT FALSE
                    """))
                    print("✅ Columna 'is_admin' agregada")
                
                db.session.commit()
            
            # Crear admin si no existe
            from app import Usuario
            admin_existente = Usuario.query.filter_by(is_admin=True).first()
            
            if not admin_existente:
                admin = Usuario(
                    nom_usuario="Admin",
                    ape_usuario="Sistema",
                    email="admin@tienda.com",
                    is_admin=True
                )
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuario administrador creado")
            else:
                print("✅ Usuario administrador ya existe")
            
            print("🎉 Configuración post-despliegue completada!")
            return True
            
    except Exception as e:
        print(f"❌ Error en configuración post-despliegue: {e}")
        return False

if __name__ == "__main__":
    success = post_deploy_setup()
    sys.exit(0 if success else 1) 