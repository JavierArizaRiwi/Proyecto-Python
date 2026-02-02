import logging
from flask import Flask

# --- Extensions & Infrastructure ---
# Este módulo centraliza la configuración de herramientas transversales
# como Logging, Bases de Datos (SQLAlchemy), Migraciones, JWT, etc.
# Mantiene el 'create_app' limpio y ordenado.

def configure_logging(app: Flask, level: str) -> None:
    """
    Configura el sistema de logging para que funcione bien con Docker.
    
    En contenedores, los logs deben ir a STDOUT/STDERR para que Docker
    los capture y los gestores de logs (ELK, CloudWatch) los procesen.
    """
    numeric_level = getattr(logging, level, logging.INFO)

    # StreamHandler envía los logs a la consola (stderr por defecto).
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)

    # Configuración del logger raíz (captura logs de librerías de terceros también)
    root = logging.getLogger()
    root.setLevel(numeric_level)

    # Evita duplicar handlers
    if not root.handlers:
        root.addHandler(handler)

    # Sincroniza el nivel del logger de Flask
    app.logger.setLevel(numeric_level)
