import sqlite3
import os

DB_PATH = 'employees.db'

def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        raise e

def execute_query(query, params=None, fetch=False):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        query = query.replace('%s', '?')
        
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        if fetch:
            results = cursor.fetchall()
            conn.close()
            return results
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        if conn:
            conn.rollback()
            conn.close()
        print(f"Query execution error: {e}")
        raise e

def initialize_database():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS employees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                department TEXT,
                designation TEXT,
                salary REAL,
                email TEXT,
                phone TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                date DATE NOT NULL,
                check_in TIME,
                check_out TIME,
                status TEXT DEFAULT 'Present',
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leaves (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                leave_type TEXT NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                reason TEXT,
                status TEXT DEFAULT 'Pending',
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS payroll (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                month_year DATE NOT NULL,
                basic_salary REAL,
                allowances REAL,
                deductions REAL,
                net_pay REAL,
                payment_date DATE,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS job_openings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                department TEXT,
                description TEXT,
                posted_date DATE DEFAULT CURRENT_DATE,
                closing_date DATE,
                status TEXT DEFAULT 'Open'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER,
                candidate_name TEXT,
                email TEXT,
                phone TEXT,
                resume TEXT,
                application_date DATE DEFAULT CURRENT_DATE,
                status TEXT DEFAULT 'Applied',
                FOREIGN KEY (job_id) REFERENCES job_openings(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS training (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                start_date DATE,
                end_date DATE,
                trainer TEXT,
                status TEXT DEFAULT 'Scheduled'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                start_date DATE,
                end_date DATE,
                status TEXT DEFAULT 'Planning'
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS project_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER,
                employee_id INTEGER,
                role TEXT,
                assigned_date DATE DEFAULT CURRENT_DATE,
                FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                FOREIGN KEY (employee_id) REFERENCES employees(id) ON DELETE CASCADE
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM employees")
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO employees (name, department, designation, salary, email)
                VALUES (?, ?, ?, ?, ?)
            ''', ('Sadida', 'cse', 'terstret', 1223.00, 'sadida@email.com'))
            print("✅ Sample employee added!")
        
        conn.commit()
        conn.close()
        print("✅ Database tables created successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False

def test_connection():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()
    initialize_database()
