import os

from flask import Flask
from .routes import api


def create_app(test_config=None):
    from logging.config import dictConfig

    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] api: %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers':
            {
                'wsgi': {
                    'class': 'logging.StreamHandler',
                    'stream': 'ext://flask.logging.wsgi_errors_stream',
                    'formatter': 'default'
                },
                'custom_handler': {
                    'class': 'logging.FileHandler',
                    'formatter': 'default',
                    'filename': 'app.log'
                }
            },
        'root': {
            'level': 'DEBUG',
            'handlers': ['wsgi', 'custom_handler']
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
    except OSError as e:
        app.logger.debug(e)

    # with app.app_context():
    from .controller import db_controller
    db_controller.init_app(app)
    app.register_blueprint(api.api_bp)
    app.app_context()
    db_controller.reset_cache()



    ### As all attempts to initiate the app loop from here in a consistent way failed,
    ### I am resorting to making a curl call instead upon starting the app:
    ### `curl http://localhost:5001/api/toggleRunLoop`

    #This does not seem to work neither–trying to resolve this by altering the service script
    # import requests
    # app.logger.debug("Starting app loop")
    # response = requests.get('http://localhost:5001/api/toggleRunLoop')
    # app.logger.debug(f'Response on starting app loop: {response}')

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
