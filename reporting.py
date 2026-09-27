import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import execute_query

class ReportingFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.show_report()

    def setup_ui(self):
        tk.Label(self, text="📈 Reporting", font=('Segoe UI', 20, 'bold'),
                fg='#2c3e50').pack(pady=10)

        btn_frame = tk.Frame(self, bg='white')
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        report_buttons = [
            ("👥 Employee Count", self.employee_count),
            ("📅 Attendance Summary", self.attendance_summary),
            ("🏖️ Leave Summary", self.leave_summary),
            ("💰 Payroll Summary", self.payroll_summary),
            ("📊 Department Wise", self.department_wise),
            ("📋 All Reports", self.all_reports)
        ]

        for text, command in report_buttons:
            tk.Button(btn_frame, text=text, bg='#3498db', fg='white',
                     font=('Segoe UI', 10), width=18, height=2,
                     command=command).pack(side=tk.LEFT, padx=5, pady=5)

        self.report_frame = tk.Frame(self, bg='white', relief=tk.SUNKEN, bd=2)
        self.report_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ('Metric', 'Value')
        self.tree = ttk.Treeview(self.report_frame, columns=columns, show='headings', height=15)
        self.tree.heading('Metric', text='Metric')
        self.tree.heading('Value', text='Value')
        self.tree.column('Metric', width=300)
        self.tree.column('Value', width=200)

        scrollbar = ttk.Scrollbar(self.report_frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill='y')

    def clear_tree(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def display_report(self, data):
        self.clear_tree()
        if isinstance(data, dict):
            for key, val in data.items():
                self.tree.insert('', tk.END, values=(key, val))
        elif isinstance(data, list):
            for row in data:
                self.tree.insert('', tk.END, values=row)

    def employee_count(self):
        try:
            count = execute_query("SELECT COUNT(*) FROM employees", fetch=True)[0][0]
            dept_count = execute_query("""
                SELECT department, COUNT(*) 
                FROM employees 
                WHERE department IS NOT NULL 
                GROUP BY department
            """, fetch=True)
            
            data = {"Total Employees": count}
            for dept, cnt in dept_count:
                data[f"  {dept}"] = cnt
            
            self.display_report(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load report: {str(e)}")

    def attendance_summary(self):
        try:
            present = execute_query("SELECT COUNT(*) FROM attendance WHERE status='Present'", fetch=True)[0][0]
            absent = execute_query("SELECT COUNT(*) FROM attendance WHERE status='Absent'", fetch=True)[0][0]
            leave = execute_query("SELECT COUNT(*) FROM attendance WHERE status='Leave'", fetch=True)[0][0]
            
            data = {
                "✅ Present": present,
                "❌ Absent": absent,
                "🏖️ On Leave": leave,
                "📊 Total": present + absent + leave
            }
            self.display_report(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load report: {str(e)}")

    def leave_summary(self):
        try:
            pending = execute_query("SELECT COUNT(*) FROM leaves WHERE status='Pending'", fetch=True)[0][0]
            approved = execute_query("SELECT COUNT(*) FROM leaves WHERE status='Approved'", fetch=True)[0][0]
            rejected = execute_query("SELECT COUNT(*) FROM leaves WHERE status='Rejected'", fetch=True)[0][0]
            
            data = {
                "⏳ Pending": pending,
                "✅ Approved": approved,
                "❌ Rejected": rejected,
                "📊 Total": pending + approved + rejected
            }
            self.display_report(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load report: {str(e)}")

    def payroll_summary(self):
        try:
            total = execute_query("SELECT COALESCE(SUM(net_pay), 0) FROM payroll", fetch=True)[0][0]
            count = execute_query("SELECT COUNT(*) FROM payroll", fetch=True)[0][0]
            avg = total / count if count > 0 else 0
            
            data = {
                "💰 Total Payroll": f"",
                "📊 Total Records": count,
                "📈 Average Salary": f""
            }
            self.display_report(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load report: {str(e)}")

    def department_wise(self):
        try:
            data = [["Department", "Employees"]]
            rows = execute_query("""
                SELECT department, COUNT(*) 
                FROM employees 
                WHERE department IS NOT NULL 
                GROUP BY department
                ORDER BY COUNT(*) DESC
            """, fetch=True)
            
            for row in rows:
                data.append([row[0], row[1]])
            
            self.tree.heading('Metric', text='Department')
            self.tree.heading('Value', text='Employees')
            self.display_report(data)
            self.tree.heading('Metric', text='Metric')
            self.tree.heading('Value', text='Value')
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load report: {str(e)}")

    def all_reports(self):
        try:
            emp_count = execute_query("SELECT COUNT(*) FROM employees", fetch=True)[0][0]
            present = execute_query("SELECT COUNT(*) FROM attendance WHERE status='Present'", fetch=True)[0][0]
            pending = execute_query("SELECT COUNT(*) FROM leaves WHERE status='Pending'", fetch=True)[0][0]
            total_pay = execute_query("SELECT COALESCE(SUM(net_pay), 0) FROM payroll", fetch=True)[0][0]
            active_projects = execute_query("SELECT COUNT(*) FROM projects WHERE status='Active'", fetch=True)[0][0]
            total_apps = execute_query("SELECT COUNT(*) FROM applications", fetch=True)[0][0]
            
            data = {
                "📊 SUMMARY REPORT": "=" * 30,
                "👥 Total Employees": emp_count,
                "📅 Present Today": present,
                "🏖️ Pending Leave": pending,
                "💰 Total Payroll": f"",
                "📋 Active Projects": active_projects,
                "📝 Total Applications": total_apps,
                "=" * 30: "End of Report"
            }
            self.display_report(data)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load report: {str(e)}")

    def show_report(self):
        self.employee_count()
