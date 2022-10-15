"""
The db controller gives access to the persistent sqlite db
and the dbm key-value store to represent the runtime states.
"""

from flask import Flask, current_app
from . import _db_sqlite, _db_dbms

app = Flask(__name__)


def init_app(app):
    _db_sqlite.init_app(app)


def is_badge_valid(badge_id):
    return _db_sqlite.is_badge_valid(badge_id)


def insert_new_badge(badge_id, number: int, first_name, last_name):
    current_app.logger.debug('Entering db_controller.insert_new_badge()')
    current_app.logger.debug(f'badge_id: {badge_id}, number:{number}, first_name: {first_name}, last_name: {last_name}')
    current_app.logger.debug('*****************************')
    _db_sqlite.insert_new_badge(badge_id, number, first_name, last_name)


def fetch_badges():
    app.logger.debug('Fetch Badges')
    return _db_sqlite.fetch_badges()


def fetch_badge_persons():
    app.logger.debug('Fetch badges and their persons')
    return _db_sqlite.fetch_badge_persons()


def log_to_database(message, person_id, badge_id):
    app.logger.debug(f"Message: {message}, personId: {person_id}, badgeId: {badge_id}")
    _db_sqlite.log_to_database(message, person_id, badge_id)

# ### dbm access ###


def get_is_app_loop_running():
    return _db_dbms.get_is_app_loop_running()


def set_is_app_loop_running(is_running: bool):
    _db_dbms.set_is_app_loop_running(is_running)


def get_is_relay_switched_on():
    return _db_dbms.get_is_relay_switched_on()


def set_is_relay_switched_on(is_switched_on: bool):
    app.logger.debug(f'set_is_relay_switched_on({is_switched_on}): entering')
    _db_dbms.set_is_relay_switched_on(is_switched_on)


def get_current_badge():
    return _db_dbms.get_current_badge()


def set_current_badge(badge_id):
    _db_dbms.set_current_badge(badge_id)


def get_current_person():
    return _db_dbms.get_current_person()


def set_current_person(person_id):
    _db_dbms.set_current_person(person_id)


def get_is_in_admin_mode():
    return _db_dbms.get_is_in_admin_mode()


def set_is_in_admin_mode(set_to: bool):
    _db_dbms.set_is_in_admin_mode(set_to)

def get_is_in_insert_badge_mode():
    return _db_dbms.get_is_in_insert_badge_mode()

def set_is_in_insert_badge_mode(set_to: bool):
    _db_dbms.set_is_in_insert_badge_mode(set_to)
