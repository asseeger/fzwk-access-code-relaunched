"""
Controller for the App Loop Logic that constantly monitors the RFID-Sensor for changes.
"""
import time

from flask import Flask, current_app
import multiprocessing
from . import relay_controller, db_controller, rfid_controller

app = Flask(__name__)

process = None


def start_app_loop():
    app.logger.debug('Starting the app loop.')
    db_controller.set_is_app_loop_running(True)
    # TODO: implement start_app_loop()


def stop_app_loop():
    app.logger.debug('Stopping the app loop.')
    db_controller.set_is_app_loop_running(False)
    # TODO: implement stop_app_loop()


def toggle_app_loop():
    app.logger.debug('Toggling the app loop.')
    if db_controller.get_is_app_loop_running():
        stop_app_loop()
    else:
        start_app_loop()


def enter_admin_mode():
    """Entering a mode to read in a badge that is currently not registered in order to connect it with a person."""
    app.logger.debug('Entering admin mode.')
    # TODO: start reading in badges that get connected


def app_loop():
    while True:
        badge_id = rfid_controller.read_badge()
        if badge_id == None:
            app.logger.debug('No chip present.')
            if relay_controller.is_switched_on():
                relay_controller.switch_off()
                # TODO: write **db** log that badge was removed (person stopped using the machine)
        else:
            person_id = db_controller.is_badge_valid(badge_id)
            if person_id != None:
                db_controller.set_current_badge(badge_id)
                db_controller.set_current_person(person_id)
                # TODO: write **db** log that badge was inserted with badge_id and person_id, activating the machine.
                relay_controller.switch_on()
            else:
                relay_controller.switch_off()
        time.sleep(1)
