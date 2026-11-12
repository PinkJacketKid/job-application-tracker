import mysql.connector
from mysql.connector import Error

def get_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.1',
            database='job_tracker'
        )

        return connection
    except Error as e:
        print(f'Connection error: {e}')
        return False
