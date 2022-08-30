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


def toggle_admin_mode():
    """Entering a mode to read in a badge that is currently not registered in order to connect it with a person."""
    app.logger.debug('Entering admin mode.')
    if db_controller.get_is_app_loop_running():
        stop_app_loop()


def app_loop():
    while True:
        badge_id = read_badge()
        if badge_id is None:
            if relay_controller.is_switched_on():
                relay_controller.switch_off()
                current_badge_id = db_controller.get_current_badge()
                current_person_id = db_controller.get_current_person()
                db_controller.log_to_database('Badge was removed, switching off.', current_person_id, current_badge_id)
        else:
            person_id = db_controller.is_badge_valid(badge_id)
            if person_id is not None:
                db_controller.set_current_badge(badge_id)
                db_controller.set_current_person(person_id)
                db_controller.log_to_database('Badge was inserted, switching on.', badge_id, person_id)
                relay_controller.switch_on()
            else:
                relay_controller.switch_off()
                db_controller.log_to_database('Unknown badge was inserted, switching off.', badge_id, None)
        time.sleep(1)



def read_badge():
    badge_id = rfid_controller.read_badge()
    if badge_id is None:
        app.logger.debug('No chip present.')
        return None
    else:
        return badge_id


def read_badge_mode():
    while True:
        badge_id = read_badge()
        if badge_id is not None:
            db_controller.set_current_badge(badge_id)
        time.sleep(1)


