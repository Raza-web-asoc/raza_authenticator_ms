FROM python:3.11-slim

# Desactiva la verificación de versiones de pip y habilita la salida sin búfer
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/auth


# Establece el directorio de trabajo dentro del contenedor
WORKDIR /auth

# Copia el archivo de dependencias al directorio de trabajo
COPY requirements.txt /auth/

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt


# Copia todo el código de la aplicación al contenedor
COPY . .

RUN chmod +x app/scripts/wait-for-it.sh




