from flask import Blueprint

api_bp = Blueprint("api", __name__)

from . import routes  # noqa: E402,F401
print("--- CARGANDO MODULO PURCHASES ---")
from . import purchases  # noqa: E402,F401
print("--- MODULO PURCHASES CARGADO ---")
