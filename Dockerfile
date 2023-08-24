# Utiliza una imagen base ligera de Ubuntu
FROM python:3.11.4-slim-buster

# Establece el directorio de trabajo
WORKDIR /app

# Copia el código fuente de la aplicación a la imagen
COPY . /app

# Instala las dependencias de la aplicación Django
RUN pip3 install -r requirements.txt
RUN python3 manage.py collectstatic --noinput
