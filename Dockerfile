FROM python:3.11-slim

# Desactiva la verificación de versiones de pip y habilita la salida sin búfer
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias al directorio de trabajo
COPY requirements.txt /app/

# Instala dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copia el script wait-for-it y hazlo ejecutable
COPY app/scripts/wait-for-it.sh /usr/local/bin/wait-for-it
RUN chmod +x /usr/local/bin/wait-for-it

# Copia todo el código de la aplicación al contenedor
COPY . .

# Expone el puerto 8000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
