"""
Factoring out all methods that have to do with the dbm database.
"""

from flask import Flask, current_app
import dbm

app = Flask(__name__)

_dbm_store_location = 'instance/dbm_store'
_is_app_loop_running_literal: str = 'is_app_loop_running'
_is_relay_switched_on_literal: str = 'is_relay_switched_on'
_current_badge_literal: str = 'current_badge'
_current_person_literal: str = 'current_person'
_is_in_admin_mode_literal = 'is_in_admin_mode'
_is_in_insert_badge_mode_literal = '_is_in_insert_badge_mode'


def fetch_dbm():
    return dbm.open(_dbm_store_location, 'c')


def reset_cache():
    """Resets the app's status informations stored in dbm"""
    set_is_app_loop_running(False)
    set_is_relay_switched_on(False)
    set_is_in_admin_mode(False)
    set_is_in_insert_badge_mode(False)


def get_is_app_loop_running():
    app.logger.debug('get_is_app_loop_running(): entering')
    with dbm.open(_dbm_store_location) as dbms:
        is_app_loop_running = get_bool_from_key(_is_app_loop_running_literal)
        app.logger.debug(f'get_is_app_loop_running(): is_app_loop_running = {is_app_loop_running}')
        return is_app_loop_running


def set_is_app_loop_running(is_running: bool):
    set_bool_to_key(is_running, _is_app_loop_running_literal)


def get_is_relay_switched_on():
    is_relay_switched_on = get_bool_from_key(_is_relay_switched_on_literal)
    return is_relay_switched_on


def set_is_relay_switched_on(is_switched_on: bool):
    app.logger.debug(f'set_is_relay_switched_on({is_switched_on}): entering')
    set_bool_to_key(is_switched_on, _is_relay_switched_on_literal)


def get_current_badge():
    app.logger.debug('get_current_badge(): entering')
    with dbm.open(_dbm_store_location) as dbms:
        current_badge = int(dbms.get(_current_badge_literal))
        app.logger.debug(f'get_current_badge(): current_badge = {current_badge}')
        return current_badge


def set_current_badge(badge_id):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_current_badge_literal] = str(badge_id)


def get_current_person():
    app.logger.debug('get_current_person(): entering')
    with dbm.open(_dbm_store_location) as dbms:
        current_person = int(dbms.get(_current_person_literal))
        app.logger.debug(f'get_current_badge(): current_person = {current_person}')
        return current_person


def set_current_person(person_id):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_current_person_literal] = str(person_id)


def get_is_in_admin_mode():
    app.logger.debug('get_is_in_admin_mode(): entering')
    is_in_admin_mode = get_bool_from_key(_is_in_admin_mode_literal)
    return is_in_admin_mode


def set_is_in_admin_mode(set_to: bool):
    app.logger.debug(f'set_is_in_admin_mode(set_to: {set_to}): entering')
    set_bool_to_key(set_to, _is_in_admin_mode_literal)


def get_is_in_insert_badge_mode():
    app.logger.debug('get_is_in_insert_badge_mode(): entering')
    is_in_insert_badge_mode = get_bool_from_key(_is_in_insert_badge_mode_literal)
    return is_in_insert_badge_mode


def set_is_in_insert_badge_mode(set_to: bool):
    set_bool_to_key(set_to, _is_in_insert_badge_mode_literal)


def set_bool_to_key(value: bool, key: str):
    with fetch_dbm() as dbms:
        dbms[key] = str(int(value))


def get_bool_from_key(key: str):
    with fetch_dbm() as dbms:
        try:
            value_from_dbms = dbms.get(key)
            # app.logger.debug(f'get_bool_from_key({key}): {value_from_dbms}')
            value_in_int = int(value_from_dbms)
            # app.logger.debug(f'get_bool_from_key({key}): {value_in_int}')
            value_in_bool = bool(value_in_int)
            # app.logger.debug(f'get_bool_from_key({key}): {value_in_bool}')
            value = value_in_bool
        except TypeError:
            value = False
        except NameError:
            value = False
        return value
