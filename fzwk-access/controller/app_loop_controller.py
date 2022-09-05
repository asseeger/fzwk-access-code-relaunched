"""
Controller for the App Loop Logic that constantly monitors the RFID-Sensor for changes.
"""
import time
import multiprocessing
from flask import Flask
from . import relay_controller, db_controller, rfid_controller

app = Flask(__name__)
process_name = 'app_loop'


# def has_app_loop_process():
#     processes = multiprocessing.active_children()
#     app.logger.debug('Active processes:')
#     for this_process in processes:
#         app.logger.debug(this_process.name)


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
    # while True:
    #     badge_id = read_badge()
    #     if badge_id is None:
    #         app.logger.debug('No badge present…')
    #         if relay_controller.is_switched_on():
    #             relay_controller.switch_off()
    #             current_badge_id = db_controller.get_current_badge()
    #             current_person_id = db_controller.get_current_person()
    #             db_controller.log_to_database('Badge was removed, switching off.', current_person_id, current_badge_id)
    #     else:
    #         person_id = db_controller.is_badge_valid(badge_id)
    #         if person_id is not None:
    #             db_controller.set_current_badge(badge_id)
    #             db_controller.set_current_person(person_id)
    #             db_controller.log_to_database('Badge was inserted, switching on.', badge_id, person_id)
    #             relay_controller.switch_on()
    #         else:
    #             relay_controller.switch_off()
    #             db_controller.log_to_database('Unknown badge was inserted, switching off.', badge_id, None)
    #     app.logger.debug('')
    #     time.sleep(5)

    while True:
        badge_id = rfid_controller.reader.read_id_no_block()
        if badge_id is None:
            badge_id = rfid_controller.reader.read_id_no_block()
            if badge_id is None:
                app.logger.logToConsole('no chip present')
                if relay_controller.is_switched_on()
                    relay_controller.switch_off()
                    # db_controller.writeToLog('Deactivating.',
                                                 # person=self.currentPerson, badgeId=self.currentBadge)
        else:
            app.logger.logToConsole('Badge id: %i' % badge_id)
            isValid, person = db_controller.is_badge_valid(badge_id)
            if isValid:
                currentBadge = badge_id
                currentPerson = person
                app.logger.logToConsole('Valid: activating')
                # db_controller.writeToLog('Activating.',
                #                              person=self.currentPerson, badgeId=self.currentBadge)
                if not relay_controller.is_switched_on():
                    relay_controller.switch_on()
            else:
                app.logger.logToConsole('Invalid: not activating')
                # self.dbController.writeToLog('Invalid badge: %s.' % (badge_id), badgeId=10000)
                if relay_controller.is_switched_on():
                    relay_controller.switch_off()
        print()
        time.sleep(1)


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


