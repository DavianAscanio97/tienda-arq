from app import app, db
from sqlalchemy import text

def actualizar_base_datos():
    with app.app_context():
        try:
            # Agregar columna email si no existe
            db.session.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS email VARCHAR(120) UNIQUE NOT NULL DEFAULT 'usuario@example.com'
            """))
            
            # Agregar columna is_admin si no existe
            db.session.execute(text("""
                ALTER TABLE usuarios 
                ADD COLUMN IF NOT EXISTS is_admin BOOLEAN DEFAULT FALSE
            """))
            
            db.session.commit()
            print("✅ Base de datos actualizada exitosamente!")
            
        except Exception as e:
            print(f"❌ Error al actualizar la base de datos: {e}")
            db.session.rollback()

if __name__ == "__main__":
    actualizar_base_datos() 