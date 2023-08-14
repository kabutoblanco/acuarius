# Utiliza una imagen base ligera de Ubuntu
FROM debian:bullseye-slim

# Actualiza el sistema y instala las dependencias necesarias
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip nginx certbot

# Establece el directorio de trabajo
WORKDIR /app

# Copia el código fuente de la aplicación a la imagen
COPY . /app

# Instala las dependencias de la aplicación Django
RUN pip3 install -r requirements.txt
RUN python3 manage.py collectstatic --noinput
RUN pip3 install --upgrade certbot
RUN mkdir -p /var/www/html/.well-known/acme-challenge/ && \
    ln -s /var/www/html/.well-known/acme-challenge/ /etc/letsencrypt/.well-known/acme-challenge

# Configura Nginx para servir archivos estáticos
COPY nginx.conf /etc/nginx/sites-available/default

# Exponer el puerto 80 para Nginx
EXPOSE 80
EXPOSE 443
EXPOSE 8080

# Inicia Nginx y la aplicación Django
CMD service nginx start && gunicorn acuarius.wsgi:application --bind 0.0.0.0:8000
