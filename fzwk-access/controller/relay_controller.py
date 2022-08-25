from flask import Flask, current_app as app

app = Flask(__name__)

class RelayController(object):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if RelayController.__instance is None:
            RelayController.__instance = object.__new__(cls)
            try:
                import RPi.GPIO as Gpio
            except ModuleNotFoundError:
                app.logger.debug('RPi-Module not found–we are in dev mode.')
