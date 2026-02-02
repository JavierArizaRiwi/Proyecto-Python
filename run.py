"""
Entry-point para Desarrollo Local.

Se ejecuta con 'python run.py' o 'flask run'.
No debe usarse en producción (usar wsgi.py + Gunicorn).
"""
from app import create_app

app = create_app()
