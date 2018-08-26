import os

from flask import Flask, redirect, url_for


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite')
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed
        app.config.from_mapping(test_config)

    # Insure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register functions with application
    from . import db
    db.init_app(app)

    # Create routes
    @app.route('/hello')
    def hello():
        return "Hello world."

    # @app.route('/')
    # @app.route('/index')
    # def index():
    #     return redirect(url_for('auth.login'))

    # Blueprints - Auth
    from . import auth
    app.register_blueprint(auth.bp)

    # Blueprints - Game (session)
    from . import game
    app.register_blueprint(game.bp)
    app.add_url_rule('/', endpoint='index')

    return app
