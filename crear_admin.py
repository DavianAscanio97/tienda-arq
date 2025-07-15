from app import app, db, Usuario

def crear_admin():
    with app.app_context():
        # Verificar si ya existe un admin
        admin_existente = Usuario.query.filter_by(is_admin=True).first()
        
        if admin_existente:
            print("Ya existe un usuario administrador.")
            return
        
        # Crear usuario administrador
        admin = Usuario(
            nom_usuario="Admin",
            ape_usuario="Sistema",
            email="admin@tienda.com",
            is_admin=True
        )
        admin.set_password("admin123")
        
        db.session.add(admin)
        db.session.commit()
        
        print("Usuario administrador creado exitosamente!")
        print("Email: admin@tienda.com")
        print("Contraseña: admin123")

if __name__ == "__main__":
    crear_admin() 