from flask import Blueprint, current_app, render_template, abort, redirect, request, make_response, jsonify
from jinja2 import TemplateNotFound

from ..controller import app_loop_controller

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

@api_bp.route('/toggleRunLoop')
def toggleRunLoop():
    # TODO: implement toggleRunLoop()
    return make_response('', 200)
