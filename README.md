# Flask API Production-Ready + Docker Deployment

API REST profesional desarrollada con Flask, estructurada con App Factory,
Blueprints y lista para producción con Docker.

------------------------------------------------------------------------

## Características

-   App Factory (create_app)
-   Blueprints
-   Configuración por entorno (.env)
-   Endpoint /health
-   **Nginx** como Reverse Proxy
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
    ├── nginx/
    │   └── conf.d/
    │       └── default.conf
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
    build: 
      context: .
      dockerfile: Dockerfile
    container_name: flask-api
    env_file:
      - .env
    expose:
      - "8000"
    restart: always

  nginx:
    image: nginx:1.25-alpine
    container_name: nginx-proxy
    ports:
      - "80:80"
    volumes:
      - ./nginx/conf.d:/etc/nginx/conf.d
    depends_on:
      - api
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


# Flask API Production-Ready + Docker Deployment

Proyecto Flask bien organizado, listo para desplegar con Docker.
Incluye App Factory, Blueprints, configuración por entorno (.env), endpoint `/health`, logging básico, Dockerfile + Docker Compose y **Gunicorn** para producción.

---

## Probar (cURL) — base

> Estos comandos están pensados para ejecutarse **en local** apuntando al puerto **8000**.

```bash
# 1. Health check
curl -i http://localhost:8000/health

# 2. Ping
curl -i http://localhost:8000/api/v1/ping

# 3. Crear Compra
curl -i -X POST -H "Content-Type: application/json"   -d '{"user_id": "u1", "items": [{"product_id": "p1", "price": 10, "quantity": 2}]}'   http://localhost:8000/api/v1/purchases

# 4. Ver Compra (copia el ID del paso anterior)
# curl -i http://localhost:8000/api/v1/purchases/<ID_AQUI>
```

---

## CRUD completo — Purchases (cURL)

> Mantiene el mismo estilo de los ejemplos base: `curl -i` y JSON inline.

### 1) Crear compra (CREATE)

```bash
curl -i -X POST -H "Content-Type: application/json"   -d '{"user_id": "u1", "items": [{"product_id": "p1", "price": 10, "quantity": 2}]}'   http://localhost:8000/api/v1/purchases
```

**Tip:** copia el `id` que retorne la API y úsalo como `<ID_AQUI>` en los siguientes comandos.

---

### 2) Listar compras (READ ALL)

```bash
curl -i http://localhost:8000/api/v1/purchases
```

---

### 3) Ver compra por ID (READ ONE)

```bash
curl -i http://localhost:8000/api/v1/purchases/<ID_AQUI>
```

---

### 4) Actualizar compra por ID (UPDATE)

> Ajusta el payload según las reglas de tu API (por ejemplo, items completos vs parcheo).

```bash
curl -i -X PUT -H "Content-Type: application/json"   -d '{"user_id": "u1", "items": [{"product_id": "p1", "price": 12, "quantity": 3}]}'   http://localhost:8000/api/v1/purchases/<ID_AQUI>
```

---

### 5) Eliminar compra por ID (DELETE)

```bash
curl -i -X DELETE http://localhost:8000/api/v1/purchases/<ID_AQUI>
```

---

## Nota sobre puertos (8000 vs 8080)

- **Sin Docker (local):** normalmente se ejecuta en `http://localhost:8000`
- **Con Docker Compose:** muchas veces se expone `8080` en el host y `8000` en el contenedor, por ejemplo `8080:8000`

Si tu `docker-compose.yml` expone `8080:8000`, entonces los mismos cURL quedarían así:

```bash
curl -i http://localhost:8080/health
curl -i http://localhost:8080/api/v1/ping
curl -i -X POST -H "Content-Type: application/json"   -d '{"user_id": "u1", "items": [{"product_id": "p1", "price": 10, "quantity": 2}]}'   http://localhost:8080/api/v1/purchases
```

---

## Endpoints esperados

| Método | Endpoint | Descripción |
|---|---|---|
| GET | /health | Healthcheck (ALB/ASG) |
| GET | /api/v1/ping | Ping |
| POST | /api/v1/purchases | Crear compra |
| GET | /api/v1/purchases | Listar compras |
| GET | /api/v1/purchases/{id} | Obtener compra |
| PUT | /api/v1/purchases/{id} | Actualizar compra |
| DELETE | /api/v1/purchases/{id} | Eliminar compra |

## Autor

Javier Ariza

Plantilla profesional para APIs Flask en producción.