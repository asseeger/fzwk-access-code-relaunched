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
            'level': 'INFO',
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

    # from flask_caching import Cache
    # config = {
    #     "DEBUG": True,  # some Flask specific configs
    #     "CACHE_TYPE": "SimpleCache",  # Flask-Caching related configs
    #     "CACHE_DEFAULT_TIMEOUT": 300
    # }
    # # app = Flask(__name__)
    # # tell Flask to use the above defined config
    # app.config.from_mapping(config)
    # cache = Cache(app)

    with app.app_context():
        from .controller import db_controller
        db_controller.init_app(app)

        from .controller import app_loop_controller
        app_loop_controller.start_app_loop()
        app.logger.debug('Application Start.')

    ### Testing the relay controller
    # from .controller import relay_controller
    # relay_controller.switch_on()

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
