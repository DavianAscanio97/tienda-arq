# Usar una imagen base de Python 3.11
FROM python:3.11-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar los archivos de requisitos primero para aprovechar la caché de Docker
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY . .

# Crear un usuario no root para ejecutar la aplicación
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Exponer el puerto 5000
EXPOSE 5000

# Variables de entorno
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Comando para ejecutar la aplicación
CMD ["python", "app.py"] 