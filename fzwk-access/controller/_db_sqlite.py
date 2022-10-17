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
    if row is not None:
        person_id = row['personId']
        if person_id is not None:
            return True, person_id  # might be none if not found
        else:
            return False, None


def log_to_database(message, person_id, badge_id):
    """Insert the given message with the person and badge id as a log entry into the db"""
    current_app.logger.debug(f"Message: {message}, personId: {person_id}, badgeId: {badge_id}")
    cursor = get_db().cursor()
    script = f"""
    INSERT INTO logEntry (personId, badgeId, message)
        VALUES ({person_id}, {badge_id}, "{message}");
    """
    current_app.logger.debug(f'The script is {script}')
    cursor.executescript(script)


def insert_new_badge(badge_id, number: int, first_name, last_name):
    """Insert the given badge into the table as allowed. Also registers the given persn."""
    current_app.logger.debug('Entering _db_sqlite..insert_new_badge()')
    current_app.logger.debug(f'badge_id: {badge_id}, number:{number}, first_name: {first_name}, last_name: {last_name}')
    current_app.logger.debug('*****************************')

    cursor = get_db().cursor()
    script = f"""
    INSERT INTO badge (id,  isAssigned, number) 
        VALUES ({badge_id}, True, {number});
    INSERT INTO person (first_name, last_name) 
        VALUES ("{first_name}", "{last_name}");
    INSERT INTO person_badge VALUES
           ( (SELECT id FROM person WHERE first_name = "{first_name}" AND last_name = "{last_name}"),
            {badge_id});
    """
    current_app.logger.debug(f'The script is: {script}')
    cursor.executescript(script)


def fetch_badges():
    """Returns all badges found in the db"""
    cursor = get_db().cursor()
    # TODO: change this query to fetch currently active badges _with_ the attached person's name
    query = """
    SELECT badge.*, person.* FROM badge, person
    WHERE badge
    """
    result = cursor.execute(query).fetchall()
    result = [dict(row) for row in result]
    current_app.logger.debug(f"Query result is: {result}")
    return result


def fetch_badge_persons():
    """Returns all badges and persons found in the db"""
    cursor = get_db().cursor()
    query = """
    SELECT badge.*, person.* from badge 
    JOIN person_badge ON badge.id = person_badge.badgeId 
    JOIN person ON person_badge.personId = person.id
    """
    current_app.logger.debug(f'Query is: {query}')
    result = cursor.execute(query).fetchall()
    result = [dict(row) for row in result]
    current_app.logger.debug(f'Query result is: {result}')
    return result


def delete_badge(badge_id):
    try:
        con = get_db()
        cursor = con.cursor()
        # Enabling cascade on delete
        # stmt = 'PRAGMA foreign_keys = ON'
        # cursor.execute(stmt)
        # get_db().commit()
        # Deleting from person_badge should suffice because of sql constraints and delete cascading
        query = f'''
        PRAGMA foreign_keys = ON;
        DELETE
        FROM person_badge AS pb
        WHERE pb.badgeId = {badge_id};
        '''
        current_app.logger.debug(f'Query is: {query}')
        cursor.execute(query)
        con.commit()
    except Exception as e:
        current_app.logger.debug(e)
