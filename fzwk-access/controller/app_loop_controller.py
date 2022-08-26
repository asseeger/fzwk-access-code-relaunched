from flask import Flask, current_app
from . import relay_controller, db_controller

app = Flask(__name__)


def start_app_loop():
    app.logger.debug('Starting the app loop.')
    db_controller.set_is_app_loop_running(True)
    # TODO: implement start_app_loop()


def stop_app_loop():
    app.logger.debug('Stopping the app loop.')
    db_controller.set_is_app_loop_running(False)
    # TODO: implement stop_app_loop()


def toggle_app_loop():
    app.logger.debug('Toggling the app loop.')
    if db_controller.get_is_app_loop_running():
        stop_app_loop()
    else:
        start_app_loop()


def enter_admin_mode():
    """Entering a mode to read in a badge that is currently not registered in order to connect it with a person."""
    app.logger.debug('Entering admin mode.')
    # TODO: start reading in badges that get connected
