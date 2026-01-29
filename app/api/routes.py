from flask import jsonify
from . import api_bp

@api_bp.get("/ping")
def ping():
    return jsonify(message="pong"), 200
