# Utiliza una imagen base ligera de Ubuntu
FROM debian:bullseye-slim

# Actualiza el sistema y instala las dependencias necesarias
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip nginx

# Establece el directorio de trabajo
WORKDIR /app

# Copia el código fuente de la aplicación a la imagen
COPY . /app

# Instala las dependencias de la aplicación Django
RUN pip3 install -r requirements.txt

# Configura Nginx para servir archivos estáticos
COPY nginx.conf /etc/nginx/sites-available/default

# Exponer el puerto 80 para Nginx
EXPOSE 80

# Inicia Nginx y la aplicación Django
CMD service nginx start && python3 manage.py runserver 0.0.0.0:8000