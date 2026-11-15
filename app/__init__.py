from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
    db.init_app(app)
    migrate.init_app(app,db)
    from . import models
    from .routes.tasks import tasks_bp
    app.register_blueprint(tasks_bp)
    return app


