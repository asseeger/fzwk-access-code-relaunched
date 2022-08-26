"""
The db controller gives access to the persistent sqlite db
and the dbm key-value store to represent the runtime states.
"""

import sqlite3

import click
from flask import current_app, g
from . import _db_sqlite, _db_dbms


def init_app(app):
    _db_sqlite.init_app(app)


def is_badge_valid(badge_id):
    """Checks whether the given badge has access and returns the badge's person id if it has."""
    cursor = get_db().cursor()
    query = """
            SELECT personId FROM person_badge WHERE badgeId = {}
            """.format(badge_id)
    row = cursor.execute(query).fetchone()
    if row != None:
        person_id = row['personId']
        return person_id  # might be none if not found


# ### dbm access ###


def get_is_app_loop_running():
    return _db_dbms.get_is_app_loop_running()


def set_is_app_loop_running(is_running: bool):
    _db_dbms.set_is_app_loop_running(is_running)


def get_is_relay_switched_on():
    return _db_dbms.get_is_relay_switched_on()


def set_is_relay_switched_on(is_switched_on: bool):
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


def insert_new_badge(badge_id, number: int, first_name, last_name):
    _db_sqlite.insert_new_badge(badge_id, number, first_name, last_name)
