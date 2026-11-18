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

# Jobs CRUD functions
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
            return None

        cursor = connection.cursor(dictionary=True)
        one_job_query = ("""SELECT job_id, jobs.company_id, job_title, company_name, job_type, salary_min, salary_max, requirements, job_url, date_posted FROM jobs INNER JOIN companies ON jobs.company_id = companies.company_id WHERE job_id = %s""")

        # For debugging
        # print(job_id)
        # print("job_id type: ", type(job_id))

        job_id_list = [job_id]

        # For debugging
        # print(job_id_list)
        # print("job_id_list type: ", type(job_id_list))

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
        #print("job_id_list type: ", type(job_id_list))

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

# Companies CRUD functions
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

def get_company(company_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        one_company_query = ('SELECT * FROM companies WHERE company_id = %s')

        # For debugging
        # print(company_id)
        # print("company_id type: ", type(company_id))

        company_id_list = [company_id]

        # For debugging
        # print(company_id_list)
        # print("company_id_list type: ", type(company_id_list))

        cursor.execute(one_company_query, company_id_list)

        result = cursor.fetchone()
        # Print result is for debugging
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_company: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def create_company(data):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        insert_company_query = ("""
                            INSERT INTO companies (company_name, industry, website, city, state, notes)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """)

        cursor.execute(insert_company_query, (data['company_name'], data.get('industry'),
          data.get('website') or None, data.get('city'),
          data.get('state'), data.get('notes') or None))

        connection.commit()
    
    except Error as error:
        print(f'Database error in create_company: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def update_company(company_id, data):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        update_company_query = ("""
                            UPDATE companies SET company_name=%s, industry=%s, website=%s, city=%s,
                            state=%s, notes=%s WHERE company_id=%s
                        """)

        cursor.execute(update_company_query, (data['company_name'], data.get('industry'),
          data.get('website') or None, data.get('city'),
          data.get('state'), data.get('notes') or None, company_id))

        connection.commit()
    
    except Error as error:
        print(f'Database error in update_company: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def delete_company(company_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        delete_company_query = ('DELETE FROM companies WHERE company_id = %s')

        # For debugging
        # print(company_id)
        # print("company_id type: ", type(company_id))

        company_id_list = [company_id]

        # For debugging
        # print(job_id_list)
        #print("job_id_list type: ", type(job_id_list))

        cursor.execute(delete_company_query, company_id_list)

        connection.commit()
    
    except Error as error:
        print(f'Database error in delete_company: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

# Applications CRUD Functions
def get_all_applications():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        all_applications_query = ('SELECT a.*, j.job_title, c.company_name FROM applications a LEFT JOIN jobs j ON a.job_id = j.job_id LEFT JOIN companies c ON j.company_id = c.company_id ORDER BY a.application_id, a.application_date')

        cursor.execute(all_applications_query)

        result = cursor.fetchall()
        # Print result is for debugging
        # print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_all_applications: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_application(application_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        one_application_query = ('SELECT a.*, j.job_title, c.company_name FROM applications a LEFT JOIN jobs j ON a.job_id = j.job_id LEFT JOIN companies c ON j.company_id = c.company_id WHERE application_id = %s')

        # For debugging
        # print(application_id)
        # print("application_id type: ", type(application_id))

        application_id_list = [application_id]

        # For debugging
        # print(application_id_list)
        # print("application_id_list type: ", type(application_id_list))

        cursor.execute(one_application_query, application_id_list)

        result = cursor.fetchone()
        # Print result is for debugging
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_application: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def create_application(data):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        interview = data.get('interview_data', '{}')
        if isinstance(interview, str) and interview:
            try:
                json.loads(interview)
            except:
                interview = json.dumps({"notes": interview})
        elif not interview:
            interview = None

        insert_application_query = ("""
                            INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data)
                            VALUES (%s, %s, %s, %s, %s, %s)
                        """)

        cursor.execute(insert_application_query, (data.get('job_id'), data['application_date'], data.get('status'),
          data.get('resume_version') or None, bool(data.get('cover_letter_sent')), interview))

        connection.commit()
    
    except Error as error:
        print(f'Database error in create_application: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def update_application(application_id, data):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        interview = data.get('interview_data', '{}')
        if isinstance(interview, str) and interview:
            try:
                json.loads(interview)
            except:
                interview = json.dumps({"notes": interview})
        elif not interview:
            interview = None

        update_application_query = ("""
                            UPDATE applications SET job_id=%s, application_date=%s, status=%s, resume_version=%s,
                                cover_letter_sent=%s, interview_data=%s WHERE application_id=%s
                        """)

        cursor.execute(update_application_query, (data.get('job_id'), data['application_date'], data.get('status'),
          data.get('resume_version') or None, bool(data.get('cover_letter_sent')), interview, application_id))

        connection.commit()
    
    except Error as error:
        print(f'Database error in update_application: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def delete_application(application_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        delete_application_query = ('DELETE FROM applications WHERE application_id = %s')

        # For debugging
        # print(application_id)
        # print("application_id type: ", type(application_id))

        application_id_list = [application_id]

        # For debugging
        # print(application_id_list)
        #print("application_id_list type: ", type(application_id_list))

        cursor.execute(delete_application_query, application_id_list)

        connection.commit()
    
    except Error as error:
        print(f'Database error in delete_application: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

# Contacts CRUD functions
def get_all_contacts():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        all_contacts_query = ('SELECT contact_id, contact_name, title, company_name, email, phone, linkedin_url, contacts.notes FROM contacts INNER JOIN companies ON contacts.company_id = companies.company_id ORDER BY contact_id, contact_name')

        cursor.execute(all_contacts_query)

        result = cursor.fetchall()
        # Print result is for debugging
        # print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_all_contacts: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_contact(contact_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        one_contact_query = ('SELECT contact_id, contacts.company_id, contact_name, title, company_name, email, phone, linkedin_url, contacts.notes FROM contacts INNER JOIN companies ON contacts.company_id = companies.company_id WHERE contact_id = %s')

        # For debugging
        # print(contact_id)
        # print("contact_id type: ", type(contact_id))

        contact_id_list = [contact_id]

        # For debugging
        # print(contact_id_list)
        # print("contact_id_list type: ", type(contact_id_list))

        cursor.execute(one_contact_query, contact_id_list)

        result = cursor.fetchone()
        # Print result is for debugging
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_contact: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def create_contact(data):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        insert_contact_query = ("""
                            INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """)

        cursor.execute(insert_contact_query, (data.get('company_id'), data['contact_name'], data.get('title'),
          data.get('email') or None, data.get('phone') or None,
          data.get('linkedin_url'), data.get('notes') or None))

        connection.commit()
    
    except Error as error:
        print(f'Database error in create_contact: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def update_contact(contact_id, data):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)

        update_contact_query = ("""
                            UPDATE contacts SET company_id=%s, contact_name=%s, title=%s, email=%s, phone=%s, 
                            linkedin_url=%s, notes=%s WHERE contact_id=%s
                        """)

        cursor.execute(update_contact_query, (data.get('company_id'), data['contact_name'], data.get('title'),
          data.get('email') or None, data.get('phone') or None,
          data.get('linkedin_url'), data.get('notes') or None, contact_id))

        connection.commit()
    
    except Error as error:
        print(f'Database error in update_contact: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def delete_contact(contact_id):
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        delete_contact_query = ('DELETE FROM contacts WHERE contact_id = %s')

        # For debugging
        # print(contact_id)
        # print("contact_id type: ", type(contact_id))

        contact_id_list = [contact_id]

        # For debugging
        # print(contact_id_list)
        #print("contact_id_list type: ", type(contact_id_list))

        cursor.execute(delete_contact_query, contact_id_list)

        connection.commit()
    
    except Error as error:
        print(f'Database error in delete_contact: {error}')
        if cursor is not None:
            connection.rollback()
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

# For job match
def get_jobs_with_requirements():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        jobs_with_requirements_query = ('SELECT job_id, job_title, company_name, job_type, salary_min, salary_max, requirements, job_url, date_posted FROM jobs INNER JOIN companies ON jobs.company_id = companies.company_id WHERE requirements IS NOT NULL')

        cursor.execute(jobs_with_requirements_query)

        result = cursor.fetchall()
        # Print result is for debugging
        # print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_jobs_with_requirements: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

# Functions for dashboard
def get_total_jobs():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        job_count_query = ('SELECT COUNT(*) as c FROM jobs')

        cursor.execute(job_count_query)

        result = cursor.fetchone()
        # Print result is for debugging
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_total_jobs: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_total_companies():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        company_count_query = ('SELECT COUNT(*) as c FROM companies')

        cursor.execute(company_count_query)

        result = cursor.fetchone()
        # Print result is for debugging
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_total_companies: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_total_applications():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        application_count_query = ('SELECT COUNT(*) as c FROM applications')

        cursor.execute(application_count_query)

        result = cursor.fetchone()
        # Print result is for debugging
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_total_applications: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_total_contacts():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        contact_count_query = ('SELECT COUNT(*) as c FROM contacts')

        cursor.execute(contact_count_query)

        result = cursor.fetchone()
        # Print result is for debugging
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_total_contacts: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_applications_status_count():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        applications_status_count_query = ('SELECT status, COUNT(*) as count FROM applications GROUP BY status')

        cursor.execute(applications_status_count_query)

        result = cursor.fetchall()
        # Print result is for debugging
        # print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_applications_status_count: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_jobs_type_count():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        jobs_type_count_query = ('SELECT job_type, COUNT(*) as count FROM jobs GROUP BY job_type')

        cursor.execute(jobs_type_count_query)

        result = cursor.fetchall()
        # Print result is for debugging
        # print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_jobs_type_count: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_recent_applications():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        recent_applications_query = ("""
                            SELECT a.*, j.job_title, c.company_name
                            FROM applications a
                            LEFT JOIN jobs j ON a.job_id = j.job_id
                            LEFT JOIN companies c ON j.company_id = c.company_id
                            ORDER BY a.application_date DESC LIMIT 5
                        """)

        cursor.execute(recent_applications_query)

        result = cursor.fetchall()
        # Print result is for debugging
        # print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_recent_applications: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_offers_count():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        offers_count_query = ("SELECT COUNT(*) as c FROM applications WHERE status='Offer'")

        cursor.execute(offers_count_query)

        result = cursor.fetchone()
        # Print result is for debugging
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_offers_count: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_interviews_count():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        interviews_count_query = ("SELECT COUNT(*) as c FROM applications WHERE status='Interview'")

        cursor.execute(interviews_count_query)

        result = cursor.fetchone()
        # Print result is for debugging
        print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_interviews_count: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()

def get_all_offers():
    connection = None
    cursor = None

    try:
        connection = get_connection()

        if connection is None:
            return []

        cursor = connection.cursor(dictionary=True)
        all_offers_query = ("""
                                SELECT a.*, j.job_title, j.salary_min, j.salary_max, j.job_type,
                                    c.company_name, c.industry, c.city, c.state
                                FROM applications a
                                LEFT JOIN jobs j ON a.job_id = j.job_id
                                LEFT JOIN companies c ON j.company_id = c.company_id
                                WHERE a.status='Offer'
                                ORDER BY a.application_date DESC
                            """)

        cursor.execute(all_offers_query)

        result = cursor.fetchall()
        # Print result is for debugging
        # print(result)

        return result
    
    except Error as error:
        print(f'Database error in get_all_offers: {error}')
        return []

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None and connection.is_connected():
            connection.close()