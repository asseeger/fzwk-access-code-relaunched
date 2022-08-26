from flask import Flask, current_app as app
from . import db_controller

app = Flask(__name__)

try:
    import RPi.GPIO as Gpio
except ModuleNotFoundError:
    dev_mode = True
    app.logger.debug('RPi-Module not found–we are in dev mode.')



relay_pin = 16
if not dev_mode:
    Gpio.setup(relay_pin, Gpio.OUT)
    from ..resources import SimpleMFRC522
    reader = SimpleMFRC522.SimpleMFRC522()


def read_badge():
    if not dev_mode:
        return reader.read_id_no_block()
