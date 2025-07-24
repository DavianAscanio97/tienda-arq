# Tienda Digital - API y Web

Este proyecto implementa una tienda digital con autenticación, panel de administración y endpoints RESTful para productos.

## Estructura del Proyecto

- `app.py`: Aplicación principal Flask (modelos, rutas web y API, configuración).
- `templates/`: Plantillas HTML esenciales para la web.
- `requirements.txt`: Dependencias del proyecto.
- `Procfile`, `wsgi.py`, `runtime.txt`, `render.yaml`: Archivos para despliegue en Render o similar.

## Instalación y Ejecución

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Configura las variables de entorno si es necesario (`SECRET_KEY`, `DATABASE_URL`).
3. Ejecuta la aplicación:
   ```bash
   python app.py
   ```

## Endpoints Principales

### Web
- `/` : Página principal
- `/login` : Login de usuario
- `/register` : Registro de usuario
- `/admin` : Panel de administración (requiere usuario admin)
- `/productos` : Vista de productos
- `/servicios` : Vista de servicios

### API REST
- `GET /status` : Estado del servicio (JSON)
- `GET /api/productos` : Listar productos (JSON)
- `POST /api/agregar` : Agregar producto (JSON)

## Notas
- El modelo de datos y la lógica están centralizados en `app.py`.
- El proyecto está listo para despliegue en Render u otros servicios compatibles con WSGI.

---

¡Proyecto simplificado y organizado para fácil mantenimiento y despliegue! 