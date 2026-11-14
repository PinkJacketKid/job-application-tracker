import mysql.connector
from mysql.connector import Error
import json

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
        all_jobs_query = ('SELECT job_id, job_title, company_name, job_type, salary_min, salary_max, requirements, job_url, date_posted FROM jobs INNER JOIN companies ON jobs.company_id = companies.company_id ORDER BY job_id, date_posted')

        cursor.execute(all_jobs_query)

        result = cursor.fetchall()
        # Print result is for debugging
        # print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_all_jobs: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_job(job_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        one_job_query = ('SELECT job_id, job_title, company_name, job_type, salary_min, salary_max, requirements, job_url, date_posted FROM jobs INNER JOIN companies ON jobs.company_id = companies.company_id WHERE job_id = %s')

        # For debugging
        # print(job_id)
        # print("job_id type: ", type(job_id))

        job_id_list = [job_id]

        # For debugging
        # print(job_id_list)
        # print("job_id type: ", type(job_id_list))
        
        cursor.execute(one_job_query, job_id_list)

        result = cursor.fetchone()
        # Print result is for debugging
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_job: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def create_job(data):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        requireds = data.get('requirements', '[]')
        if isinstance(requireds, str):
            # Parse comma-separated skills into JSON array
            skills = [s.strip() for s in requireds.split(',') if s.strip()]
            requireds = json.dumps(skills)

        insert_job_query = ("""
                            INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements)
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """)

        cursor.execute(insert_job_query, (data.get('company_id'), data['job_title'], data.get('job_type'),
          data.get('salary_min') or None, data.get('salary_max') or None,
          data.get('job_url'), data.get('date_posted') or None, requireds))

        connection.commit()
    
    except Error as error:
        print(f'Database error in create_job: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def update_job(job_id, data):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        requireds = data.get('requirements', '[]')
        if isinstance(requireds, str):
            # Parse comma-separated skills into JSON array
            skills = [s.strip() for s in requireds.split(',') if s.strip()]
            requireds = json.dumps(skills)

        update_job_query = ("""
                            UPDATE jobs SET company_id=%s, job_title=%s, job_type=%s, salary_min=%s, salary_max=%s,
                            job_url=%s, date_posted=%s, requirements=%s WHERE job_id=%s
                        """)

        cursor.execute(update_job_query, (data.get('company_id'), data['job_title'], data.get('job_type'),
          data.get('salary_min') or None, data.get('salary_max') or None,
          data.get('job_url'), data.get('date_posted') or None, requireds, job_id))

        connection.commit()
    
    except Error as error:
        print(f'Database error in update_job: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def delete_job(job_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        delete_job_query = ('DELETE FROM jobs WHERE job_id = %s')

        # For debugging
        # print(job_id)
        # print("job_id type: ", type(job_id))

        job_id_list = [job_id]

        # For debugging
        # print(job_id_list)
        #print("job_id type: ", type(job_id_list))

        cursor.execute(delete_job_query, job_id_list)

        connection.commit()
    
    except Error as error:
        print(f'Database error in delete_job: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_all_companies():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        all_companies_query = ('SELECT * FROM companies ORDER BY company_id, company_name')

        cursor.execute(all_companies_query)

        result = cursor.fetchall()
        # Print result is for debugging
        # print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_all_companies: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()