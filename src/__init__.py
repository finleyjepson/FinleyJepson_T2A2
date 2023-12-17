from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()

db = SQLAlchemy()

# Create the Flask application
def create_app():
    app = Flask(__name__)
    jwt = JWTManager(app)

    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')

    db.init_app(app)
    jwt.init_app(app)

    # Error handling 
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Bad Request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'message': 'Unauthorized'}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Not Found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message': 'Internal Server Error'}), 500
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'message': 'Method Not Allowed'}), 405

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .app import app as app_blueprint
    app.register_blueprint(app_blueprint)

    from .cli_bp import cli_bp, init_db_command, seed_db_command, reset_db_command
    app.register_blueprint(cli_bp)
    # Add CLI commands
    with app.app_context():
        app.cli.add_command(init_db_command)
        app.cli.add_command(seed_db_command)
        app.cli.add_command(reset_db_command)

    return app