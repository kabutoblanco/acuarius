# Utiliza una imagen base ligera de Ubuntu
FROM debian:bullseye-slim

ENV NGINX_CONFIG ${NGINX_CONFIG}

# Actualiza el sistema y instala las dependencias necesarias
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip nginx

# Establece el directorio de trabajo
WORKDIR /app

# Copia el código fuente de la aplicación a la imagen
COPY . /app

# Instala las dependencias de la aplicación Django
RUN pip3 install -r requirements.txt
RUN python3 manage.py collectstatic --noinput

# Configura Nginx para servir archivos estáticos
COPY ./${NGINX_CONFIG} /etc/nginx/sites-available/default

# Exponer el puerto 80 para Nginx
EXPOSE 80
EXPOSE 443
