from flask import Flask, jsonify
from .config import Settings
from .extensions import configure_logging
from .api import api_bp
from .web import web_bp

def create_app() -> Flask:
    """
    Application Factory Pattern.
    
    Crea y configura una instancia de la aplicación Flask.
    Esto permite crear múltiples instancias con diferentes configuraciones
    (ej. para testing vs producción) y evita variables globales.
    """
    settings = Settings.from_env()

    app = Flask(settings.app_name)
    app.config["SECRET_KEY"] = settings.secret_key

    configure_logging(app, settings.log_level)

    # Registro de Blueprints (Módulos de rutas)
    # url_prefix='/api/v1' versiona la API, buena práctica para evolución futura.
    app.register_blueprint(api_bp, url_prefix="/api/v1")
    app.register_blueprint(web_bp)

    @app.get("/health")
    def health():
        return jsonify(status="ok", app=settings.app_name, env=settings.flask_env), 200

    @app.errorhandler(404)
    def not_found(_):
        return jsonify(error="not_found"), 404

    return app
