"""
The db controller gives access to the persistent sqlite db
and the dbm key-value store to represent the runtime states.
"""

import sqlite3
import dbm

import click
from flask import current_app, g

_dbm_store = 'dbm_store'
_is_app_loop_running_literal: str = 'is_app_loop_running'
_is_relay_switched_on_literal: str = 'is_relay_switched_on'


def get_is_app_loop_running():
    with dbm.open(_dbm_store) as dbms:
        return eval(dbms.get(_is_app_loop_running_literal))


def set_is_app_loop_running(is_running: bool):
    with dbm.open(_dbm_store, 'c') as dbms:
        dbms[_is_app_loop_running_literal] = str(is_running)

def get_is_relay_switched_on():
    with dbm.open(_dbm_store) as dbms:
        return eval(dbms.get(_is_relay_switched_on_literal))

def set_is_relay_switched_on(is_switched_on: bool):
    with dbm.open(_dbm_store, 'c') as dbms:
        dbms[_is_relay_switched_on_literal] = str(is_switched_on)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
