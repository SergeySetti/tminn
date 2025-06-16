import time

from dotenv import load_dotenv
from flask import Flask
from flask_injector import FlaskInjector

from app.config import Config
from app.services.service import AppModule


def create_app(config_class=Config):
    load_dotenv()

    Flask.url_for.__annotations__ = {}
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    # add templates global variables
    app.jinja_env.globals.update(
        app_name=app.config,
        current_year=time.strftime('%Y')
    )

    # Configure dependency injection

    FlaskInjector(app=app, modules=[AppModule])

    return app
