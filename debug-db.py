#!/usr/bin/env python3
"""
Script de diagnóstico para la base de datos
"""
import os
import sys
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

def test_database_connection():
    """Prueba la conexión a la base de datos"""
    print("Iniciando diagnostico de base de datos...")
    
    # Obtener URL de la base de datos
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("DATABASE_URL no esta configurada")
        return False
    
    print(f"URL de base de datos: {database_url}")
    
    # Detectar driver
    try:
        import psycopg
        driver = "psycopg"
        print("Driver psycopg detectado")
    except ImportError:
        try:
            import psycopg2
            driver = "psycopg2"
            print("Driver psycopg2 detectado")
        except ImportError:
            print("No se encontro driver de PostgreSQL")
            return False
    
    # Configurar URL según el driver
    if database_url.startswith('postgres://'):
        if driver == "psycopg":
            database_url = database_url.replace('postgres://', 'postgresql+psycopg://', 1)
        else:
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
    elif database_url.startswith('postgresql://') and driver == "psycopg":
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
    
    print(f"URL configurada: {database_url}")
    
    try:
        # Crear engine
        engine = create_engine(database_url, echo=True)
        
        # Probar conexión
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"Conexion exitosa - PostgreSQL: {version}")
            
            # Verificar tablas
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            print(f"Tablas encontradas: {tables}")
            
            # Verificar tabla usuarios
            if 'usuarios' in tables:
                columns = [col['name'] for col in inspector.get_columns('usuarios')]
                print(f"Columnas en tabla usuarios: {columns}")
                
                # Verificar si hay usuarios
                result = connection.execute(text("SELECT COUNT(*) FROM usuarios"))
                count = result.fetchone()[0]
                print(f"Numero de usuarios: {count}")
                
                # Verificar admins
                result = connection.execute(text("SELECT COUNT(*) FROM usuarios WHERE is_admin = true"))
                admin_count = result.fetchone()[0]
                print(f"Numero de administradores: {admin_count}")
            else:
                print("Tabla 'usuarios' no existe")
            
            return True
            
    except SQLAlchemyError as e:
        print(f"Error de SQLAlchemy: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def create_tables_and_admin():
    """Crea las tablas y el usuario administrador"""
    print("\nCreando tablas y usuario administrador...")
    
    try:
        from app import app, db, Usuario
        
        with app.app_context():
            # Crear tablas
            db.create_all()
            print("Tablas creadas")
            
            # Verificar si existe admin
            admin = Usuario.query.filter_by(is_admin=True).first()
            if not admin:
                # Crear admin
                admin = Usuario(
                    nom_usuario="Admin",
                    ape_usuario="Sistema",
                    email="admin@tienda.com",
                    is_admin=True
                )
                admin.set_password("admin123")
                db.session.add(admin)
                db.session.commit()
                print("Usuario administrador creado")
                print("Email: admin@tienda.com")
                print("Contraseña: admin123")
            else:
                print("Usuario administrador ya existe")
            
            return True
            
    except Exception as e:
        print(f"Error al crear tablas/admin: {e}")
        return False

if __name__ == "__main__":
    print("Diagnostico de Base de Datos")
    print("=" * 50)
    
    # Probar conexión
    if test_database_connection():
        print("\nConexion a base de datos exitosa")
        
        # Crear tablas y admin
        if create_tables_and_admin():
            print("\nConfiguracion completada exitosamente!")
        else:
            print("\nError al configurar tablas/administrador")
    else:
        print("\nError de conexion a la base de datos")
        sys.exit(1) 