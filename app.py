from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_admin.form import Select2Widget
from wtforms.fields import SelectField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_admin import AdminIndexView, expose
from flask_login import current_user

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
    return db.session.get(Usuario, int(user_id))

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
    categoria = db.relationship('Categoria', backref='productos')

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

class ProductoAdmin(SecureModelView):
    form_columns = ['nombre', 'descripcion', 'imagen', 'precio', 'id_categoria']
    form_extra_fields = {
        'id_categoria': QuerySelectField(
            'Categoría',
            query_factory=lambda: Categoria.query.all(),
            get_label='nom_categoria',
            allow_blank=False,
            get_pk=lambda c: c.id_categoria
        )
    }

class MyAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not (current_user.is_authenticated and current_user.is_admin):
            flash('Debes iniciar sesión como administrador para acceder al panel.', 'error')
            return redirect(url_for('login'))
        
        try:
            usuarios_count = Usuario.query.count()
            productos_count = Producto.query.count()
            categorias_count = Categoria.query.count()
        except Exception as e:
            print(f"Error obteniendo conteos: {e}")
            usuarios_count = 0
            productos_count = 0
            categorias_count = 0
            
        return self.render('admin/dashboard.html',
            usuarios_count=usuarios_count,
            productos_count=productos_count,
            categorias_count=categorias_count
        )

admin = Admin(
    app,
    name='Panel Admin',
    template_mode='bootstrap3',
    index_view=MyAdminIndexView(name='Dashboard'),
    base_template='admin/base.html'
)
admin.add_view(SecureModelView(Usuario, db.session))
admin.add_view(SecureModelView(Categoria, db.session))
admin.add_view(ProductoAdmin(Producto, db.session))

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/inicio/")
def inicio():
    return render_template("index.html")

@app.route('/productos')
def productos():
    productos = Producto.query.all()
    categorias = {c.id_categoria: c.nom_categoria for c in Categoria.query.all()}
    return render_template('plantilla1.html', productos=productos, categorias=categorias)

# Eliminar la función y ruta /servicios
def servicios():
    pass  # Eliminada para que la ruta no exista
# Elimina también el decorador @app.route('/servicios')

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
                return redirect(url_for('admin.index'))
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
                    return redirect(url_for('admin.index'))
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

# --- CRUD Productos ---
from flask import abort

@app.route('/admin/productos')
@login_required
def productos_crud():
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    productos = Producto.query.all()
    categorias = {c.id_categoria: c.nom_categoria for c in Categoria.query.all()}
    categorias_list = Categoria.query.all()
    
    return render_template('admin/productos.html', productos=productos, categorias=categorias, categorias_list=categorias_list)

@app.route('/admin/productos/nuevo', methods=['GET', 'POST'])
@login_required
def producto_nuevo():
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    categorias = Categoria.query.all()
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        imagen = request.form['imagen']
        id_categoria = request.form['id_categoria']
        nuevo = Producto(nombre=nombre, descripcion=descripcion, precio=precio, imagen=imagen, id_categoria=id_categoria)
        db.session.add(nuevo)
        db.session.commit()
        flash('Producto agregado correctamente', 'success')
        return redirect(url_for('productos_crud'))
    return render_template('admin/producto_form.html', categorias=categorias, producto=None)

@app.route('/admin/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def producto_editar(id):
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    producto = Producto.query.get_or_404(id)
    categorias = Categoria.query.all()
    if request.method == 'POST':
        producto.nombre = request.form['nombre']
        producto.descripcion = request.form['descripcion']
        producto.precio = float(request.form['precio'])
        producto.imagen = request.form['imagen']
        producto.id_categoria = int(request.form['id_categoria'])
        db.session.commit()
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('productos_crud'))
    return render_template('admin/producto_form.html', categorias=categorias, producto=producto)

@app.route('/admin/productos/eliminar/<int:id>')
@login_required
def producto_eliminar(id):
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('productos_crud'))

# --- CRUD Categorías ---
@app.route('/admin/categorias')
@login_required
def categorias_crud():
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    categorias = Categoria.query.all()
    return render_template('admin/categorias.html', categorias=categorias)

@app.route('/admin/categorias/nueva', methods=['GET', 'POST'])
@login_required
def categoria_nueva():
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        nom_categoria = request.form['nom_categoria']
        nueva = Categoria(nom_categoria=nom_categoria)
        db.session.add(nueva)
        db.session.commit()
        flash('Categoría agregada correctamente', 'success')
        return redirect(url_for('categorias_crud'))
    return render_template('admin/categoria_form.html', categoria=None)

@app.route('/admin/categorias/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def categoria_editar(id):
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    categoria = Categoria.query.get_or_404(id)
    if request.method == 'POST':
        categoria.nom_categoria = request.form['nom_categoria']
        db.session.commit()
        flash('Categoría actualizada correctamente', 'success')
        return redirect(url_for('categorias_crud'))
    return render_template('admin/categoria_form.html', categoria=categoria)

@app.route('/admin/categorias/eliminar/<int:id>')
@login_required
def categoria_eliminar(id):
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    categoria = Categoria.query.get_or_404(id)
    db.session.delete(categoria)
    db.session.commit()
    flash('Categoría eliminada correctamente', 'success')
    return redirect(url_for('categorias_crud'))

@app.route('/admin/usuarios')
@login_required
def usuarios_crud():
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@app.route('/admin/usuarios/nuevo', methods=['GET', 'POST'])
@login_required
def usuario_nuevo():
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        nom_usuario = request.form['nom_usuario']
        ape_usuario = request.form['ape_usuario']
        email = request.form['email']
        password = request.form['password']
        is_admin = 'is_admin' in request.form
        
        if Usuario.query.filter_by(email=email).first():
            flash('El email ya está registrado', 'error')
            return render_template('admin/usuario_form.html', usuario=None)
        
        nuevo_usuario = Usuario(
            nom_usuario=nom_usuario,
            ape_usuario=ape_usuario,
            email=email,
            is_admin=is_admin
        )
        nuevo_usuario.set_password(password)
        
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usuario agregado correctamente', 'success')
        return redirect(url_for('usuarios_crud'))
    
    return render_template('admin/usuario_form.html', usuario=None)

@app.route('/admin/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def usuario_editar(id):
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    usuario = Usuario.query.get_or_404(id)
    if request.method == 'POST':
        usuario.nom_usuario = request.form['nom_usuario']
        usuario.ape_usuario = request.form['ape_usuario']
        usuario.email = request.form['email']
        usuario.is_admin = 'is_admin' in request.form
        
        # Solo cambiar contraseña si se proporciona una nueva
        if request.form.get('password'):
            usuario.set_password(request.form['password'])
        
        db.session.commit()
        flash('Usuario actualizado correctamente', 'success')
        return redirect(url_for('usuarios_crud'))
    
    return render_template('admin/usuario_form.html', usuario=usuario)

@app.route('/admin/usuarios/eliminar/<int:id>')
@login_required
def usuario_eliminar(id):
    if not current_user.is_admin:
        flash('Acceso denegado. Solo administradores pueden acceder.', 'error')
        return redirect(url_for('home'))
    
    usuario = Usuario.query.get_or_404(id)
    
    # No permitir eliminar el usuario actual
    if usuario.id_ud_usuario == current_user.id_ud_usuario:
        flash('No puedes eliminar tu propia cuenta', 'error')
        return redirect(url_for('usuarios_crud'))
    
    db.session.delete(usuario)
    db.session.commit()
    flash('Usuario eliminado correctamente', 'success')
    return redirect(url_for('usuarios_crud'))

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

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)