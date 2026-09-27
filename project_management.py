import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import execute_query

class ProjectFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_projects()
        self.load_assignments()

    def setup_ui(self):
        tk.Label(self, text="📋 Project Management", font=('Segoe UI', 20, 'bold'),
                fg='#2c3e50').pack(pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tab1 = tk.Frame(notebook)
        notebook.add(tab1, text="📁 Projects")
        self.setup_projects_tab(tab1)

        tab2 = tk.Frame(notebook)
        notebook.add(tab2, text="👥 Assignments")
        self.setup_assignments_tab(tab2)

    def setup_projects_tab(self, parent):
        form = tk.LabelFrame(parent, text="Add New Project", font=('Segoe UI', 10, 'bold'))
        form.pack(fill=tk.X, padx=5, pady=5)

        row1 = tk.Frame(form)
        row1.pack(fill=tk.X, pady=5)
        tk.Label(row1, text="Project Name:").pack(side=tk.LEFT, padx=5)
        self.name_entry = tk.Entry(row1, width=25)
        self.name_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(row1, text="Description:").pack(side=tk.LEFT, padx=5)
        self.desc_entry = tk.Entry(row1, width=30)
        self.desc_entry.pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(form)
        row2.pack(fill=tk.X, pady=5)
        tk.Label(row2, text="Start Date:").pack(side=tk.LEFT, padx=5)
        self.start_entry = tk.Entry(row2, width=15)
        self.start_entry.pack(side=tk.LEFT, padx=5)
        self.start_entry.insert(0, "2026-08-09")
        tk.Label(row2, text="End Date:").pack(side=tk.LEFT, padx=5)
        self.end_entry = tk.Entry(row2, width=15)
        self.end_entry.pack(side=tk.LEFT, padx=5)
        self.end_entry.insert(0, "2026-12-31")
        tk.Button(row2, text="Add Project", bg='#27ae60', fg='white',
                 command=self.add_project).pack(side=tk.LEFT, padx=5)

        columns = ('ID', 'Name', 'Description', 'Start', 'End', 'Status')
        self.project_tree = ttk.Treeview(parent, columns=columns, show='headings', height=8)
        for col in columns:
            self.project_tree.heading(col, text=col)
            self.project_tree.column(col, width=120)
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.project_tree.yview)
        self.project_tree.configure(yscrollcommand=scrollbar.set)
        self.project_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=5)

        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Refresh", bg='#3498db', fg='white',
                 command=self.load_projects).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Start", bg='#2ecc71', fg='white',
                 command=lambda: self.update_project_status('Active')).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Complete", bg='#3498db', fg='white',
                 command=lambda: self.update_project_status('Completed')).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="On Hold", bg='#f39c12', fg='white',
                 command=lambda: self.update_project_status('On Hold')).pack(side=tk.LEFT, padx=5)

    def setup_assignments_tab(self, parent):
        form = tk.LabelFrame(parent, text="Assign Employee to Project", font=('Segoe UI', 10, 'bold'))
        form.pack(fill=tk.X, padx=5, pady=5)

        row1 = tk.Frame(form)
        row1.pack(fill=tk.X, pady=5)
        tk.Label(row1, text="Project:").pack(side=tk.LEFT, padx=5)
        self.proj_combo = ttk.Combobox(row1, width=25)
        self.proj_combo.pack(side=tk.LEFT, padx=5)
        self.load_project_combo()
        tk.Label(row1, text="Employee:").pack(side=tk.LEFT, padx=5)
        self.emp_combo = ttk.Combobox(row1, width=25)
        self.emp_combo.pack(side=tk.LEFT, padx=5)
        self.load_employee_combo()

        row2 = tk.Frame(form)
        row2.pack(fill=tk.X, pady=5)
        tk.Label(row2, text="Role:").pack(side=tk.LEFT, padx=5)
        self.role_entry = tk.Entry(row2, width=25)
        self.role_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(row2, text="Assign", bg='#27ae60', fg='white',
                 command=self.add_assignment).pack(side=tk.LEFT, padx=5)

        columns = ('ID', 'Project', 'Employee', 'Role', 'Assigned Date')
        self.assignment_tree = ttk.Treeview(parent, columns=columns, show='headings', height=8)
        for col in columns:
            self.assignment_tree.heading(col, text=col)
            self.assignment_tree.column(col, width=120)
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.assignment_tree.yview)
        self.assignment_tree.configure(yscrollcommand=scrollbar.set)
        self.assignment_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=5)

        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Refresh", bg='#3498db', fg='white',
                 command=self.load_assignments).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Remove", bg='#e74c3c', fg='white',
                 command=self.remove_assignment).pack(side=tk.LEFT, padx=5)

    def load_project_combo(self):
        try:
            rows = execute_query("SELECT id, name FROM projects", fetch=True)
            values = []
            for row in rows:
                values.append(str(row[0]) + " - " + str(row[1]))
            self.proj_combo['values'] = values
            if values:
                self.proj_combo.set(values[0])
        except Exception as e:
            print(f"Error loading projects: {e}")

    def load_employee_combo(self):
        try:
            rows = execute_query("SELECT id, name FROM employees", fetch=True)
            values = []
            for row in rows:
                values.append(str(row[0]) + " - " + str(row[1]))
            self.emp_combo['values'] = values
            if values:
                self.emp_combo.set(values[0])
        except Exception as e:
            print(f"Error loading employees: {e}")

    def load_projects(self):
        try:
            for item in self.project_tree.get_children():
                self.project_tree.delete(item)
            rows = execute_query("SELECT id, name, description, start_date, end_date, status FROM projects", fetch=True)
            for row in rows:
                self.project_tree.insert('', tk.END, values=row)
        except Exception as e:
            print(f"Error loading projects: {e}")

    def load_assignments(self):
        try:
            for item in self.assignment_tree.get_children():
                self.assignment_tree.delete(item)
            query = """
                SELECT pa.id, p.name, e.name, pa.role, pa.assigned_date
                FROM project_assignments pa
                JOIN projects p ON pa.project_id = p.id
                JOIN employees e ON pa.employee_id = e.id
            """
            rows = execute_query(query, fetch=True)
            for row in rows:
                self.assignment_tree.insert('', tk.END, values=row)
        except Exception as e:
            print(f"Error loading assignments: {e}")

    def add_project(self):
        name = self.name_entry.get().strip()
        desc = self.desc_entry.get().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Project name is required")
            return
        try:
            query = "INSERT INTO projects (name, description, start_date, end_date) VALUES (?, ?, ?, ?)"
            execute_query(query, (name, desc, start, end))
            messagebox.showinfo("Success", "Project added!")
            self.name_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.load_projects()
            self.load_project_combo()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add project: {str(e)}")

    def update_project_status(self, status):
        selected = self.project_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a project")
            return
        if messagebox.askyesno("Confirm", f"Mark project as {status}?"):
            try:
                project_id = self.project_tree.item(selected[0])['values'][0]
                execute_query("UPDATE projects SET status=? WHERE id=?", (status, project_id))
                self.load_projects()
                messagebox.showinfo("Success", f"Project status updated to {status}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {str(e)}")

    def add_assignment(self):
        proj = self.proj_combo.get()
        emp = self.emp_combo.get()
        role = self.role_entry.get().strip()
        if not all([proj, emp, role]):
            messagebox.showerror("Error", "Please fill all fields")
            return
        try:
            proj_id = proj.split(' - ')[0]
            emp_id = emp.split(' - ')[0]
            query = "INSERT INTO project_assignments (project_id, employee_id, role) VALUES (?, ?, ?)"
            execute_query(query, (proj_id, emp_id, role))
            messagebox.showinfo("Success", "Employee assigned to project!")
            self.role_entry.delete(0, tk.END)
            self.load_assignments()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to assign: {str(e)}")

    def remove_assignment(self):
        selected = self.assignment_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an assignment to remove")
            return
        if messagebox.askyesno("Confirm", "Remove this assignment?"):
            try:
                assignment_id = self.assignment_tree.item(selected[0])['values'][0]
                execute_query("DELETE FROM project_assignments WHERE id=?", (assignment_id,))
                self.load_assignments()
                messagebox.showinfo("Success", "Assignment removed")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to remove: {str(e)}")
