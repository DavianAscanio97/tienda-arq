from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Crear la app Flask
app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '32Rr_66062626')

# Configuración de base de datos para Render
database_url = os.getenv('DATABASE_URL')

# Detectar qué driver de PostgreSQL está disponible
try:
    import psycopg
    driver = "psycopg"
    print(f"Driver detectado: {driver}")
except ImportError:
    try:
        import psycopg2
        driver = "psycopg2"
        print(f"Driver detectado: {driver}")
    except ImportError:
        driver = "psycopg2"  # fallback
        print(f"No se encontro driver, usando fallback: {driver}")

# Configurar URL según el driver disponible
if database_url:
    print(f"URL original: {database_url}")
    if database_url.startswith('postgres://'):
        if driver == "psycopg":
            database_url = database_url.replace('postgres://', 'postgresql+psycopg://', 1)
        else:
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
    elif database_url.startswith('postgresql://') and driver == "psycopg":
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
    print(f"URL configurada: {database_url}")

if not database_url:
    # Fallback local
    if driver == "psycopg":
        database_url = 'postgresql+psycopg://arq_cloud_tienda_user:mGuWS9nVgNMJslIDPBOOMX3AEmoser6E@dpg-d1qq7ibipnbc73elodog-a.oregon-postgres.render.com/arq_cloud_tienda?sslmode=require'
    else:
        database_url = 'postgresql://arq_cloud_tienda_user:mGuWS9nVgNMJslIDPBOOMX3AEmoser6E@dpg-d1qq7ibipnbc73elodog-a.oregon-postgres.render.com/arq_cloud_tienda?sslmode=require'
    print(f"URL fallback: {database_url}")

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
    try:
        if current_user.is_authenticated:
            if current_user.is_admin:
                return redirect(url_for('admin_panel'))
            return redirect(url_for('home'))
        
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            if not email or not password:
                flash('Por favor completa todos los campos', 'error')
                return render_template('login.html')
            
            user = Usuario.query.filter_by(email=email).first()
            
            if user and user.check_password(password):
                login_user(user)
                flash(f'¡Bienvenido {user.nom_usuario} {user.ape_usuario}!', 'success')
                
                # Redirigir según el tipo de usuario
                if user.is_admin:
                    return redirect(url_for('admin_panel'))
                else:
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Email o contraseña incorrectos', 'error')
        
        return render_template('login.html')
    except Exception as e:
        print(f"Error en login: {e}")
        flash('Error interno del servidor. Por favor intenta de nuevo.', 'error')
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
    
    # Obtener estadísticas
    usuarios_count = Usuario.query.count()
    productos_count = Producto.query.count()
    categorias_count = Categoria.query.count()
    ventas_count = 0  # Por ahora 0, se puede implementar después
    
    return render_template('admin-welcome.html', 
                         usuarios_count=usuarios_count,
                         productos_count=productos_count,
                         categorias_count=categorias_count,
                         ventas_count=ventas_count)

# --- API REST: Endpoint de estado del servicio ---
@app.route('/status', methods=['GET'])
def service_status():
    """
    Endpoint de prueba para verificar el estado del servicio.
    Devuelve un mensaje JSON indicando que el servicio funciona correctamente.
    """
    return jsonify(message="El servicio está funcionando correctamente.")

# --- API REST: Listar productos ---
@app.route('/api/productos', methods=['GET'])
def listar_productos():
    """
    Endpoint para obtener todos los productos en formato JSON.
    """
    productos = Producto.query.all()
    return jsonify([
        {
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "precio": p.precio,
            "id_categoria": p.id_categoria
        }
        for p in productos
    ])

# --- API REST: Agregar producto ---
@app.route('/api/productos/agregar', methods=['POST'])
def agregar_producto():
    """
    Endpoint para agregar un nuevo producto vía JSON.
    Espera los campos: nombre, descripcion, precio, id_categoria.
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se proporcionaron datos JSON"}), 400
    try:
        nuevo = Producto(
            nombre=data["nombre"],
            descripcion=data.get("descripcion", ""),
            precio=data["precio"],
            id_categoria=data["id_categoria"]
        )
        db.session.add(nuevo)
        db.session.commit()
        return jsonify({"message": "Producto agregado correctamente."}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al agregar producto: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)