
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from website.static.db import db

from .main import main
from .authentication import authentication
from .models import User

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)

    app.register_blueprint(main)
    app.register_blueprint(authentication)

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = "authentication.login"
    login_manager.init_app(app)

    # Flask login requires method for laoding current user
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
