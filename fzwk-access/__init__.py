import os

from flask import Flask
from .routes import api


def create_app(test_config=None):
    from logging.config import dictConfig

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }},
        'root': {
            'leqvel': 'INFO',
            'handlers': ['wsgi']
        }
    })

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'fzwk-access.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # with app.app_context():
    #     from .controller import db_controller
    #     db_controller.init_app(app)


    ### As all attempts to initiate the app loop from here in a consistent way failed,
    ### I am resorting to making a curl call instead upon starting the app:
    ### `curl http://localhost:5001/api/toggleRunLoop`
    # from .controller import app_loop_controller
    # app_loop_controller.start_app_loop()
    # app.logger.debug('Application Start.')

        # from .routes import api
        # api.toggleRunLoop()
        # app.logger.debug('Application Start.')

    app.register_blueprint(api.api_bp)

    app.app_context()

    def cleanup():
        if not test_mode:
            app.logger.debug('Cleanup')
            GPIO.cleanup()

    try:
        import atexit
        import RPi.GPIO as GPIO
        test_mode = False
        atexit.register(cleanup)
    except:
        test_mode = True
    return app
