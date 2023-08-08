# Usa la imagen base de Python
FROM python:3.8

# Establece la variable de entorno PYTHONUNBUFFERED a 1
ENV PYTHONUNBUFFERED 1

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el archivo de requisitos y lo instala
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Copia el resto de los archivos al directorio de trabajo
COPY . /app/

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar Gunicorn
CMD ["gunicorn", "acuarius.wsgi:application", "--bind", "0.0.0.0:8000"]