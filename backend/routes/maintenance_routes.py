from flask import Blueprint
from backend.controllers.maintenance_controller import scan_for_maintenance, get_maintenance_history
from backend.controllers.receive_controller import receive_from_maintenance

maintenance_routes = Blueprint('maintenance_routes', __name__)

maintenance_routes.add_url_rule('/scan', view_func=scan_for_maintenance, methods=['POST'])
maintenance_routes.add_url_rule('/receive', view_func=receive_from_maintenance, methods=['POST'])
maintenance_routes.add_url_rule('/history', view_func=get_maintenance_history, methods=['GET'])
