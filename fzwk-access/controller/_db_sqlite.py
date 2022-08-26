"""
Factoring out all sqlite statements and queries.
"""

import sqlite3
import click
from flask import current_app, g

# ### Setup ###


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


# ### Statements and Queries ###

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


def insert_new_badge(badge_id, number: int, first_name, last_name):
    """Insert the given badge into the table as allowed. Also registers the given persn."""
    cursor = get_db().cursor()
    script = f"""
    INSERT INTO badge (id,  isAssigned, number) VALUES ({badge_id}, True, {number});
    INSERT INTO person (firstname, lastname) VALUES ("{first_name}", "{last_name}");
    INSERT INTO person_badge VALUES
           ( (SELECT id FROM person WHERE firstname = "{first_name}" AND lastname = "{last_name}"),
            {badge_id});
    """
    current_app.logger.debug(f'The script is: {script}')
    cursor.executescript(script)


def fetch_badges():
    """Returns all badges found in the db"""
    cursor = get_db().cursor()
    query = """
    SELECT * FROM badge
    """
    result = cursor.execute(query).fetchall()
    result = [dict(row) for row in result]
    current_app.logger.debug(f"Query result is: {result}")
    return result
