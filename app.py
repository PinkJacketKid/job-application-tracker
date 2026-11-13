from flask import Flask, render_template, request, redirect, jsonify
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

if __name__ == '__main__':
    app.run(debug=True)