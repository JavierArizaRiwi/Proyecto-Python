# Flask API (Production-ready) + Docker (Staging/Prod friendly)

Proyecto Flask bien organizado, listo para desplegar con Docker.
Incluye:
- App factory (create_app)
- Blueprints
- Config por entorno (.env)
- Endpoint /health (ideal para ALB/ASG)
- Logging básico
- Dockerfile + docker-compose
- Gunicorn para producción

## 1) Requisitos
- Docker y Docker Compose instalados

## 2) Ejecutar en local (sin Docker)
```bash
python -m venv venv
source venv/bin/activate  # en Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python -m flask --app run:app run --host 0.0.0.0 --port 8000
```

Probar:
```bash
# 1. Health check
curl -i http://localhost:8000/health
# 2. Ping
curl -i http://localhost:8000/api/v1/ping
# 3. Crear Compra
curl -i -X POST -H "Content-Type: application/json" -d '{"user_id": "u1", "items": [{"product_id": "p1", "price": 10, "quantity": 2}]}' http://localhost:8000/api/v1/purchases
# 4. Ver Compra (copia el ID del paso anterior)
# curl -i http://localhost:8000/api/v1/purchases/<ID_AQUI>
```

## 3) Ejecutar con Docker (dev/prod con Gunicorn)
```bash
cp .env.example .env
docker compose up --build
```

Probar:
```bash
curl -i http://localhost:8080/health
```

## 4) Variables de entorno
Copia `.env.example` a `.env` y ajusta valores.

- `FLASK_ENV`: development | production
- `APP_NAME`: nombre de la app
- `LOG_LEVEL`: DEBUG | INFO | WARNING | ERROR
- `SECRET_KEY`: clave (no la subas al repo)
- `PORT`: puerto interno de la app dentro del contenedor (default 8000)

## 5) Estructura
```
.
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   └── web/
│       ├── __init__.py
│       └── routes.py
├── run.py
├── wsgi.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── .env.example
└── .gitignore
```

## 6) Despliegue recomendado en EC2 + NGINX (tu arquitectura)
- Docker expone **solo a loopback**: `127.0.0.1:8080:8000`
- NGINX recibe 80/443 y hace reverse proxy a `127.0.0.1:8080`

Ejemplo NGINX (prod):
```nginx
server {
  listen 80;
  server_name api.tudominio.com;

  location / {
    proxy_pass http://127.0.0.1:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
  }
}
```

## 7) Healthcheck para AutoScaling / ALB
Configura el Target Group para usar:
- Path: `/health`
- Success codes: `200`
# Proyecto-Python
