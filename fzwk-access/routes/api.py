from flask import current_app as app
from flask import Blueprint, render_template, abort, redirect, request, make_response, jsonify
from jinja2 import TemplateNotFound

api_bp=Blueprint('api', __name__, url_prefix='/api')

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
    return make_response(jsonify(runLoopStatus=True), 200)