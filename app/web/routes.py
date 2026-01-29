from flask import jsonify
from . import web_bp

@web_bp.get("/")
def index():
    return jsonify(message="Flask API up. Try /api/v1/ping or /health"), 200
