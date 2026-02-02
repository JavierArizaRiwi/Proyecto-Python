from dataclasses import dataclass
import os
from dotenv import load_dotenv

# --- Configuration Management ---
# Seguimos el principio "Store config in the environment" (The Twelve-Factor App).
# Esto permite desplegar la misma imagen Docker en Dev, Staging y Prod,
# cambiando solo las variables de entorno.

@dataclass(frozen=True)
class Settings:
    """
    Contenedor inmutable para la configuración de la aplicación.
    frozen=True asegura que la configuración no cambie durante la ejecución (Thread-Safety).
    """
    flask_env: str
    app_name: str
    log_level: str
    secret_key: str
    port: int

    @staticmethod
    def from_env() -> "Settings":
        """Factory method que carga variables desde .env y el sistema."""
        load_dotenv(override=False)

        flask_env = os.getenv("FLASK_ENV", "development")
        app_name = os.getenv("APP_NAME", "miapp-flask")
        log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        secret_key = os.getenv("SECRET_KEY", "change-me")

        port_raw = os.getenv("PORT", "8000")
        try:
            port = int(port_raw)
        except ValueError:
            port = 8000

        return Settings(
            flask_env=flask_env,
            app_name=app_name,
            log_level=log_level,
            secret_key=secret_key,
            port=port,
        )
