#!/usr/bin/env python3
"""
Script para configurar la base de datos externa de Render
"""
import os
import sys

def setup_external_database():
    """Configura la base de datos externa"""
    print("🚀 Configurando base de datos externa...")
    
    # Configurar variables de entorno
    os.environ['DATABASE_URL'] = 'postgresql://arq_cloud_tienda_user:mGuWS9nVgNMJslIDPBOOMX3AEmoser6E@dpg-d1qq7ibipnbc73elodog-a.oregon-postgres.render.com:5432/arq_cloud_tienda?sslmode=require'
    
    print("✅ Variables de entorno configuradas")
    
    try:
        # Importar después de configurar las variables
        from app import app, db, Usuario
        from sqlalchemy import text, inspect
        
        with app.app_context():
            print("🔄 Conectando a la base de datos...")
            
            # Crear tablas
            db.create_all()
            print("✅ Tablas creadas/verificadas")
            
            # Verificar tabla usuarios
            inspector = inspect(db.engine)
            if 'usuarios' in inspector.get_table_names():
                existing_columns = [col['name'] for col in inspector.get_columns('usuarios')]
                print(f"📋 Columnas existentes: {existing_columns}")
                
                # Agregar columnas si no existen
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
            
            # Crear usuario administrador
            admin = Usuario.query.filter_by(is_admin=True).first()
            if not admin:
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
                print("📧 Email: admin@tienda.com")
                print("🔑 Contraseña: admin123")
            else:
                print("✅ Usuario administrador ya existe")
            
            # Verificar conexión
            result = db.session.execute(text("SELECT COUNT(*) FROM usuarios"))
            count = result.fetchone()[0]
            print(f"👤 Total de usuarios en la base de datos: {count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = setup_external_database()
    if success:
        print("\n🎉 Configuración completada exitosamente!")
        print("🌐 La aplicación está lista para usar")
    else:
        print("\n❌ Error en la configuración")
        sys.exit(1) 