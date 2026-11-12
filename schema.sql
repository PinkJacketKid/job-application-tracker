CREATE DATABASE IF NOT EXISTS job_tracker;
USE job_tracker;

CREATE TABLE IF NOT EXISTS companies (
    company_id INT AUTO_INCREMENT PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    industry VARCHAR(50),
    website VARCHAR(200),
    city VARCHAR(50),
    state VARCHAR(50),
    notes TEXT
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    job_title VARCHAR(100) NOT NULL,
    job_type ENUM('Full-time','Part-time','Contract','Internship'),
    salary_min INT,
    salary_max INT,
    job_url VARCHAR(300),
    date_posted DATE,
    requirements JSON,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

CREATE TABLE IF NOT EXISTS applications (
    application_id INT AUTO_INCREMENT PRIMARY KEY,
    job_id INT NOT NULL,
    application_date DATE NOT NULL,
    status ENUM('Applied','Screening','Interview','Offer','Rejected','Withdrawn'),
    resume_version VARCHAR(50),
    cover_letter_sent BOOLEAN DEFAULT FALSE,
    interview_data JSON,
    FOREIGN KEY (job_id) REFERENCES jobs(job_id)
);

CREATE TABLE IF NOT EXISTS contacts (
    contact_id INT AUTO_INCREMENT PRIMARY KEY,
    company_id INT NOT NULL,
    contact_name VARCHAR(100) NOT NULL,
    title VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    linkedin_url VARCHAR(200),
    notes TEXT,
    FOREIGN KEY (company_id) REFERENCES companies(company_id)
);

-- Sample data from assignments
INSERT INTO companies (company_name, industry, website, city, state) VALUES
('Tech Solutions Inc', 'Technology', 'www.techsolutions.com', 'Miami', 'Florida'),
('Data Analytics Corp', 'Data Science', 'www.dataanalytics.com', 'Austin', 'Texas'),
('Cloud Systems LLC', 'Cloud Computing', 'www.cloudsystems.com', 'Seattle', 'Washington'),
('Digital Innovations', 'Software', 'www.digitalinnovations.com', 'San Francisco', 'California'),
('Smart Tech Group', 'AI/ML', 'www.smarttech.com', 'Boston', 'Massachusetts');

INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, date_posted, requirements) VALUES
(1, 'Software Developer', 'Full-time', 70000, 90000, '2025-01-15', '["Python", "SQL", "Flask"]'),
(1, 'Database Administrator', 'Full-time', 75000, 95000, '2025-01-10', '["Python", "SQL"]'),
(2, 'Data Analyst', 'Full-time', 65000, 85000, '2025-01-12', '["Python", "SQL", "Tableau"]'),
(3, 'Cloud Engineer', 'Full-time', 80000, 100000, '2025-01-08', '["Python", "SQL", "Docker"]'),
(4, 'Junior Developer', 'Full-time', 55000, 70000, '2025-01-14', '["Python", "SQL", "Java"]'),
(4, 'Senior Developer', 'Full-time', 95000, 120000, '2025-01-14', '["Python", "SQL", "Java", "Go"]'),
(5, 'ML Engineer', 'Full-time', 90000, 115000, '2025-01-11', '["Python", "SQL", "Git"]');

INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent) VALUES
(1, '2025-01-16', 'Applied', 'v2.1', TRUE),
(3, '2025-01-13', 'Interview', 'v2.1', TRUE),
(4, '2025-01-09', 'Rejected', 'v2.0', FALSE),
(5, '2025-01-15', 'Applied', 'v2.1', TRUE),
(7, '2025-01-12', 'Screening', 'v2.1', TRUE);

-- Adding interview data
UPDATE applications
SET interview_data = '{
  "interview_rounds": 2,
  "interviewers": ["Sarah Johnson", "Mike Chen"],
  "technical_questions": ["SQL joins", "Python basics", "API design"],
  "feedback": "Strong technical skills, good communication",
  "next_steps": "Final round scheduled"
}'
WHERE application_id = 2;

UPDATE applications
SET interview_data = '{
  "interview_rounds": 1,
  "interviewers": ["Emily Williams"],
  "technical_questions": ["Database normalization", "Transaction isolation"],
  "feedback": "Needs more experience with cloud platforms",
  "rating": 3
}'
WHERE application_id = 5;

INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes) VALUES
(1, 'Sarah Johnson', 'HR Manager', 'sjohnson@techsolutions.com', '415-555-0101', 'https://linkedin.com/in/sarahjohnson', 'Very responsive, met at meetup'),
(2, 'Michael Chen', 'Technical Recruiter', 'mchen@dataanalytics.com', '212-555-0102', 'https://linkedin.com/in/michaelchen', 'Reached out on LinkedIn'),
(3, 'Emily Williams', 'Hiring Manager', 'ewilliams@cloudsystems.com', NULL, 'https://linkedin.com/in/emilywilliams', 'Employee referral contact'),
(4, 'David Brown', 'Senior Developer', NULL, '305-754-0800', 'https://linkedin.com/in/davidbrown', 'Called me'),
(5, 'Lisa Garcia', 'Talent Acquisition', 'lgarcia@smarttech.com', NULL, 'https://linkedin.com/in/lisagarcia', 'Emailed me and does not do phone calls');
