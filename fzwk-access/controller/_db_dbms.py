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
    with dbm.open(_dbm_store_location) as dbms:
        is_app_loop_running = (dbms.get(_is_app_loop_running_literal) == 1)
        return is_app_loop_running


def set_is_app_loop_running(is_running: bool):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_is_app_loop_running_literal] = str(is_running)


def get_is_relay_switched_on():
    current_app.logger.debug('get_is_relay_switched_on(): entering')
    with dbm.open(_dbm_store_location) as dbms:
        is_relay_switched_on_string = dbms.get(_is_relay_switched_on_literal)
        current_app.logger.debug(f'get_is_relay_switched_on(): is_relay_switched_on = {is_relay_switched_on_string}')
        is_relay_switched_on = (is_relay_switched_on_string == "b'True'")
        return is_relay_switched_on


def set_is_relay_switched_on(is_switched_on: bool):
    current_app.logger.debug(f'set_is_relay_switched_on({is_switched_on}): entering')
    with dbm.open(_dbm_store_location, 'c') as dbms:
        current_app.logger.debug('writing to dbm')
        is_switched_on_string = str(is_switched_on)
        dbms[_is_relay_switched_on_literal] = is_switched_on_string


def get_current_badge():
    with dbm.open(_dbm_store_location) as dbms:
        return dbms.get(_current_badge_literal)


def set_current_badge(badge_id):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_current_badge_literal] = badge_id


def get_current_person():
    with dbm.open(_dbm_store_location) as dbms:
        return dbms.get(_current_person_literal)


def set_current_person(person_id):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_current_person_literal] = person_id


def get_is_in_admin_mode():
    with dbm.open(_dbm_store_location) as dbms:
        is_in_admin_mode = (dbms.get(_is_in_admin_mode_literal) == 1)
        return is_in_admin_mode


def set_is_in_admin_mode(set_to: bool):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_is_in_admin_mode_literal] = str(set_to)


def get_is_in_insert_badge_mode():
    with fetch_dbm() as dbms:
        _is_in_admin_mode = (dbms.get(_is_in_admin_mode_literal) == 1)
        return _is_in_admin_mode

def set_is_in_insert_badge_mode(set_to: bool):
    with fetch_dbm() as dbms:
        dbms[_is_in_insert_badge_mode_literal] = str(set_to)
