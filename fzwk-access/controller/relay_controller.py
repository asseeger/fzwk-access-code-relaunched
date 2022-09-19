from flask import Flask
from . import db_controller

app = Flask(__name__)


try:
    import RPi.GPIO as GPIO
except ModuleNotFoundError:
    app.logger.debug('RPi-Module not found–we are in dev mode.')
    testing_mode = True
else:
    app.logger.debug('We are on the RPi!!!')
    testing_mode = False
    relay_pin = 23
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(relay_pin, GPIO.OUT)
    GPIO.output(relay_pin, GPIO.HIGH)


def is_switched_on():
    app.logger.debug('is_switched_on(): entering')
    is_relay_switched_on = db_controller.get_is_relay_switched_on()
    app.logger.debug(f'is_switched_on(): {is_relay_switched_on}')
    return is_relay_switched_on


def toggle_switch():
    app.logger.debug('toggle_switch(): entering')
    if is_switched_on():
        app.logger.debug('toggle_switch(): switching off')
        switch_off()
    else:
        app.logger.debug('toggle_switch(): switching on')

        ###Temp. Solution
        GPIO.output(relay_pin, GPIO.LOW)
        db_controller.set_is_relay_switched_on(True)
        is_relay_switched_on = is_switched_on()
        app.logger.debug(f'is_switched_on(): {is_relay_switched_on}')
        ###

        switch_on()


def switch_on():
    app.logger.debug('switch_on(): Switching ON')
    if not testing_mode:
        GPIO.output(relay_pin, GPIO.LOW)
    else:
        app.logger.debug('switch_on(): Simulating–we are in dev mode.')
    db_controller.set_is_relay_switched_on(True)


def switch_off():
    app.logger.debug('switch_off(): Switching OFF')
    if not testing_mode:
        app.logger.debug('switch_off(): Switching OFF')
        GPIO.output(relay_pin, GPIO.HIGH)
    else:
        app.logger.debug('We are in dev mode.')
    db_controller.set_is_relay_switched_on(False)
