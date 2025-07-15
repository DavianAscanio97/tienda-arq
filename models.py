from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Categoria(db.Model):
    __tablename__ = 'categorias'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nom_categoria = db.Column(db.String(100), nullable=False)
    productos = db.relationship('Producto', backref='categoria', lazy=True)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'
    id_ud_usuario = db.Column(db.Integer, primary_key=True)
    nom_usuario = db.Column(db.String(50), nullable=False)
    ape_usuario = db.Column(db.String(50), nullable=False)
    pasword = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def get_id(self):
        return str(self.id_ud_usuario)
    
    def set_password(self, password):
        self.pasword = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.pasword, password)