from flask import Blueprint, request, jsonify
from backend.db import get_connection

maintenance_controller = Blueprint('maintenance_controller', __name__)

# SEND TO MAINTENANCE
@maintenance_controller.route('/scan', methods=['POST'])
def scan_for_maintenance():
    try:
        data = request.get_json() or {}
        rfid_uid = (data.get('rfid_uid') or '').strip()
        if not rfid_uid:
            return jsonify({
                'success': False,
                'message': 'RFID UID is required'
            }), 400
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # check tool exists
        cursor.execute("SELECT rfid_uid, tool_name, model_no FROM tools WHERE rfid_uid = %s", (rfid_uid,))
        tool_rows = cursor.fetchall()
        if len(tool_rows) == 0:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Tool not registered'
            }), 404
        # already under maintenance?
        cursor.execute("SELECT rfid_uid FROM maintenance_tools WHERE rfid_uid = %s", (rfid_uid,))
        maint_rows = cursor.fetchall()
        if len(maint_rows) > 0:
            cursor.close()
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Tool already under maintenance'
            }), 409
        # create history row if not open
        cursor.execute("SELECT id FROM received_tools WHERE rfid_uid = %s AND received_date IS NULL", (rfid_uid,))
        history = cursor.fetchall()
        if len(history) == 0:
            cursor.execute(
                "INSERT INTO received_tools (rfid_uid, tool_name, model_no) VALUES (%s, %s, %s)",
                (tool_rows[0]['rfid_uid'], tool_rows[0]['tool_name'], tool_rows[0]['model_no'])
            )
        # insert into active maintenance
        cursor.execute(
            "INSERT INTO maintenance_tools (rfid_uid, tool_name, model_no) VALUES (%s, %s, %s)",
            (tool_rows[0]['rfid_uid'], tool_rows[0]['tool_name'], tool_rows[0]['model_no'])
        )
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'message': 'Tool sent to maintenance successfully'
        })
    except Exception as err:
        print(err)
        return jsonify({
            'success': False,
            'message': 'Server error'
        }), 500

# MAINTENANCE HISTORY
@maintenance_controller.route('/history', methods=['GET'])
def get_maintenance_history():
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT 
                rfid_uid,
                tool_name,
                model_no,
                sent_date,
                received_date
            FROM received_tools
            ORDER BY sent_date DESC
            """
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify({
            'success': True,
            'tools': rows or []
        })
    except Exception as err:
        print(err)
        return jsonify({
            'success': False,
            'tools': []
        }), 500
