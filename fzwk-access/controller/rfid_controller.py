from flask import Flask

app = Flask(__name__)

try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    dev_mode = True
    app.logger.debug('RPi-Module not found–we are in dev mode.')
else:
    dev_mode = False
    relay_pin = 16
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)
    from ..resources import SimpleMFRC522
    reader = SimpleMFRC522.SimpleMFRC522()


def read_badge():
    if not dev_mode:
        # return reader.read_id_no_block()
        return reader.read_id()
