from flask import Flask, current_app
from . import db_controller

app = Flask(__name__)

try:
    import RPi.GPIO as Gpio
except ModuleNotFoundError:
    app.logger.debug('RPi-Module not found–we are in dev mode.')
    testing_mode = True
else:
    testing_mode = False
    relay_pin = 16
    Gpio.setmode(Gpio.BCM)
    Gpio.setup(relay_pin, Gpio.OUT)



def is_switched_on():
    return db_controller.get_is_relay_switched_on()


def toggle_switch():
    current_app.logger.debug('toggle_switch()')
    if is_switched_on():
        switch_off()
    else:
        switch_on()


def switch_on():
    app.logger.debug('switch_on(): Switching ON')
    if not testing_mode:
        Gpio.output(relay_pin, Gpio.LOW)
    else:
        app.logger.debug('We are in dev mode.')
    db_controller.set_is_relay_switched_on(True)


def switch_off():
    if not testing_mode:
        app.logger.debug('switch_off(): Switching OFF')
        Gpio.output(relay_pin, Gpio.HIGH)
    else:
        app.logger.debug('We are in dev mode.')
    db_controller.set_is_relay_switched_on(False)


# def toggle_admin_mode