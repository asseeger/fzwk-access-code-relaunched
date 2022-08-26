from flask import Flask, current_app as app

app = Flask(__name__)

try:
    import RPi.GPIO as Gpio
except ModuleNotFoundError:
    app.logger.debug('RPi-Module not found–we are in dev mode.')


def is_switched_on():
    return g.relay_is_switched_on


def switch_on():
    app.logger.debug('Switching ON')
    if not testing_mode:
        Gpio.output(relay_pin, Gpio.LOW)
    else:
        app.logger.debug('We are in dev mode.')
    db_controller.set_is_relay_switched_on(True)


def switch_off():
    if not testing_mode:
        app.logger.debug('Switching OFF')
        Gpio.output(relay_pin, Gpio.HIGH)
    else:
        app.logger.debug('We are in dev mode.')
    db_controller.set_is_relay_switched_on(False)