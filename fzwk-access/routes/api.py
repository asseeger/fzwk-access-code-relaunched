import json

from flask import Blueprint, current_app, render_template, abort, redirect, request, make_response, jsonify
from jinja2 import TemplateNotFound

from ..controller import app_loop_controller, db_controller, relay_controller

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/')
def api_home():
    """Returns just a 204 code for any api consumer to check for a valid connection."""
    return make_response('', 204)


def fetch_current_state():
    current_app.logger.debug('fetch_current_state(): entering')
    is_relay_switched_on = bool(db_controller.get_is_relay_switched_on())
    current_app.logger.debug(f'is_switched_on: {is_relay_switched_on}')
    return {
        'runLoopStatus': bool(db_controller.get_is_app_loop_running()),
        'isInAdminMode': bool(db_controller.get_is_in_admin_mode()),
        'isInInsertBadgeMode': bool(db_controller.get_is_in_insert_badge_mode()),
        'isRelaySwitchedOn': is_relay_switched_on
    }


@api_bp.route('/status')
def status():
    """
    For consumers to check connectivity with server,
    also returns the current status of the run loop.
    """
    current_app.logger.debug('entering')
    current_state = fetch_current_state()
    current_app.logger.debug(current_state)
    return make_response(jsonify(current_state), 200)


@api_bp.route('/toggleRunLoop')
def toggle_run_loop():
    app_loop_controller.toggle_app_loop()
    return make_response(jsonify(fetch_current_state()), 200)


@api_bp.route('test', methods=['POST'])
def test():
    content = request.json
    current_app.logger.debug(f"Received json with content: {content}")

    message = content['message']
    person_id = content['personId']
    badge_id = content['badgeId']
    current_app.logger.debug(f"Message: {message}, personId: {person_id}, badgeId: {badge_id}")

    db_controller.log_to_database(message, person_id, badge_id)

    return  make_response('', 204)


@api_bp.route('toggleAdminMode')
def toggle_admin_mode():
    current_app.logger.debug('toggle_admin_mode(): entering')
    is_in_admin_mode = db_controller.get_is_in_admin_mode()
    current_app.logger.debug(f'toggle_admin_mode(): is_in_admin_mode = {is_in_admin_mode}')
    if is_in_admin_mode:
        db_controller.set_is_in_admin_mode(False)
    else:
        db_controller.set_is_in_admin_mode(True)
    current_app.logger.debug('toggle_admin_mode(): exiting')
    current_app.logger.debug('****************************')

    # Resetting insert badge mode in case the admin mode was not switched off properly before
    db_controller.set_is_in_insert_badge_mode(False)
    return make_response(jsonify(fetch_current_state()), 200)


@api_bp.route('toggleRelaySwitch')
def toggle_relay_is_switched_on():
    current_app.logger.debug('Entering')
    relay_controller.toggle_switch()
    return make_response(jsonify(fetch_current_state()), 200)


@api_bp.route('toggleInsertBadgeMode')
def toggle_insert_badge_mode():
    if db_controller.get_is_in_insert_badge_mode():
        set_to = False
    else:
        set_to = True
    db_controller.set_is_in_insert_badge_mode(set_to)
    current_app.logger.debug(f'Is in insert_badge_mode: {db_controller.get_is_in_insert_badge_mode()}')
    return make_response(jsonify(fetch_current_state()), 200)


@api_bp.route('insertBadgePerson', methods=['POST'])
def insert_badge_person():
    current_app.logger.debug('insert_badge_person(): Entering')
    try:
        content = request.json
        current_app.logger.debug(f"Received json with content: {content}")
        if not db_controller.get_is_in_admin_mode() and not db_controller.get_is_in_insert_badge_mode():
            message = 'Der Server ist weder im Admin- noch im Badge-Insert-Modus.'
            current_app.logger.debug(message)
            return make_response(message, 400)
        elif not db_controller.get_is_in_admin_mode():
            message = 'Der Server ist nicht im Admin-Modus.'
            current_app.logger.debug(message)
            return make_response(message, 400)
        elif not db_controller.get_is_in_insert_badge_mode():
            message = 'Der Server ist nicht im Badge-Insert-Modus.'
            current_app.logger.debug(message)
            return make_response(message, 400)

        badge_id = content['id']
        number = content['number']
        first_name = content['first_name']
        last_name = content['last_name']
        current_app.logger.debug(f'badge_id: {badge_id}, number:{number}, first_name: {first_name}, last_name: {last_name}')

        db_controller.insert_new_badge(badge_id, number, first_name, last_name)
        toggle_insert_badge_mode()
        return make_response('', 204)
    except Exception as e:
        message = f'There was an error: {e}'
        current_app.logger.debug(message)
        current_app.logger.debug(request.headers)
        return make_response(message, 400)

@api_bp.route('/badg<path:suffix>', methods = ['POST', 'GET', 'DELETE'])
def badge(suffix):
    """
    Implements the /badge* family
    :param suffix: the suffix to /badge
    :return: json response with according http code
    """
    current_app.logger.debug(f'Suffix is {suffix}')
    current_app.logger.debug(f"Calling /badg{suffix}")
    current_app.logger.debug(f"Request content is: {request.json}")
    if suffix == 'es':
        content = db_controller.fetch_badges()
        current_app.logger.debug(f"Response content is: {json.dumps(content)}")
        return jsonify(content)
    elif suffix == 'e':
        if request.method == 'GET':
            current_badge = db_controller.get_current_badge()
            current_app.logger.debug(f'Current badge is: {current_badge}')
            response = {
                "current_badge": current_badge
            }
            return make_response(jsonify(response), 200)
        elif request.method == 'DELETE':
            badge_id = request.json['id']
            db_controller.delete_badge(badge_id)
            return make_response('', 204)
    else:
        return make_response(f'Route /badge{suffix} is not implemented.', 404)


@api_bp.route('/badgePersons')
def badge_persons():
    try:
        current_app.logger.debug('Calling /badgePersons')
        content = db_controller.fetch_badge_persons()
        current_app.logger.debug(f"Content is: {json.dumps(content)}")
        return make_response(jsonify(content), 200)
    except Exception as e:
        message = f'There was an error: {e}'
        current_app.logger.debug(message)
        current_app.logger.debug(request.headers)
        return make_response(message, 400)