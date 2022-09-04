from flask import current_app
from . import db_controller


try:
    import RPi.GPIO as Gpio
except ModuleNotFoundError:
    # current_app.logger.debug('RPi-Module not found–we are in dev mode.')
    testing_mode = True
else:
    # current_app.logger.debug('We are on the RPi!!!')
    testing_mode = False
    relay_pin = 16
    Gpio.setmode(Gpio.BCM)
    Gpio.setup(relay_pin, Gpio.OUT)


def is_switched_on():
    current_app.logger.debug('is_switched_on(): entering')
    is_relay_switched_on = db_controller.get_is_relay_switched_on()
    current_app.logger.debug(f'is_switched_on(): {is_relay_switched_on}')
    return is_relay_switched_on


def toggle_switch():
    current_app.logger.debug('toggle_switch(): entering')
    if is_switched_on():
        current_app.logger.debug('toggle_switch(): switching off')
        switch_off()
    else:
        current_app.logger.debug('toggle_switch(): switching on')

        ###Temp. Solution
        Gpio.output(relay_pin, Gpio.LOW)
        db_controller.set_is_relay_switched_on(True)
        is_relay_switched_on = is_switched_on()
        current_app.logger.debug(f'is_switched_on(): {is_relay_switched_on}')
        ###

        switch_on()


def switch_on():
    current_app.logger.debug('switch_on(): Switching ON')
    if not testing_mode:
        Gpio.output(relay_pin, Gpio.LOW)
    else:
        current_app.logger.debug('We are in dev mode.')
    db_controller.set_is_relay_switched_on(True)


def switch_off():
    current_app.logger.debug('switch_off(): Switching OFF')
    if not testing_mode:
        current_app.logger.debug('switch_off(): Switching OFF')
        Gpio.output(relay_pin, Gpio.HIGH)
    else:
        current_app.logger.debug('We are in dev mode.')
    db_controller.set_is_relay_switched_on(False)


# def toggle_admin_mode