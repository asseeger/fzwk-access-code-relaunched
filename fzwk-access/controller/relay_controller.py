from flask import Flask, current_app as app

app = Flask(__name__)

try:
    import RPi.GPIO as Gpio
except ModuleNotFoundError:
    app.logger.debug('RPi-Module not found–we are in dev mode.')
