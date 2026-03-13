from flask import Blueprint
from backend.controllers.receive_controller import receive_from_maintenance

receive_routes = Blueprint('receive_routes', __name__)

receive_routes.add_url_rule('/receive', view_func=receive_from_maintenance, methods=['POST'])
