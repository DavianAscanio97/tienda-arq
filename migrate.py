#!/usr/bin/env python3
import os
import sys
from app import app, db
from sqlalchemy import text, inspect

def migrate_database():
    """Ejecuta las migraciones de la base de datos"""
    with app.app_context():
        try:
            print("🔄 Iniciando migraciones de base de datos...")
            
            # Crear todas las tablas si no existen
            db.create_all()
            print("✅ Tablas creadas/verificadas exitosamente!")
            
            # Verificar si la tabla usuarios existe
            inspector = inspect(db.engine)
            if 'usuarios' not in inspector.get_table_names():
                print("❌ La tabla 'usuarios' no existe")
                return False
            
            # Obtener columnas existentes
            existing_columns = [col['name'] for col in inspector.get_columns('usuarios')]
            print(f"📋 Columnas existentes: {existing_columns}")
            
            # Agregar columna email si no existe
            if 'email' not in existing_columns:
                try:
                    db.session.execute(text("""
                        ALTER TABLE usuarios 
                        ADD COLUMN email VARCHAR(120) UNIQUE NOT NULL DEFAULT 'usuario@example.com'
                    """))
                    print("✅ Columna 'email' agregada")
                except Exception as e:
                    print(f"⚠️  Error al agregar columna email: {e}")
            
            # Agregar columna is_admin si no existe
            if 'is_admin' not in existing_columns:
                try:
                    db.session.execute(text("""
                        ALTER TABLE usuarios 
                        ADD COLUMN is_admin BOOLEAN DEFAULT FALSE
                    """))
                    print("✅ Columna 'is_admin' agregada")
                except Exception as e:
                    print(f"⚠️  Error al agregar columna is_admin: {e}")
            
            db.session.commit()
            print("✅ Migraciones completadas exitosamente!")
            return True
            
        except Exception as e:
            print(f"❌ Error durante las migraciones: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    success = migrate_database()
    sys.exit(0 if success else 1) 