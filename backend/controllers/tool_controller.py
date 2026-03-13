from flask import Blueprint, request, jsonify
from backend.db import get_connection

# Blueprint will be registered in the main app

tool_controller = Blueprint('tool_controller', __name__)

# REGISTER TOOL (DIRECT + SAFE)
@tool_controller.route('/register', methods=['POST'])
def register_tool():
    try:
        data = request.get_json() or {}
        rfid_uid = data.get('rfid_uid')
        tool_name = data.get('tool_name')
        model_no = data.get('model_no')

        if not rfid_uid or not tool_name:
            return jsonify({
                'success': False,
                'message': 'RFID UID and Tool Name are required'
            })

        rfid_uid = rfid_uid.strip()
        tool_name = tool_name.strip()

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        # RFID must be unique
        cursor.execute("SELECT rfid_uid FROM tools WHERE rfid_uid = %s", (rfid_uid,))
        rfid_exists = cursor.fetchall()
        if len(rfid_exists) > 0:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'message': 'RFID already registered'
            })

        # Handle duplicate tool names (auto suffix)
        final_name = tool_name
        counter = 1
        while True:
            cursor.execute("SELECT tool_name FROM tools WHERE tool_name = %s", (final_name,))
            name_check = cursor.fetchall()
            if len(name_check) == 0:
                break
            final_name = f"{tool_name}{counter}"
            counter += 1

        cursor.execute(
            "INSERT INTO tools (rfid_uid, tool_name, model_no) VALUES (%s, %s, %s)",
            (rfid_uid, final_name, model_no if model_no else None)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            'success': True,
            'message': 'Tool registered successfully'
        })
    except Exception as error:
        print("Register error:", error)
        return jsonify({
            'success': False,
            'message': 'Server error while registering tool'
        }), 500

# AVAILABLE TOOLS (UNCHANGED)
@tool_controller.route('/available', methods=['GET'])
def get_available_tools():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT t.rfid_uid, t.tool_name, t.model_no
            FROM tools t
            LEFT JOIN maintenance_tools m ON t.rfid_uid = m.rfid_uid
            WHERE m.rfid_uid IS NULL
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'tools': rows or []
        })
    except Exception as error:
        print("Available tools error:", error)
        return jsonify({
            'success': False,
            'message': 'Failed to load available tools',
            'tools': []
        }), 500
