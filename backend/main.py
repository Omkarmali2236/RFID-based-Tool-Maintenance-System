from flask import Flask, jsonify
from flask_cors import CORS
from backend.routes.tool_routes import tool_routes
from backend.routes.maintenance_routes import maintenance_routes
from backend.routes.receive_routes import receive_routes
from backend.routes.received_routes import received_routes
import os

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return jsonify({"message": "RFID Tool Maintenance API running"})

# ROUTES
app.register_blueprint(tool_routes, url_prefix="/api/tools")
app.register_blueprint(maintenance_routes, url_prefix="/api/maintenance")
app.register_blueprint(receive_routes, url_prefix="/api")  # POST /api/receive
app.register_blueprint(received_routes, url_prefix="/api/received")  # GET /api/received

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
