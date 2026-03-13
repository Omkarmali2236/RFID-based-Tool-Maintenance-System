import os
from dotenv import load_dotenv
load_dotenv()
import mysql.connector
from mysql.connector import pooling

# Load environment variables (Flask will typically use python-dotenv or similar)
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', '127.0.0.1'),
    'port': int(os.environ.get('DB_PORT', 3306)),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_NAME'),
}

# Create a connection pool (similar to mysql2's createPool)
pool = pooling.MySQLConnectionPool(
    pool_name="rfid_pool",
    pool_size=5,
    **DB_CONFIG
)

def get_connection():
    return pool.get_connection()
