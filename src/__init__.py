from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    jwt = JWTManager(app)

    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

    db.init_app(app)
    jwt.init_app(app)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .app import app as app_blueprint
    app.register_blueprint(app_blueprint)

    from .cli_bp import cli_bp, init_db_command, seed_db_command
    app.register_blueprint(cli_bp)
    with app.app_context():
        app.cli.add_command(init_db_command)
        app.cli.add_command(seed_db_command)

    return app