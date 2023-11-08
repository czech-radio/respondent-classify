import flask
import os
from service.routes import main_bp


class Configuration:
    # Korektor external service.
    @property
    def KOREKTOR_SERVICE_URL(self):
        host = os.getenv("KOREKTOR_HOST") or "localhost"
        port = os.getenv("KOREKTOR_PORT") or 8000
        return f"{host}:{port}"

    # Morphodita external service.
    @property
    def MORPHODITA_SERVICE_URL(self):
        host = os.getenv("MOTPHODITA_HOST") or "localhost"
        port = os.getenv("MOTPHODITA_PORT") or 3000
        return f"{host}:{port}"


def create_app(config=None):
    """
    Create and configure Flask application.
    """
    app = flask.Flask(f"{__name__}")

    # Register blueprintes (routers).
    app.register_blueprint(blueprint=main_bp, url_prefix="/")

    # Configure application server.
    app.config.from_object(Configuration())

    return app
