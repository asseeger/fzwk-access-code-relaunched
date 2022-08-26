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
        return eval(dbms.get(_is_app_loop_running_literal))


def set_is_app_loop_running(is_running: bool):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_is_app_loop_running_literal] = str(is_running)


def get_is_relay_switched_on():
    with dbm.open(_dbm_store_location) as dbms:
        return eval(dbms.get(_is_relay_switched_on_literal))


def set_is_relay_switched_on(is_switched_on: bool):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_is_relay_switched_on_literal] = str(is_switched_on)


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
        is_in_admin_mode = eval(dbms.get(_is_in_admin_mode_literal))
        return is_in_admin_mode


def set_is_in_admin_mode(set_to: bool):
    with dbm.open(_dbm_store_location, 'c') as dbms:
        dbms[_is_in_admin_mode_literal] = str(set_to)


def get_is_in_insert_badge_mode():
    with fetch_dbm() as dbms:
        return eval(dbms.get(_is_in_admin_mode_literal))


def set_is_in_insert_badge_mode(set_to: bool):
    with fetch_dbm() as dbms:
        dbms[_is_in_insert_badge_mode_literal] = str(set_to)
