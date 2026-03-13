from flask import Blueprint
from backend.controllers.tool_controller import register_tool, get_available_tools

# This blueprint is for registering routes, not logic

tool_routes = Blueprint('tool_routes', __name__)

tool_routes.add_url_rule('/register', view_func=register_tool, methods=['POST'])
tool_routes.add_url_rule('/available', view_func=get_available_tools, methods=['GET'])
