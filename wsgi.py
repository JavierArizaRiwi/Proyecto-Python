"""
Entry-point para Servidores WSGI de Producción (Gunicorn).

Este archivo expone la variable 'app' que Gunicorn buscará para ejecutar.
No contiene lógica, solo la instanciación.
"""
from app import create_app

app = create_app()
