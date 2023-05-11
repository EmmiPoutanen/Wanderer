
from flask import Flask
from flask_login import LoginManager

from website.static.db import db

from .authentication import authentication
from .main import main
from .models import User

def create_app():
    app = Flask(__name__)
    # Dummy secret key since this is test environment
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    db.init_app(app)

    # Route before user is authenticated
    app.register_blueprint(authentication)
    # Route when user is authenticated
    app.register_blueprint(main)

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
