from app import app, db
from sqlalchemy import text

def actualizar_base_datos():
    with app.app_context():
        try:
            # Crear todas las tablas si no existen
            db.create_all()
            print("✅ Tablas creadas/verificadas exitosamente!")
            
            # Verificar si las columnas existen antes de agregarlas
            inspector = db.inspect(db.engine)
            existing_columns = [col['name'] for col in inspector.get_columns('usuarios')]
            
            # Agregar columna email si no existe
            if 'email' not in existing_columns:
                db.session.execute(text("""
                    ALTER TABLE usuarios 
                    ADD COLUMN email VARCHAR(120) UNIQUE NOT NULL DEFAULT 'usuario@example.com'
                """))
                print("✅ Columna 'email' agregada")
            
            # Agregar columna is_admin si no existe
            if 'is_admin' not in existing_columns:
                db.session.execute(text("""
                    ALTER TABLE usuarios 
                    ADD COLUMN is_admin BOOLEAN DEFAULT FALSE
                """))
                print("✅ Columna 'is_admin' agregada")
            
            db.session.commit()
            print("✅ Base de datos actualizada exitosamente!")
            
        except Exception as e:
            print(f"❌ Error al actualizar la base de datos: {e}")
            db.session.rollback()
            # Si hay error, intentar crear las tablas desde cero
            try:
                db.drop_all()
                db.create_all()
                print("✅ Tablas recreadas desde cero")
            except Exception as e2:
                print(f"❌ Error crítico: {e2}")

if __name__ == "__main__":
    actualizar_base_datos() 