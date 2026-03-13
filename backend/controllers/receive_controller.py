from flask import Blueprint, request, jsonify
from backend.db import get_connection

receive_controller = Blueprint('receive_controller', __name__)

@receive_controller.route('/receive', methods=['POST'])
def receive_from_maintenance():
    try:
        data = request.get_json() or {}
        rfid_uid = data.get('rfid_uid')
        if not rfid_uid or not rfid_uid.strip():
            return jsonify({
                'success': False,
                'message': 'RFID is required'
            })
        rfid_uid = rfid_uid.strip()
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Tool MUST be under active maintenance
        cursor.execute("SELECT rfid_uid FROM maintenance_tools WHERE rfid_uid = %s", (rfid_uid,))
        active = cursor.fetchall()
        if len(active) == 0:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Tool is not under maintenance'
            })
        # Close maintenance history
        cursor.execute(
            "UPDATE received_tools SET received_date = NOW() WHERE rfid_uid = %s AND received_date IS NULL",
            (rfid_uid,)
        )
        # Remove from active maintenance
        cursor.execute("DELETE FROM maintenance_tools WHERE rfid_uid = %s", (rfid_uid,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'message': 'Tool received successfully'
        })
    except Exception as error:
        print("Receive error:", error)
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500
