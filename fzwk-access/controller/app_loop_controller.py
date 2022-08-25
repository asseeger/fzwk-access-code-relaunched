from flask import Flask, current_app as app
from . import relay_controller

app = Flask(__name__)

class AppLoopController(object):
    __instance = None
    _isRunning = None
    relay_controller = relay_controller.RelayController()

    def __new__(cls, *args, **kwargs):
        if AppLoopController.__instance is None:
            app.logger.debug('Instantiating.')
            AppLoopController.__instance = object.__new__(cls)
            AppLoopController.__instance.start_app_loop()
        return AppLoopController.__instance

    def start_app_loop(self):
        with app.app_context():
            app.logger.debug('Starting the app loop.')
        self._isRunning = True
        # TODO: implement start_app_loop()

    def stop_app_loop(self):
        app.logger.debug('Stopping the app loop.')
        self._isRunning = False
        # TODO: implement stop_app_loop()

    def toggle_app_loop(self):
        app.logger.debug('Toggling the app loop.')
        if self._isRunning:
            self.stop_app_loop()
        else:
            self.start_app_loop()

    def enter_admin_mode(self):
        """Entering a mode to read in a badge that is currently not registered in order to connect it with a person."""
        app.logger.debug('Entering admin mode.')
        # TODO: start reading in badges that get connected
