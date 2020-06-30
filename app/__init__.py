import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException


# instantiate extensions
login_manager = LoginManager()
db = SQLAlchemy()


def create_app(environment="development"):

    from config import config
    from app.views import main_blueprint
    from app.auth.views import auth_blueprint
    from app.auth.models import User, AnonymousUser
    from app.exam.views import exam_blueprint
    from app.dashboard.views import dashboard_blueprint

    # Instantiate app.
    app = Flask(__name__)

    # Set app config.
    env = os.environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    config[env].configure(app)

    # Set up extensions.
    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints.
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(exam_blueprint)
    app.register_blueprint(dashboard_blueprint)

    # Set up flask login.
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"
    login_manager.anonymous_user = AnonymousUser

    # user_manager = UserManager(app, db, User)
    # user_manager.USER_UNAUTHORIZED_ENDPOINT = "main.index"  # TODO: rethink of it

    # Error handlers.
    @app.errorhandler(HTTPException)
    def handle_http_error(exc):
        return render_template("error.html", error=exc), exc.code

    return app
