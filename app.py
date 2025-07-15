from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Crear la app Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '32Rr_66062626')
database_url = os.getenv('DATABASE_URL')
if not database_url:
    # Fallback local
    database_url = 'postgresql://arq_cloud_tienda_user:mGuWS9nVgNMJslIDPBOOMX3AEmoser6E@dpg-d1qq7ibipnbc73elodog-a:5432/arq_cloud_tienda?sslmode=require'

# 2) Configura SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 3) Fuerza SSL/TLS (ojo: necesario solo si tu URL no incluye sslmode)
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {'sslmode': 'require'}
}

db = SQLAlchemy(app)

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Modelos
class Categoria(db.Model):
    __tablename__ = 'categorias'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nom_categoria = db.Column(db.String(100), nullable=False)

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text)
    imagen = db.Column(db.String(200))
    precio = db.Column(db.Float, nullable=False)
    id_categoria = db.Column(db.Integer, db.ForeignKey('categorias.id_categoria'), nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_ud_usuario = db.Column(db.Integer, primary_key=True)
    nom_usuario = db.Column(db.String(50), nullable=False)
    ape_usuario = db.Column(db.String(50), nullable=False)
    pasword = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def get_id(self):
        return str(self.id_ud_usuario)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def set_password(self, password):
        self.pasword = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.pasword, password)

# Vista personalizada para el admin que requiere autenticación
class SecureModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

# Flask-Admin
admin = Admin(app, name='Panel Admin', template_mode='bootstrap3')
admin.add_view(SecureModelView(Usuario, db.session))
admin.add_view(SecureModelView(Categoria, db.session))
admin.add_view(SecureModelView(Producto, db.session))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/inicio/")
def inicio():
    return render_template("index.html")

@app.route('/productos')
def productos():
    return render_template('plantilla1.html')

@app.route('/servicios')
def servicios():
    return render_template('plantilla2.html')

@app.route('/ventas')
def ventas():
    productos = Producto.query.all()
    return render_template('ventas.html', productos=productos)

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = Usuario.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('¡Inicio de sesión exitoso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Email o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('home'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        nom_usuario = request.form.get('nom_usuario')
        ape_usuario = request.form.get('ape_usuario')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('register.html')
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return render_template('register.html')
        
        user = Usuario(
            nom_usuario=nom_usuario,
            ape_usuario=ape_usuario,
            email=email
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('¡Registro exitoso! Ahora puedes iniciar sesión', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/admin')
@login_required
def admin_panel():
    if not current_user.is_admin:
        flash('No tienes permisos para acceder al panel de administración', 'error')
        return redirect(url_for('home'))
    return redirect('/admin/')

if __name__ == '__main__':
    app.run(debug=True)