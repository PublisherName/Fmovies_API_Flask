''' This file contains the error handlers for the application. '''

from flask import Blueprint, jsonify

errors_bp = Blueprint('errors', __name__)


@errors_bp.app_errorhandler(500)
@errors_bp.app_errorhandler(400)
@errors_bp.app_errorhandler(404)
def handle_not_found_error(error):
    '''Return a error.'''
    return jsonify(error=str(error)), error.code
