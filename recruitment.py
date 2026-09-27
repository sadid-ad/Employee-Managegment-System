import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import execute_query

class RecruitmentFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_openings()
        self.load_applications()

    def setup_ui(self):
        tk.Label(self, text="🎯 Recruitment Management", font=('Segoe UI', 20, 'bold'),
                fg='#2c3e50').pack(pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tab1 = tk.Frame(notebook)
        notebook.add(tab1, text="📋 Job Openings")
        self.setup_openings_tab(tab1)

        tab2 = tk.Frame(notebook)
        notebook.add(tab2, text="📝 Applications")
        self.setup_applications_tab(tab2)

    def setup_openings_tab(self, parent):
        form = tk.LabelFrame(parent, text="Add New Job Opening", font=('Segoe UI', 10, 'bold'))
        form.pack(fill=tk.X, padx=5, pady=5)

        row1 = tk.Frame(form)
        row1.pack(fill=tk.X, pady=5)
        tk.Label(row1, text="Title:").pack(side=tk.LEFT, padx=5)
        self.title_entry = tk.Entry(row1, width=25)
        self.title_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(row1, text="Department:").pack(side=tk.LEFT, padx=5)
        self.dept_entry = tk.Entry(row1, width=20)
        self.dept_entry.pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(form)
        row2.pack(fill=tk.X, pady=5)
        tk.Label(row2, text="Description:").pack(side=tk.LEFT, padx=5)
        self.desc_entry = tk.Entry(row2, width=50)
        self.desc_entry.pack(side=tk.LEFT, padx=5)

        row3 = tk.Frame(form)
        row3.pack(fill=tk.X, pady=5)
        tk.Label(row3, text="Closing Date (YYYY-MM-DD):").pack(side=tk.LEFT, padx=5)
        self.close_entry = tk.Entry(row3, width=15)
        self.close_entry.pack(side=tk.LEFT, padx=5)
        self.close_entry.insert(0, "2026-09-30")
        tk.Button(row3, text="Add Opening", bg='#27ae60', fg='white',
                 command=self.add_opening).pack(side=tk.LEFT, padx=5)

        columns = ('ID', 'Title', 'Department', 'Closing Date', 'Status')
        self.opening_tree = ttk.Treeview(parent, columns=columns, show='headings', height=8)
        for col in columns:
            self.opening_tree.heading(col, text=col)
            self.opening_tree.column(col, width=120)
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.opening_tree.yview)
        self.opening_tree.configure(yscrollcommand=scrollbar.set)
        self.opening_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=5)

        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Refresh", bg='#3498db', fg='white',
                 command=self.load_openings).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close Opening", bg='#e67e22', fg='white',
                 command=self.close_opening).pack(side=tk.LEFT, padx=5)

    def setup_applications_tab(self, parent):
        form = tk.LabelFrame(parent, text="Add Application", font=('Segoe UI', 10, 'bold'))
        form.pack(fill=tk.X, padx=5, pady=5)

        row1 = tk.Frame(form)
        row1.pack(fill=tk.X, pady=5)
        tk.Label(row1, text="Job Opening:").pack(side=tk.LEFT, padx=5)
        self.job_combo = ttk.Combobox(row1, width=25)
        self.job_combo.pack(side=tk.LEFT, padx=5)
        self.load_job_openings()
        tk.Label(row1, text="Candidate:").pack(side=tk.LEFT, padx=5)
        self.cand_entry = tk.Entry(row1, width=20)
        self.cand_entry.pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(form)
        row2.pack(fill=tk.X, pady=5)
        tk.Label(row2, text="Email:").pack(side=tk.LEFT, padx=5)
        self.email_entry = tk.Entry(row2, width=25)
        self.email_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(row2, text="Phone:").pack(side=tk.LEFT, padx=5)
        self.phone_entry = tk.Entry(row2, width=15)
        self.phone_entry.pack(side=tk.LEFT, padx=5)

        row3 = tk.Frame(form)
        row3.pack(fill=tk.X, pady=5)
        tk.Label(row3, text="Resume (text):").pack(side=tk.LEFT, padx=5)
        self.resume_entry = tk.Entry(row3, width=50)
        self.resume_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(row3, text="Add Application", bg='#27ae60', fg='white',
                 command=self.add_application).pack(side=tk.LEFT, padx=5)

        columns = ('ID', 'Job Title', 'Candidate', 'Email', 'Status')
        self.app_tree = ttk.Treeview(parent, columns=columns, show='headings', height=8)
        for col in columns:
            self.app_tree.heading(col, text=col)
            self.app_tree.column(col, width=120)
        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=self.app_tree.yview)
        self.app_tree.configure(yscrollcommand=scrollbar.set)
        self.app_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=5)

        btn_frame = tk.Frame(parent)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="Refresh", bg='#3498db', fg='white',
                 command=self.load_applications).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Shortlist", bg='#2ecc71', fg='white',
                 command=lambda: self.update_app_status('Shortlisted')).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Hire", bg='#3498db', fg='white',
                 command=lambda: self.update_app_status('Hired')).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Reject", bg='#e74c3c', fg='white',
                 command=lambda: self.update_app_status('Rejected')).pack(side=tk.LEFT, padx=5)

    def load_job_openings(self):
        try:
            rows = execute_query("SELECT id, title FROM job_openings WHERE status='Open'", fetch=True)
            values = []
            for row in rows:
                values.append(str(row[0]) + " - " + str(row[1]))
            self.job_combo['values'] = values
            if values:
                self.job_combo.set(values[0])
        except Exception as e:
            print(f"Error loading job openings: {e}")

    def load_openings(self):
        try:
            for item in self.opening_tree.get_children():
                self.opening_tree.delete(item)
            rows = execute_query("SELECT id, title, department, closing_date, status FROM job_openings", fetch=True)
            for row in rows:
                self.opening_tree.insert('', tk.END, values=row)
        except Exception as e:
            print(f"Error loading openings: {e}")

    def load_applications(self):
        try:
            for item in self.app_tree.get_children():
                self.app_tree.delete(item)
            query = """
                SELECT a.id, j.title, a.candidate_name, a.email, a.status
                FROM applications a
                JOIN job_openings j ON a.job_id = j.id
                ORDER BY a.id DESC
            """
            rows = execute_query(query, fetch=True)
            for row in rows:
                self.app_tree.insert('', tk.END, values=row)
        except Exception as e:
            print(f"Error loading applications: {e}")

    def add_opening(self):
        title = self.title_entry.get().strip()
        dept = self.dept_entry.get().strip()
        desc = self.desc_entry.get().strip()
        close = self.close_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required")
            return
        try:
            query = "INSERT INTO job_openings (title, department, description, closing_date) VALUES (?, ?, ?, ?)"
            execute_query(query, (title, dept, desc, close))
            messagebox.showinfo("Success", "Job opening added!")
            self.title_entry.delete(0, tk.END)
            self.dept_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.load_openings()
            self.load_job_openings()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add opening: {str(e)}")

    def close_opening(self):
        selected = self.opening_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a job opening to close")
            return
        if messagebox.askyesno("Confirm", "Close this job opening?"):
            try:
                opening_id = self.opening_tree.item(selected[0])['values'][0]
                execute_query("UPDATE job_openings SET status='Closed' WHERE id=?", (opening_id,))
                self.load_openings()
                self.load_job_openings()
                messagebox.showinfo("Success", "Job opening closed")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to close: {str(e)}")

    def add_application(self):
        job = self.job_combo.get()
        if not job:
            messagebox.showerror("Error", "Select a job opening")
            return
        job_id = job.split(' - ')[0]
        name = self.cand_entry.get().strip()
        email = self.email_entry.get().strip()
        phone = self.phone_entry.get().strip()
        resume = self.resume_entry.get().strip()
        if not name or not email:
            messagebox.showerror("Error", "Name and email are required")
            return
        try:
            query = "INSERT INTO applications (job_id, candidate_name, email, phone, resume) VALUES (?, ?, ?, ?, ?)"
            execute_query(query, (job_id, name, email, phone, resume))
            messagebox.showinfo("Success", "Application added!")
            self.cand_entry.delete(0, tk.END)
            self.email_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.resume_entry.delete(0, tk.END)
            self.load_applications()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add application: {str(e)}")

    def update_app_status(self, status):
        selected = self.app_tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select an application")
            return
        if messagebox.askyesno("Confirm", f"{status} this application?"):
            try:
                app_id = self.app_tree.item(selected[0])['values'][0]
                execute_query("UPDATE applications SET status=? WHERE id=?", (status, app_id))
                self.load_applications()
                messagebox.showinfo("Success", f"Application {status}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {str(e)}")
