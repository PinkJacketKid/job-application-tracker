import mysql.connector
from mysql.connector import Error

def get_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(
            user='root',
            password='root',
            host='127.0.0.2',
            database='job_tracker_project'
        )

        return connection
    except Error as e:
        print(f'Connection error: {e}')
        return False

def get_all_jobs():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        all_jobs_query = ('SELECT jobs.job_id, jobs.job_title, companies.company_name, jobs.job_type, jobs.salary_min, jobs.salary_max, jobs.requirements, jobs.job_url, jobs.date_posted FROM jobs INNER JOIN companies ON jobs.company_id = companies.company_id ORDER BY jobs.job_id, jobs.date_posted')

        cursor.execute(all_jobs_query)

        result = cursor.fetchall()
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_all_jobs: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()
