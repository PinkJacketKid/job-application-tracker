from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
import mysql.connector
import database as db
import json

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True)