#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from werkzeug.security import generate_password_hash
from datetime import datetime

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import Usuario, Categoria, Producto

def crear_admin():
    """Crea un usuario administrador por defecto"""
    with app.app_context():
        try:
            # Verificar si ya existe un admin
            admin_existente = Usuario.query.filter_by(is_admin=True).first()
            if admin_existente:
                print(f"Ya existe un administrador: {admin_existente.email}")
                return
            
            # Crear usuario administrador
            admin = Usuario(
                nom_usuario="Administrador",
                ape_usuario="Sistema",
                email="admin@tienda.com",
                password_hash=generate_password_hash("Admin123!"),
                is_admin=True
            )
            
            db.session.add(admin)
            db.session.commit()
            
            print("Usuario administrador creado exitosamente!")
            print("Email: admin@tienda.com")
            print("Contraseña: Admin123!")
            print("\nCredenciales de acceso:")
            print("=========================")
            print("Email: admin@tienda.com")
            print("Contraseña: Admin123!")
            print("=========================")
            
        except Exception as e:
            print(f"Error al crear el administrador: {e}")
            try:
                db.session.rollback()
            except:
                pass

def crear_datos_ejemplo():
    """Crea datos de ejemplo para la tienda"""
    with app.app_context():
        try:
            # Crear categorías de ejemplo
            categorias = [
                Categoria(nom_categoria="Electrónicos", desc_categoria="Productos electrónicos y tecnología"),
                Categoria(nom_categoria="Ropa", desc_categoria="Vestimenta y accesorios"),
                Categoria(nom_categoria="Hogar", desc_categoria="Artículos para el hogar"),
                Categoria(nom_categoria="Deportes", desc_categoria="Equipamiento deportivo")
            ]
            
            for categoria in categorias:
                db.session.add(categoria)
            
            db.session.commit()
            print("Categorías de ejemplo creadas exitosamente!")
            
            # Crear productos de ejemplo
            productos = [
                Producto(
                    nom_producto="Laptop Gaming Pro",
                    desc_producto="Potente laptop para gaming con gráficos de última generación",
                    precio=1299.99,
                    stock=15,
                    categoria_id=1
                ),
                Producto(
                    nom_producto="Smartphone Ultra",
                    desc_producto="Smartphone con cámara de 108MP y batería de larga duración",
                    precio=899.99,
                    stock=25,
                    categoria_id=1
                ),
                Producto(
                    nom_producto="Camiseta Premium",
                    desc_producto="Camiseta de algodón 100% con diseño exclusivo",
                    precio=29.99,
                    stock=50,
                    categoria_id=2
                ),
                Producto(
                    nom_producto="Zapatillas Deportivas",
                    desc_producto="Zapatillas cómodas para running y entrenamiento",
                    precio=89.99,
                    stock=30,
                    categoria_id=4
                ),
                Producto(
                    nom_producto="Sofá Moderno",
                    desc_producto="Sofá elegante y cómodo para tu sala de estar",
                    precio=599.99,
                    stock=8,
                    categoria_id=3
                ),
                Producto(
                    nom_producto="Auriculares Wireless",
                    desc_producto="Auriculares con cancelación de ruido y sonido premium",
                    precio=199.99,
                    stock=20,
                    categoria_id=1
                ),
                Producto(
                    nom_producto="Lámpara LED",
                    desc_producto="Lámpara LED inteligente con control por app",
                    precio=49.99,
                    stock=35,
                    categoria_id=3
                ),
                Producto(
                    nom_producto="Smartwatch Pro",
                    desc_producto="Reloj inteligente con monitor cardíaco y GPS",
                    precio=299.99,
                    stock=12,
                    categoria_id=1
                )
            ]
            
            for producto in productos:
                db.session.add(producto)
            
            db.session.commit()
            print("Productos de ejemplo creados exitosamente!")
            
        except Exception as e:
            print(f"Error al crear datos de ejemplo: {e}")
            try:
                db.session.rollback()
            except:
                pass

def main():
    """Función principal"""
    print("Configurando la tienda digital...")
    print("=" * 50)
    
    # Crear tablas
    with app.app_context():
        try:
            db.create_all()
            print("Tablas de base de datos creadas exitosamente!")
        except Exception as e:
            print(f"Error al crear las tablas: {e}")
            return
    
    # Crear administrador
    print("\nCreando usuario administrador...")
    crear_admin()
    
    # Crear datos de ejemplo
    print("\nCreando datos de ejemplo...")
    crear_datos_ejemplo()
    
    print("\n" + "=" * 50)
    print("Configuración completada!")
    print("Puedes iniciar la aplicación con: python app.py")
    print("Accede al admin con: admin@tienda.com / Admin123!")

if __name__ == "__main__":
    main() 