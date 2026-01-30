# Flask API Production-Ready + Docker Deployment

API REST desarrollada con Flask, estructurada con App Factory,
Blueprints y lista para producción con Docker.

------------------------------------------------------------------------

## Características

-   App Factory (create_app)
-   Blueprints
-   Configuración por entorno (.env)
-   Endpoint /health
-   Logging configurable
-   Gunicorn para producción
-   Docker y Docker Compose

------------------------------------------------------------------------

## Requisitos

-   Python 3.10+
-   Docker
-   Docker Compose

------------------------------------------------------------------------

## Estructura del Proyecto

    .
    ├── app/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── extensions.py
    │   ├── api/
    │   │   └── routes.py
    │   └── web/
    │       └── routes.py
    ├── run.py
    ├── wsgi.py
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
    ├── .env.example
    └── .gitignore

------------------------------------------------------------------------

## Configuración de Variables de Entorno

``` bash
cp .env.example .env
```

Ejemplo:

``` env
FLASK_ENV=production
APP_NAME=flask-api
LOG_LEVEL=INFO
SECRET_KEY=secret_key
PORT=8000
```

------------------------------------------------------------------------

## Ejecución Local

### Crear entorno virtual

``` bash
python -m venv venv
source venv/bin/activate
```

### Instalar dependencias

``` bash
pip install -r requirements.txt
```

### Ejecutar

``` bash
python -m flask --app run:app run --host 0.0.0.0 --port 8000
```

------------------------------------------------------------------------

## Ejecución con Docker

### Construir y levantar

``` bash
docker compose up --build
```

### Probar

``` bash
curl http://localhost:8080/health
```

------------------------------------------------------------------------

## Dockerfile (Ejemplo)

``` dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "wsgi:app"]
```

------------------------------------------------------------------------

## docker-compose.yml (Ejemplo)

``` yaml
version: "3.9"

services:
  api:
    build: .
    container_name: flask-api
    env_file:
      - .env
    ports:
      - "8080:8000"
    restart: always
```

------------------------------------------------------------------------

## Endpoints

### Health

``` bash
GET /health
```

### Ping

``` bash
GET /api/v1/ping
```

------------------------------------------------------------------------

## Despliegue en EC2 con Docker

### 1. Instalar Docker

``` bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl enable docker
sudo systemctl start docker
```

### 2. Clonar proyecto

``` bash
git clone <REPO_URL>
cd proyecto
```

### 3. Configurar entorno

``` bash
cp .env.example .env
```

### 4. Construir y ejecutar

``` bash
docker compose up -d --build
```

### 5. Verificar

``` bash
docker ps
curl http://localhost:8080/health
```

------------------------------------------------------------------------

## Healthcheck para Load Balancer

Configurar en ALB:

-   Path: /health
-   Success code: 200
-   Interval: 30s

------------------------------------------------------------------------

## Seguridad

-   No subir .env
-   Usar HTTPS
-   Cerrar puertos innecesarios
-   Usar Secrets Manager

------------------------------------------------------------------------

## Logging

Controlado con:

``` env
LOG_LEVEL=INFO
```

------------------------------------------------------------------------

## Escalabilidad

Preparado para:

-   AutoScaling
-   Docker Swarm
-   ECS / EKS

------------------------------------------------------------------------

## Autor

Javier Ariza

Plantilla profesional para APIs Flask en producción.