from flask import jsonify
from http import HTTPStatus
from . import api_bp

# --- General Utility Endpoints ---
# Este módulo define rutas de utilidad general que no están ligadas
# a un recurso de negocio específico (como 'purchases').
# Es el lugar ideal para endpoints de infraestructura, diagnóstico o metadatos de la API.

@api_bp.get("/ping")
def ping():
    """
    Endpoint de diagnóstico básico (Connectivity Check).
    
    Uso:
    - Verificación rápida de que el servidor web (Gunicorn/Flask) está aceptando peticiones.
    - A diferencia de un '/health' completo (que verificaría DB, caché, etc.), esto es ligero.
    - Utilizado por Load Balancers o herramientas de monitoreo (ej. UptimeRobot) para 'Heartbeats'.
    """
    # Retornamos un JSON estándar y usamos HTTPStatus.OK para evitar "números mágicos".
    return jsonify(message="pong"), HTTPStatus.OK
