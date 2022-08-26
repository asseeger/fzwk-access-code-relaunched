import json

from flask import Blueprint, current_app, render_template, abort, redirect, request, make_response, jsonify
from jinja2 import TemplateNotFound

from ..controller import app_loop_controller, db_controller

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/')
def api_home():
    """Returns just a 204 code for any api consumer to check for a valid connection."""
    return make_response('', 204)



def fetch_current_state():
    return {
        'runLoopStatus': bool(db_controller.get_is_app_loop_running()),
        'isInAdminMode': bool(db_controller.get_is_in_admin_mode()),
        'isInInsertBadgeMode': bool(db_controller.get_is_in_insert_badge_mode())
    }


@api_bp.route('/status')
def status():
    """
    For consumers to check connectivity with server,
    also returns the current status of the run loop.
    """
    return make_response(jsonify(fetch_current_state()), 200)


@api_bp.route('/toggleRunLoop')
def toggleRunLoop():
    app_loop_controller.toggle_app_loop()
    return make_response(jsonify(fetch_current_state()), 200)


@api_bp.route('test')
def test():
    person_id = db_controller.is_badge_valid(1571256063040)
    current_app.logger.debug(f'Person Id is:{person_id}')
    return str(person_id)


@api_bp.route('toggleAdminMode')
def toggle_admin_mode():
    if db_controller.get_is_in_admin_mode():
        set_to = False
    else:
        set_to = True
    db_controller.set_is_in_admin_mode(set_to)
    return make_response(jsonify(fetch_current_state()), 200)


@api_bp.route('toggleInsertBadgeMode')
def toggle_insert_badge_mode():
    if db_controller.get_is_in_insert_badge_mode():
        set_to = False
    else:
        set_to = True
    db_controller.set_is_in_insert_badge_mode(set_to)
    return make_response(jsonify(fetch_current_state()), 200)

@api_bp.route('insertBadge', methods=['POST'])
def insert_badge():
    if not db_controller.get_is_in_admin_mode() and not db_controller.get_is_in_insert_badge_mode():
        return make_response('Der Server ist weder im Admin- noch im Badge-Insert-Modus.', 400)
    elif not db_controller.get_is_in_admin_mode():
        return make_response('Der Server ist nicht im Admin-Modus.', 400)
    elif not db_controller.get_is_in_insert_badge_mode():
        return make_response('Der Server ist nicht im Badge-Insert-Modus.', 400)

    content = request.json
    current_app.logger.debug(f"Received json with content: {content}")

    badge_id = content['badgeId']
    first_name = content['firstName']
    last_name = content['lastName']
    number = content['number']

    db_controller.insert_new_badge(badge_id, number, first_name, last_name)
    return make_response('', 204)

@api_bp.route('badge')
def badge():
    current_app.logger.debug(f"Calling /badge")
    content = db_controller.fetch_badges()
    json_content = json.dumps(content)
    current_app.logger.debug(f"Content is: {json_content}")
    return jsonify(content)
