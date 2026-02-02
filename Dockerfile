# Usamos una imagen base ligera (slim) para reducir el tamaño final y la superficie de ataque.
FROM python:3.11-slim

# Evita que Python genere archivos .pyc (bytecode), innecesarios en contenedores efímeros.
ENV PYTHONDONTWRITEBYTECODE=1
# Asegura que los logs de Python se envíen directamente a la salida estándar (stdout) sin buffer,
# permitiendo ver los logs en tiempo real con 'docker logs'.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalamos curl para poder ejecutar el HEALTHCHECK definido en docker-compose.
# Limpiamos la caché de apt para mantener la imagen pequeña.
RUN apt-get update && apt-get install -y --no-install-recommends     curl  && rm -rf /var/lib/apt/lists/*

# Copiamos primero solo los requirements.
# Esto aprovecha la caché de capas de Docker: si no cambian las dependencias, no se reinstalan.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el resto del código fuente.
COPY . .

# Exponemos el puerto donde correrá Gunicorn (interno del contenedor).
EXPOSE 8000

# Comando de inicio:
# -w 2: Dos workers (procesos) para manejar concurrencia.
# -b 0.0.0.0:8000: Escuchar en todas las interfaces de red del contenedor.
CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "wsgi:app"]
