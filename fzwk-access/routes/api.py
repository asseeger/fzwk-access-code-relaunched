from flask import Blueprint, current_app, render_template, abort, redirect, request, make_response, jsonify
from jinja2 import TemplateNotFound

from ..controller import app_loop_controller, db_controller

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/')
def api_home():
    """Returns just a 204 code for any api consumer to check for a valid connection."""
    return make_response('', 204)

@api_bp.route('/connection')
def api_connection():
    """
    For consumers to check connectivity with server,
    also returns the current status of the run loop.
    """
    # TODO: return the current run_loop_status here.
    is_app_run_loop_running = db_controller.get_is_app_loop_running()
    return make_response(jsonify(runLoopStatus=is_app_run_loop_running), 200)

@api_bp.route('/toggleRunLoop')
def toggleRunLoop():
    app_loop_controller.toggle_app_loop()
    return make_response('', 200)

@api_bp.route('test')
def test():
    person_id = db_controller.is_badge_valid(1571256063040)
    current_app.logger.debug(f'Person Id is:{person_id}')
    return str(person_id)
