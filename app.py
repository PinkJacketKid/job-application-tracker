from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import mysql.connector
import database as db
import json
import os

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()

def parse_json(req_json):
    """Parse JSON field into a list."""
    if not req_json:
        return []
    if isinstance(req_json, list):
        return req_json
    try:
        return json.loads(req_json)
    except:
        return []

def parse_json_app(req_json):
    """Parse JSON field into a list."""
    if not req_json:
        return []
    if isinstance(req_json, dict):
        return req_json
    try:
        return json.loads(req_json)
    except:
        return []

def get_db():
    return mysql.connector.connect(
        host='localhost', user='root',
        password='root', database='job_tracker'
    )

@app.route('/')
def dashboard():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT COUNT(*) as count FROM applications')
    stats = cursor.fetchone()
    conn.close()
    return render_template('dashboard.html', stats=stats)

@app.route('/jobs')
def jobs():
    jobs = db.get_all_jobs()
    for job in jobs:
        job['requirements_list'] = parse_json(job.get('requirements'))
    return render_template('jobs.html', jobs = jobs)

@app.route('/jobs/add', methods=['GET', 'POST'])
def add_job():
    companies = db.get_all_companies()

    if request.method == 'POST':
        try:
            db.create_job(request.form)
            flash('Job added successfully!', 'success')
            return redirect(url_for('jobs'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')

    return render_template('jobs_form.html', job=None, companies=companies, action='Add')

@app.route('/jobs/edit/<int:job_id>', methods=['GET', 'POST'])
def edit_job(job_id):
    job = db.get_job(job_id)
    companies = db.get_all_companies()

    if not job:
        flash('Job not found.', 'danger')
        return redirect(url_for('jobs'))
    
    if request.method == 'POST':
        try:
            db.update_job(job_id, request.form)
            flash('Job updated successfully!', 'success')
            return redirect(url_for('jobs'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
            
    job['requirements_str'] = ', '.join(parse_json(job.get('requirements')))
    return render_template('jobs_form.html', job=job, companies=companies, action='Edit')

@app.route('/jobs/delete/<int:job_id>', methods=['POST'])
def delete_job(job_id):
    try:
        db.delete_job(job_id)
        flash('Job deleted.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('jobs'))

@app.route('/companies')
def companies():
    companies = db.get_all_companies()
    return render_template('companies.html', companies = companies)

@app.route('/companies/add', methods=['GET', 'POST'])
def add_company():
    if request.method == 'POST':
        try:
            db.create_company(request.form)
            flash('Company added successfully!', 'success')
            return redirect(url_for('companies'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('companies_form.html', company=None, action='Add')

@app.route('/companies/edit/<int:company_id>', methods=['GET', 'POST'])
def edit_company(company_id):
    company = db.get_company(company_id)
    if not company:
        flash('Company not found.', 'danger')
        return redirect(url_for('companies'))
    if request.method == 'POST':
        try:
            db.update_company(company_id, request.form)
            flash('Company updated successfully!', 'success')
            return redirect(url_for('companies'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('companies_form.html', company=company, action='Edit')

@app.route('/companies/delete/<int:company_id>', methods=['POST'])
def delete_company(company_id):
    try:
        db.delete_company(company_id)
        flash('Company deleted.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('companies'))

@app.route('/applications')
def applications():
    applications = db.get_all_applications()
    for application in applications:
        # For debugging
        # print(application.get('interview_data'))
        # print("interview_data type: ", type(application.get('interview_data')))

        application['interview_data_dict'] = parse_json_app(application.get('interview_data'))

        # For debugging
        # print(application['interview_data_dict'])
        # print("interview_data_dict type: ", type(application['interview_data_dict']))
    return render_template('applications.html', applications = applications)

@app.route('/applications/add', methods=['GET', 'POST'])
def add_application():
    jobs = db.get_all_jobs()
    if request.method == 'POST':
        try:
            db.create_application(request.form)
            flash('Application added successfully!', 'success')
            return redirect(url_for('applications'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('applications_form.html', application=None, jobs=jobs, action='Add')

@app.route('/applications/edit/<int:application_id>', methods=['GET', 'POST'])
def edit_application(application_id):
    application = db.get_application(application_id)
    jobs = db.get_all_jobs()
    if not application:
        flash('Application not found.', 'danger')
        return redirect(url_for('applications'))
    if request.method == 'POST':
        try:
            db.update_application(application_id, request.form)
            flash('Application updated!', 'success')
            return redirect(url_for('applications'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('applications_form.html', application=application, jobs=jobs, action='Edit')

@app.route('/applications/delete/<int:application_id>', methods=['POST'])
def delete_application(application_id):
    try:
        db.delete_application(application_id)
        flash('Application deleted.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('applications'))

@app.route('/contacts')
def contacts():
    contacts = db.get_all_contacts()
    return render_template('contacts.html', contacts=contacts)

@app.route('/contacts/add', methods=['GET', 'POST'])
def add_contact():
    companies = db.get_all_companies()
    if request.method == 'POST':
        try:
            db.create_contact(request.form)
            flash('Contact added successfully!', 'success')
            return redirect(url_for('contacts'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('contacts_form.html', contact=None, companies=companies, action='Add')

@app.route('/contacts/edit/<int:contact_id>', methods=['GET', 'POST'])
def edit_contact(contact_id):
    contact = db.get_contact(contact_id)
    companies = db.get_all_companies()
    if not contact:
        flash('Contact not found.', 'danger')
        return redirect(url_for('contacts'))
    if request.method == 'POST':
        try:
            db.update_contact(contact_id, request.form)
            flash('Contact updated!', 'success')
            return redirect(url_for('contacts'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return render_template('contacts_form.html', contact=contact, companies=companies, action='Edit')

@app.route('/contacts/delete/<int:contact_id>', methods=['POST'])
def delete_contact(contact_id):
    try:
        db.delete_contact(contact_id)
        flash('Contact deleted.', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('contacts'))

@app.route('/job-match', methods=['GET', 'POST'])
def job_match():
    results = []
    user_skills = ''

    if request.method == 'POST':
        user_skills = request.form.get('skills', '')
        skill_list = {s.strip().lower() for s in user_skills.split(',') if s.strip()}
        all_jobs_requirements = db.get_jobs_with_requirements()

        for job in all_jobs_requirements:
            job_reqs = parse_json(job.get('requirements'))
            job_reqs_lower = [r.lower() for r in job_reqs]

            if not job_reqs:
                continue

            matched = [s for s in skill_list if s in job_reqs_lower]
            missing = [r for r in job_reqs if r.lower() not in skill_list]
            match_percentage = round(len(matched) / len(job_reqs) * 100) if job_reqs else 0

            matched_count = len(matched)

            if matched_count > 0:
                results.append({
                    'job': job,
                    'match_percentage': match_percentage,
                    'matched': matched,
                    'missing': missing,
                    'matched_count': len(matched),
                    'total_count': len(job_reqs)
                })

        results.sort(key=lambda x: x['match_percentage'], reverse=True)

    return render_template('job_match.html', results=results, user_skills=user_skills)

if __name__ == '__main__':
    app.run(debug=True)