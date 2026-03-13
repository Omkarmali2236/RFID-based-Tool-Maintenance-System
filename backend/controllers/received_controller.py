from flask import jsonify
from backend.db import get_connection

def get_received_tools():
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
        print("Received history error:", err)
        return jsonify({
            'success': False,
            'tools': []
        }), 500
