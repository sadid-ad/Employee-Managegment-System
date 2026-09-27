import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import execute_query, initialize_database

# Import all modules
from attendance import AttendanceFrame
from leave import LeaveFrame
from payroll import PayrollFrame
from recruitment import RecruitmentFrame
from training import TrainingFrame
from project_management import ProjectFrame
from reporting import ReportingFrame

# Initialize database
try:
    initialize_database()
except Exception as e:
    print(f"Database init warning: {e}")

class EmployeeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🏢 Employee Management System Pro")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f0f0')
        
        self.main_container = tk.Frame(root, bg='#f0f0f0')
        self.main_container.pack(fill=tk.BOTH, expand=True)
        
        self.create_navigation()
        
        self.content = tk.Frame(self.main_container, bg='white')
        self.content.pack(side='right', fill=tk.BOTH, expand=True)
        
        self.frames = {}
        self.create_frames()
        self.show_frame('dashboard')
        self.create_status_bar()

    def create_navigation(self):
        nav = tk.Frame(self.main_container, bg='#2c3e50', width=240)
        nav.pack(side='left', fill='y')
        nav.pack_propagate(False)
        
        title_frame = tk.Frame(nav, bg='#2c3e50')
        title_frame.pack(fill=tk.X, pady=20)
        
        tk.Label(title_frame, text="🏢 EMS", 
                font=('Segoe UI', 18, 'bold'), 
                bg='#2c3e50', fg='#3498db').pack()
        
        tk.Label(title_frame, text="Employee Management System", 
                font=('Segoe UI', 10), 
                bg='#2c3e50', fg='#bdc3c7').pack()
        
        tk.Frame(nav, bg='#34495e', height=2).pack(fill=tk.X, padx=10, pady=10)
        
        nav_buttons = [
            ("📊 Dashboard", 'dashboard'),
            ("👥 Employees", 'employees'),
            ("📅 Attendance", 'attendance'),
            ("🏖️ Leave", 'leave'),
            ("💰 Payroll", 'payroll'),
            ("🎯 Recruitment", 'recruitment'),
            ("📚 Training", 'training'),
            ("📋 Projects", 'projects'),
            ("📈 Reporting", 'reporting')
        ]
        
        self.nav_buttons = {}
        for text, key in nav_buttons:
            btn = tk.Button(nav, text=text, font=('Segoe UI', 10),
                           bg='#34495e', fg='white', 
                           width=22, height=2, relief='flat',
                           command=lambda k=key: self.show_frame(k))
            btn.pack(pady=3, padx=10)
            self.nav_buttons[key] = btn
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg='#3498db'))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg='#34495e'))

    def create_frames(self):
        modules = {
            'dashboard': DashboardFrame,
            'employees': EmployeesFrame,
            'attendance': AttendanceFrame,
            'leave': LeaveFrame,
            'payroll': PayrollFrame,
            'recruitment': RecruitmentFrame,
            'training': TrainingFrame,
            'projects': ProjectFrame,
            'reporting': ReportingFrame
        }
        
        for name, cls in modules.items():
            if cls:
                frame = cls(self.content)
                self.frames[name] = frame
                frame.pack(fill=tk.BOTH, expand=True)
                frame.pack_forget()

    def show_frame(self, name):
        for frame in self.frames.values():
            frame.pack_forget()
        
        if name in self.frames:
            self.frames[name].pack(fill=tk.BOTH, expand=True)
            
            for key, btn in self.nav_buttons.items():
                if key == name:
                    btn.configure(bg='#3498db')
                else:
                    btn.configure(bg='#34495e')

    def create_status_bar(self):
        status_bar = tk.Frame(self.root, bg='#2c3e50', height=25)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        tk.Label(status_bar, text="Ready", 
                bg='#2c3e50', fg='#bdc3c7',
                font=('Segoe UI', 9), anchor='w').pack(side=tk.LEFT, padx=10)
        
        tk.Label(status_bar, text="Python 3.12 | SQLite", 
                bg='#2c3e50', fg='#7f8c8d',
                font=('Segoe UI', 9)).pack(side=tk.RIGHT, padx=10)

class DashboardFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_dashboard_data()
    
    def setup_ui(self):
        header = tk.Frame(self, bg='#3498db', height=80)
        header.pack(fill=tk.X)
        tk.Label(header, text="📊 Dashboard", 
                font=('Segoe UI', 24, 'bold'), 
                bg='#3498db', fg='white').pack(pady=20)
        
        stats_frame = tk.Frame(self, bg='white')
        stats_frame.pack(pady=20, padx=20, fill=tk.X)
        
        self.total_employees = self.create_stat_card(stats_frame, "👥 Total Employees", "0", "#3498db", 0)
        self.total_salary = self.create_stat_card(stats_frame, "💰 Total Salary", "", "#2ecc71", 1)
        self.total_projects = self.create_stat_card(stats_frame, "📋 Active Projects", "0", "#f39c12", 2)
        self.total_leave = self.create_stat_card(stats_frame, "🏖️ Pending Leave", "0", "#e74c3c", 3)
        
        tk.Label(self, text="📋 Recent Employees", 
                font=('Segoe UI', 16, 'bold'),
                fg='#2c3e50').pack(pady=10, anchor='w', padx=20)
        
        columns = ('ID', 'Name', 'Department', 'Designation', 'Salary')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=6)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill=tk.X, padx=20, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill='y')
    
    def create_stat_card(self, parent, title, value, color, col):
        frame = tk.Frame(parent, bg=color, relief=tk.RAISED, bd=2)
        frame.grid(row=0, column=col, padx=10, pady=10, sticky='nsew')
        tk.Label(frame, text=title, font=('Segoe UI', 11), 
                bg=color, fg='white').pack(pady=5)
        lbl_value = tk.Label(frame, text=value, font=('Segoe UI', 22, 'bold'),
                            bg=color, fg='white')
        lbl_value.pack(pady=10)
        parent.grid_columnconfigure(col, weight=1)
        return lbl_value
    
    def load_dashboard_data(self):
        try:
            total = execute_query("SELECT COUNT(*) FROM employees", fetch=True)
            if total:
                self.total_employees.config(text=str(total[0][0]))
            
            salary = execute_query("SELECT COALESCE(SUM(salary), 0) FROM employees", fetch=True)
            if salary:
                self.total_salary.config(text=f"")
            
            projects = execute_query("SELECT COUNT(*) FROM projects WHERE status='Active'", fetch=True)
            if projects:
                self.total_projects.config(text=str(projects[0][0]))
            
            leave = execute_query("SELECT COUNT(*) FROM leaves WHERE status='Pending'", fetch=True)
            if leave:
                self.total_leave.config(text=str(leave[0][0]))
            
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            rows = execute_query("""
                SELECT id, name, department, designation, salary 
                FROM employees 
                ORDER BY id DESC 
                LIMIT 5
            """, fetch=True)
            
            for row in rows:
                self.tree.insert('', tk.END, values=row)
        except Exception as e:
            print(f"Dashboard Error: {e}")

class EmployeesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_employees()
    
    def setup_ui(self):
        tk.Label(self, text="👥 Employee Management", 
                font=('Segoe UI', 20, 'bold'),
                fg='#2c3e50').pack(pady=10)
        
        search_frame = tk.Frame(self, bg='white', relief=tk.RAISED, bd=1)
        search_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = tk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self.search_employees)
        
        tk.Label(search_frame, text="Department:").pack(side=tk.LEFT, padx=5)
        self.dept_combo = ttk.Combobox(search_frame, width=20)
        self.dept_combo.pack(side=tk.LEFT, padx=5)
        self.dept_combo.bind('<<ComboboxSelected>>', self.search_employees)
        self.load_departments()
        
        tk.Button(search_frame, text="🔄 Refresh", bg='#3498db', fg='white',
                 command=self.load_employees).pack(side=tk.LEFT, padx=5)
        
        columns = ('ID', 'Name', 'Department', 'Designation', 'Salary', 'Email')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)
        
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        
        btn_frame = tk.Frame(self, bg='white')
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="➕ Add Employee", bg='#27ae60', fg='white',
                 font=('Segoe UI', 10), command=self.add_employee).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✏️ Edit Employee", bg='#f39c12', fg='white',
                 font=('Segoe UI', 10), command=self.edit_employee).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="🗑️ Delete Employee", bg='#e74c3c', fg='white',
                 font=('Segoe UI', 10), command=self.delete_employee).pack(side=tk.LEFT, padx=5)
    
    def load_departments(self):
        rows = execute_query("SELECT DISTINCT department FROM employees WHERE department IS NOT NULL", fetch=True)
        depts = ['All'] + [row[0] for row in rows if row[0]]
        self.dept_combo['values'] = depts
        self.dept_combo.set('All')
    
    def load_employees(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        rows = execute_query("SELECT id, name, department, designation, salary, email FROM employees", fetch=True)
        for row in rows:
            self.tree.insert('', tk.END, values=row)
    
    def search_employees(self, event=None):
        search = self.search_entry.get().lower()
        dept = self.dept_combo.get()
        for item in self.tree.get_children():
            self.tree.delete(item)
        if dept == 'All':
            dept = None
        query = "SELECT id, name, department, designation, salary, email FROM employees WHERE 1=1"
        params = []
        if search:
            query += " AND LOWER(name) LIKE ?"
            params.append(f"%{search}%")
        if dept:
            query += " AND department = ?"
            params.append(dept)
        rows = execute_query(query, params, fetch=True)
        for row in rows:
            self.tree.insert('', tk.END, values=row)
    
    def add_employee(self):
        AddEmployeeDialog(self)
    
    def edit_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an employee to edit")
            return
        values = self.tree.item(selected[0])['values']
        EditEmployeeDialog(self, values)
    
    def delete_employee(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an employee to delete")
            return
        emp_id = self.tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm", "Delete this employee?"):
            execute_query("DELETE FROM employees WHERE id=?", (emp_id,))
            self.load_employees()
            messagebox.showinfo("Success", "Employee deleted")

class AddEmployeeDialog:
    def __init__(self, parent):
        self.parent = parent
        self.dialog = tk.Toplevel()
        self.dialog.title("Add Employee")
        self.dialog.geometry("450x550")
        self.dialog.configure(bg='white')
        self.dialog.resizable(False, False)
        self.dialog.transient(parent.master)
        self.dialog.grab_set()
        
        tk.Label(self.dialog, text="➕ Add New Employee", 
                font=('Segoe UI', 18, 'bold'),
                bg='white', fg='#2c3e50').pack(pady=15)
        
        fields = [
            ('Name *:', 'name_entry'),
            ('Department *:', 'dept_entry'),
            ('Designation:', 'desig_entry'),
            ('Salary:', 'salary_entry'),
            ('Email:', 'email_entry'),
            ('Phone:', 'phone_entry')
        ]
        
        self.entries = {}
        for label, key in fields:
            frame = tk.Frame(self.dialog, bg='white')
            frame.pack(fill=tk.X, padx=30, pady=5)
            tk.Label(frame, text=label, width=15, anchor='w',
                    bg='white', font=('Segoe UI', 10)).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=25, font=('Segoe UI', 10))
            entry.pack(side=tk.LEFT, padx=5)
            self.entries[key] = entry
        
        btn_frame = tk.Frame(self.dialog, bg='white')
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="💾 Save", bg='#27ae60', fg='white',
                 font=('Segoe UI', 10), width=12,
                 command=self.save_employee).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancel", bg='#e74c3c', fg='white',
                 font=('Segoe UI', 10), width=12,
                 command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def save_employee(self):
        name = self.entries['name_entry'].get().strip()
        dept = self.entries['dept_entry'].get().strip()
        desig = self.entries['desig_entry'].get().strip()
        salary = self.entries['salary_entry'].get().strip()
        email = self.entries['email_entry'].get().strip()
        phone = self.entries['phone_entry'].get().strip()
        if not name or not dept:
            messagebox.showerror("Error", "Name and Department are required!")
            return
        try:
            query = "INSERT INTO employees (name, department, designation, salary, email, phone) VALUES (?, ?, ?, ?, ?, ?)"
            execute_query(query, (name, dept, desig, salary if salary else None, email, phone))
            messagebox.showinfo("Success", "✅ Employee added successfully!")
            self.dialog.destroy()
            self.parent.load_employees()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add employee: {str(e)}")

class EditEmployeeDialog:
    def __init__(self, parent, values):
        self.parent = parent
        self.emp_id = values[0]
        self.dialog = tk.Toplevel()
        self.dialog.title("Edit Employee")
        self.dialog.geometry("450x500")
        self.dialog.configure(bg='white')
        self.dialog.resizable(False, False)
        self.dialog.transient(parent.master)
        self.dialog.grab_set()
        
        tk.Label(self.dialog, text="✏️ Edit Employee", 
                font=('Segoe UI', 18, 'bold'),
                bg='white', fg='#2c3e50').pack(pady=15)
        
        fields = [
            ('Name:', values[1]),
            ('Department:', values[2]),
            ('Designation:', values[3]),
            ('Salary:', values[4]),
            ('Email:', values[5])
        ]
        
        self.entries = {}
        for label, value in fields:
            frame = tk.Frame(self.dialog, bg='white')
            frame.pack(fill=tk.X, padx=30, pady=5)
            tk.Label(frame, text=label, width=15, anchor='w',
                    bg='white', font=('Segoe UI', 10)).pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=25, font=('Segoe UI', 10))
            entry.insert(0, str(value) if value else '')
            entry.pack(side=tk.LEFT, padx=5)
            self.entries[label] = entry
        
        btn_frame = tk.Frame(self.dialog, bg='white')
        btn_frame.pack(pady=20)
        tk.Button(btn_frame, text="💾 Update", bg='#27ae60', fg='white',
                 font=('Segoe UI', 10), width=12,
                 command=self.update_employee).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancel", bg='#e74c3c', fg='white',
                 font=('Segoe UI', 10), width=12,
                 command=self.dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def update_employee(self):
        name = self.entries['Name:'].get().strip()
        dept = self.entries['Department:'].get().strip()
        desig = self.entries['Designation:'].get().strip()
        salary = self.entries['Salary:'].get().strip()
        email = self.entries['Email:'].get().strip()
        if not name or not dept:
            messagebox.showerror("Error", "Name and Department are required!")
            return
        try:
            query = "UPDATE employees SET name=?, department=?, designation=?, salary=?, email=? WHERE id=?"
            execute_query(query, (name, dept, desig, salary if salary else None, email, self.emp_id))
            messagebox.showinfo("Success", "✅ Employee updated successfully!")
            self.dialog.destroy()
            self.parent.load_employees()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update employee: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeApp(root)
    root.mainloop()
