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

def get_all_jobs():
    try:
        connection = get_connection()
        cursor = connection.cursor()
        all_jobs_query = ('SELECT job_id, job_title, company_name, job_type, salary_min, salary_max, '
                          'requirements, job_url, date_posted'
                          'FROM jobs'
                          'INNER JOIN companies ON jobs.company_id = companies.company_id'
                          'ORDER BY job_id, date_posted')

        cursor.execute(all_jobs_query)

        result = cursor.fetchall()

        return result
    
    except Error as error:
        print(f'Error: {error}')

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
