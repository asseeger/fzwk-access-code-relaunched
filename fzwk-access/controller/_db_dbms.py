"""
Factoring out all methods that have to do with the dbm database.
"""

from flask import current_app
import dbm

_dbm_store_location = 'instance/dbm_store'
_is_app_loop_running_literal: str = 'is_app_loop_running'
_is_relay_switched_on_literal: str = 'is_relay_switched_on'
_current_badge_literal: str = 'current_badge'
_current_person_literal: str = 'current_person'
_is_in_admin_mode_literal = 'is_in_admin_mode'
_is_in_insert_badge_mode_literal = '_is_in_insert_badge_mode'


def fetch_dbm():
    return dbm.open(_dbm_store_location, 'c')


def get_is_app_loop_running():
    current_app.logger.debug('get_is_app_loop_running(): entering')
    with dbm.open(_dbm_store_location) as dbms:
        # is_app_loop_running = bool(dbms.get(_is_app_loop_running_literal))
        is_app_loop_running = get_bool_from_key(_is_app_loop_running_literal)
        current_app.logger.debug(f'get_is_app_loop_running(): is_app_loop_running = {is_app_loop_running}')
        return is_app_loop_running


def set_is_app_loop_running(is_running: bool):
    # with dbm.open(_dbm_store_location, 'c') as dbms:
        # dbms[_is_app_loop_running_literal] = str(is_running)
    set_bool_to_key(is_running, _is_app_loop_running_literal)


def get_is_relay_switched_on():
    current_app.logger.debug('get_is_relay_switched_on(): entering')
    # with dbm.open(_dbm_store_location) as dbms:
        # is_relay_switched_on_string = dbms.get(_is_relay_switched_on_literal)
        # is_relay_switched_on_string = get_bool_from_key(_is_relay_switched_on_literal)
        # current_app.logger.debug(f'get_is_relay_switched_on(): is_relay_switched_on_string = {is_relay_switched_on_string}')
        # is_relay_switched_on = bool(is_relay_switched_on_string)
        # current_app.logger.debug(f'get_is_relay_switched_on(): is_relay_switched_on = {is_relay_switched_on_string}')
        # return is_relay_switched_on
    is_relay_switched_on = get_bool_from_key(_is_relay_switched_on_literal)
    return is_relay_switched_on


def set_is_relay_switched_on(is_switched_on: bool):
    current_app.logger.debug(f'set_is_relay_switched_on({is_switched_on}): entering')
    # with dbm.open(_dbm_store_location, 'c') as dbms:
    #     current_app.logger.debug('writing to dbm')
    #     is_switched_on_string = str(is_switched_on)
    #     dbms[_is_relay_switched_on_literal] = is_switched_on_string
    set_bool_to_key(is_switched_on, _is_relay_switched_on_literal)


def get_current_badge():
    current_app.logger.debug('get_current_badge(): entering')
    with dbm.open(_dbm_store_location) as dbms:
        current_badge = dbms.get(_current_badge_literal)
        current_app.logger.debug(f'get_current_badge(): current_badge = {current_badge}')
        return current_badge


def set_current_badge(badge_id):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_current_badge_literal] = badge_id


def get_current_person():
    current_app.logger.debug('get_current_person(): entering')
    with dbm.open(_dbm_store_location) as dbms:
        current_person = dbms.get(_current_person_literal)
        current_app.logger.debug(f'get_current_badge(): current_person = {current_person}')
        return current_person


def set_current_person(person_id):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_current_person_literal] = person_id


def get_is_in_admin_mode():
    current_app.logger.debug('get_is_in_admin_mode(): entering')
    # with dbm.open(_dbm_store_location) as dbms:
    #     is_in_admin_mode = bool(dbms.get(_is_in_admin_mode_literal))
    #     current_app.logger.debug(f'get_is_in_admin_mode(): is_in_admin_mode = {is_in_admin_mode}')
    #     return is_in_admin_mode
    is_in_admin_mode = get_bool_from_key(_is_in_admin_mode_literal)
    return is_in_admin_mode


def set_is_in_admin_mode(set_to: bool):
    current_app.logger.debug(f'set_is_in_admin_mode(set_to: {set_to}): entering')
    # with dbm.open(_dbm_store_location, 'c') as dbms:
    #     dbms[_is_in_admin_mode_literal] = str(set_to)
    set_bool_to_key(set_to, _is_in_admin_mode_literal)


def get_is_in_insert_badge_mode():
    current_app.logger.debug('get_is_in_insert_badge_mode(): entering')
    # with fetch_dbm() as dbms:
    #     is_in_insert_badge_mode = bool(dbms.get(_is_in_insert_badge_mode_literal))
    #     current_app.logger.debug(f'get_is_in_insert_badge_mode(): {is_in_insert_badge_mode}')
    #     return is_in_insert_badge_mode
    is_in_insert_badge_mode = get_bool_from_key(_is_in_insert_badge_mode_literal)
    return is_in_insert_badge_mode


def set_is_in_insert_badge_mode(set_to: bool):
    # with fetch_dbm() as dbms:
    #     dbms[_is_in_insert_badge_mode_literal] = str(set_to)
    set_bool_to_key(set_to, _is_in_insert_badge_mode_literal)


def set_bool_to_key(value: bool, key: str):
    with fetch_dbm() as dbms:
        dbms[key] = str(int(value))


def get_bool_from_key(key: str):
    with fetch_dbm() as dbms:
        try:
            value = bool(int(dbms.get(key)))
        except TypeError:
            value = False
        except NameError:
            value = False
        return value
