from flask import Flask, current_app as app
from . import db_controller

app = Flask(__name__)

try:
    import RPi.GPIO as Gpio
except ModuleNotFoundError:
    app.logger.debug('RPi-Module not found–we are in dev mode.')


def is_switched_on():
    return db_controller.get_is_relay_switched_on()


def toggle_switch():
    if is_switched_on():
        switch_off()
    else:
        switch_on()


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


# def toggle_admin_mode