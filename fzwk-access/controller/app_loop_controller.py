"""
Controller for the App Loop Logic that constantly monitors the RFID-Sensor for changes.
"""
import time
import multiprocessing
from flask import Flask
from . import relay_controller, db_controller, rfid_controller

app = Flask(__name__)
process_name = 'app_loop'


def start_app_loop():
    process_active = False
    for process in multiprocessing.active_children():
        if process.name == process_name:
            process_active = True
            break
    if not process_active:
        app.logger.debug('Starting the app loop.')
        db_controller.set_is_app_loop_running(True)

        process = multiprocessing.Process(name=process_name, target=app_loop)
        process.start()
    else:
        app.logger.debug('App loop is already running, no need to start again.')


def stop_app_loop():
    app.logger.debug('Stopping the app loop.')
    db_controller.set_is_app_loop_running(False)
    for process in multiprocessing.active_children():
        process.kill()


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
        try:
            badge_id = rfid_controller.reader.read_id_no_block()
            if badge_id is None:
                # Quirk: try again to read–if this is omitted,
                # the relay will flip-flop (de-)activation while a valid chip is present
                badge_id = rfid_controller.reader.read_id_no_block()
                if badge_id is None:
                    if relay_controller.is_switched_on():
                        app.logger.debug('Chip was removed.')
                        relay_controller.switch_off()
                        person_to_deactivate = db_controller.get_current_person()
                        badge_id_to_deactivate = db_controller.get_current_badge()
                        db_controller.log_to_database('Deactivating.', person_to_deactivate, badge_id_to_deactivate)
                    else:
                        app.logger.debug('no chip present')
                else:
                    # This is part II of above mentioned quirk–if a badge was recognized in the prior loop,
                    # this else branch is being walked through with no apparent benefit or disadvantage if
                    # this branch does nothing.
                    #TODO: it seems as though we land in this branch relatively often–
                    # check out why
                    pass
            else:
                app.logger.debug(f'Badge id: {badge_id}')
                is_valid, person_id = db_controller.is_badge_valid(badge_id)
                app.logger.debug(f'The badge is valid: {is_valid}')
                if is_valid:
                    app.logger.debug('Valid: activating')
                    db_controller.log_to_database('Activating.', person_id, badge_id)
                    if not relay_controller.is_switched_on():
                        relay_controller.switch_on()
                else:
                    app.logger.debug('Invalid: not activating')
                    #TODO: this is where I can hook into reading/adding badge mode:
                    # if in add badge mode (dbm)
                    #    store id of this badge in dbm
                    # make this value available through api
                    if relay_controller.is_switched_on():
                        relay_controller.switch_off()
        except Exception as e:
            app.logger.debug(f'The exception {type(e).__name__} was raised in the run-loop: {e}')
        time.sleep(1)


# def app_loop_process_badge(badge_id):
#

def read_badge():
    app.logger.debug('read_badge(): entering')
    badge_id = rfid_controller.read_badge()
    if badge_id is None:
        badge_id = rfid_controller.read_badge()
    app.logger.debug(f'read_badge(): badge_id is {badge_id}')
    if badge_id is None:
        return None
    else:
        return badge_id


def read_badge_mode():
    while True:
        badge_id = read_badge()
        if badge_id is not None:
            db_controller.set_current_badge(badge_id)
        time.sleep(1)


