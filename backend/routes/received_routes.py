from flask import Blueprint
from backend.controllers.received_controller import get_received_tools

received_routes = Blueprint('received_routes', __name__)

received_routes.add_url_rule('/', view_func=get_received_tools, methods=['GET'])
