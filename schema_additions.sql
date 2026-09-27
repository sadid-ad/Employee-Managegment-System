-- Attendance
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    date DATE NOT NULL,
    check_in TIME,
    check_out TIME,
    status VARCHAR(20) DEFAULT 'Present' -- Present, Absent, Leave, etc.
);

-- Leave
CREATE TABLE leaves (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    leave_type VARCHAR(50) NOT NULL, -- Annual, Sick, Casual, etc.
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    reason TEXT,
    status VARCHAR(20) DEFAULT 'Pending' -- Pending, Approved, Rejected
);

-- Payroll
CREATE TABLE payroll (
    id SERIAL PRIMARY KEY,
    employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    month_year DATE NOT NULL, -- first day of month
    basic_salary NUMERIC(10,2),
    allowances NUMERIC(10,2),
    deductions NUMERIC(10,2),
    net_pay NUMERIC(10,2),
    payment_date DATE
);

-- Recruitment (Job Openings & Applications)
CREATE TABLE job_openings (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    department VARCHAR(100),
    description TEXT,
    posted_date DATE,
    closing_date DATE,
    status VARCHAR(20) DEFAULT 'Open'
);

CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    job_id INTEGER REFERENCES job_openings(id) ON DELETE CASCADE,
    candidate_name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    resume TEXT,
    application_date DATE,
    status VARCHAR(20) DEFAULT 'Applied' -- Applied, Shortlisted, Interviewed, Hired, Rejected
);

-- Training
CREATE TABLE training (
    id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    trainer VARCHAR(100),
    status VARCHAR(20) DEFAULT 'Scheduled'
);

CREATE TABLE training_attendance (
    id SERIAL PRIMARY KEY,
    training_id INTEGER REFERENCES training(id) ON DELETE CASCADE,
    employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    attended BOOLEAN DEFAULT FALSE
);

-- Project Management
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    status VARCHAR(20) DEFAULT 'Planning' -- Planning, Active, Completed, On Hold
);

CREATE TABLE project_assignments (
    id SERIAL PRIMARY KEY,
    project_id INTEGER REFERENCES projects(id) ON DELETE CASCADE,
    employee_id INTEGER REFERENCES employees(id) ON DELETE CASCADE,
    role VARCHAR(50),
    assigned_date DATE
);