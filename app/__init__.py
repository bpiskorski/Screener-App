from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate 

migrate = Migrate() 

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Load configuration from config.py

    # Initialize database
    db.init_app(app)
    migrate.init_app(app, db)

    # Register routes
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    return app