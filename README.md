# Sistema de Tienda Digital con Autenticación

Este proyecto implementa un sistema completo de tienda digital con autenticación de usuarios y panel de administración.

## Características

- ✅ Sistema de autenticación completo (login/registro)
- ✅ Panel de administración protegido
- ✅ Gestión de usuarios, productos y categorías
- ✅ Interfaz moderna y responsive
- ✅ Base de datos PostgreSQL

## Instalación

### Opción 1: Despliegue en Render (Recomendado)

1. **Fork o clona este repositorio**
2. **Conecta tu repositorio a Render**
3. **Crea un nuevo Web Service en Render**
4. **Configura las variables de entorno automáticamente**
5. **¡Listo! Render ejecutará automáticamente las migraciones**

### Opción 2: Instalación Local

#### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

#### 2. Configurar variables de entorno (opcional)

```bash
export SECRET_KEY="tu_clave_secreta_aqui"
export DATABASE_URL="tu_url_de_postgresql"
```

#### 3. Actualizar la base de datos

```bash
python actualizar_db.py
```

#### 4. Crear usuario administrador

```bash
python crear_admin.py
```

#### 5. Ejecutar la aplicación

```bash
python app.py
```

## Acceso al Sistema

### Usuario Administrador (creado automáticamente)
- **Email:** admin@tienda.com
- **Contraseña:** admin123
- **URL del admin:** 
  - Local: http://localhost:5000/admin
  - Render: https://tu-app.onrender.com/admin

### Registro de nuevos usuarios
- **URL de registro:** 
  - Local: http://localhost:5000/register
  - Render: https://tu-app.onrender.com/register
- **URL de login:** 
  - Local: http://localhost:5000/login
  - Render: https://tu-app.onrender.com/login

## Despliegue en Render

### Configuración Automática

El proyecto incluye archivos de configuración para Render:

- **`render.yaml`**: Configuración automática del servicio y base de datos
- **`build.sh`**: Script que ejecuta migraciones automáticamente
- **`wsgi.py`**: Punto de entrada para Gunicorn

### Pasos para Desplegar

1. **Sube tu código a GitHub**
2. **Ve a [Render.com](https://render.com)**
3. **Crea un nuevo "Web Service"**
4. **Conecta tu repositorio de GitHub**
5. **Render detectará automáticamente la configuración**
6. **Las migraciones se ejecutarán automáticamente**

### Variables de Entorno en Render

Render configurará automáticamente:
- `DATABASE_URL`: URL de la base de datos PostgreSQL
- `SECRET_KEY`: Clave secreta generada automáticamente
- `PYTHON_VERSION`: Versión de Python (3.9.16)

## Estructura del Proyecto

```
tienda-arq/
├── app.py                 # Aplicación principal Flask
├── models.py              # Modelos de base de datos
├── requirements.txt       # Dependencias Python
├── wsgi.py                # Punto de entrada para producción
├── render.yaml            # Configuración para Render
├── build.sh               # Script de build para Render
├── crear_tablas.py        # Script para crear tablas
├── actualizar_db.py       # Script para actualizar BD
├── crear_admin.py         # Script para crear admin
├── .gitignore             # Archivos a ignorar en Git
├── static/                # Archivos estáticos
│   └── img/
│       └── logo.jpeg
└── templates/             # Plantillas HTML
    ├── index.html         # Página principal
    ├── login.html         # Página de login
    ├── register.html      # Página de registro
    ├── plantilla1.html    # Página de productos
    ├── plantilla2.html    # Página de servicios
    └── ventas.html        # Página de ventas
```

## Funcionalidades

### Sistema de Autenticación
- Registro de usuarios con validación
- Login seguro con hash de contraseñas
- Logout automático
- Protección de rutas con `@login_required`

### Panel de Administración
- Gestión de usuarios (CRUD)
- Gestión de productos (CRUD)
- Gestión de categorías (CRUD)
- Acceso restringido solo para administradores

### Seguridad
- Contraseñas hasheadas con Werkzeug
- Sesiones seguras con Flask-Login
- Validación de formularios
- Protección CSRF implícita

## Rutas Disponibles

- `/` - Página principal
- `/login` - Iniciar sesión
- `/register` - Registrarse
- `/logout` - Cerrar sesión
- `/admin` - Panel de administración
- `/productos` - Página de productos
- `/servicios` - Página de servicios
- `/ventas` - Página de ventas

## Tecnologías Utilizadas

- **Backend:** Flask, SQLAlchemy, Flask-Login
- **Base de Datos:** PostgreSQL
- **Frontend:** Bootstrap 5, HTML5, CSS3
- **Autenticación:** Flask-Login, Werkzeug
- **Admin:** Flask-Admin

## Notas Importantes

1. **Primera vez:** Ejecuta `actualizar_db.py` antes de `crear_admin.py`
2. **Seguridad:** Cambia la contraseña del admin después del primer login
3. **Base de datos:** Asegúrate de que PostgreSQL esté configurado correctamente
4. **Variables de entorno:** Configura `SECRET_KEY` y `DATABASE_URL` para producción

## Solución de Problemas

### Error de conexión a la base de datos
- Verifica que PostgreSQL esté ejecutándose
- Confirma las credenciales en `app.py`
- Asegúrate de que la base de datos exista

### Error de importación de módulos
- Instala todas las dependencias: `pip install -r requirements.txt`
- Verifica que estés en el directorio correcto

### Error de permisos de administrador
- Ejecuta `python crear_admin.py` para crear el usuario admin
- Verifica que el usuario tenga `is_admin = True` en la base de datos

### Error de psycopg2 en Render (Python 3.13)
- **Solución implementada:** Cambiado a Python 3.11.7 y psycopg2-binary 2.9.9
- **Archivos actualizados:** `requirements.txt`, `render.yaml`, `runtime.txt`
- **Scripts mejorados:** `migrate.py`, `setup.py` para mejor compatibilidad

### Error de puerto en Render
- **Solución implementada:** Configurado para usar `$PORT` automáticamente
- **Archivos actualizados:** `wsgi.py`, `app.py`, `Procfile` 