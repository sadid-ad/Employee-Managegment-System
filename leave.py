import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import execute_query

class LeaveFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_employees()
        self.load_data()

    def setup_ui(self):
        tk.Label(self, text="🏖️ Leave Management", font=('Segoe UI', 20, 'bold'),
                fg='#2c3e50').pack(pady=10)
        
        toolbar = tk.Frame(self, bg='white')
        toolbar.pack(fill=tk.X, pady=5, padx=10)

        tk.Label(toolbar, text="Employee:", bg='white').pack(side=tk.LEFT, padx=5)
        self.emp_combo = ttk.Combobox(toolbar, width=20)
        self.emp_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(toolbar, text="Leave Type:", bg='white').pack(side=tk.LEFT, padx=5)
        self.type_combo = ttk.Combobox(toolbar, width=15, values=['Annual', 'Sick', 'Casual', 'Maternity', 'Other'])
        self.type_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(toolbar, text="Start Date:", bg='white').pack(side=tk.LEFT, padx=5)
        self.start_entry = tk.Entry(toolbar, width=12)
        self.start_entry.pack(side=tk.LEFT, padx=5)
        self.start_entry.insert(0, "2026-08-09")

        tk.Label(toolbar, text="End Date:", bg='white').pack(side=tk.LEFT, padx=5)
        self.end_entry = tk.Entry(toolbar, width=12)
        self.end_entry.pack(side=tk.LEFT, padx=5)
        self.end_entry.insert(0, "2026-08-10")

        tk.Button(toolbar, text="Apply Leave", bg='#27ae60', fg='white',
                 command=self.apply_leave).pack(side=tk.LEFT, padx=5)

        columns = ('ID', 'Employee', 'Type', 'Start', 'End', 'Status')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        btn_frame = tk.Frame(self, bg='white')
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="🔄 Refresh", bg='#3498db', fg='white',
                 command=self.load_data).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✅ Approve", bg='#2ecc71', fg='white',
                 command=lambda: self.update_status('Approved')).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Reject", bg='#e74c3c', fg='white',
                 command=lambda: self.update_status('Rejected')).pack(side=tk.LEFT, padx=5)

    def load_employees(self):
        try:
            rows = execute_query("SELECT id, name FROM employees ORDER BY name", fetch=True)
            values = []
            for row in rows:
                values.append(str(row[0]) + " - " + str(row[1]))
            self.emp_combo['values'] = values
            if values:
                self.emp_combo.set(values[0])
        except Exception as e:
            print(f"Error loading employees: {e}")

    def load_data(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            query = """
                SELECT l.id, e.name, l.leave_type, l.start_date, l.end_date, l.status
                FROM leaves l
                JOIN employees e ON l.employee_id = e.id
                ORDER BY l.id DESC
            """
            rows = execute_query(query, fetch=True)
            
            for row in rows:
                self.tree.insert('', tk.END, values=row)
                
        except Exception as e:
            print(f"Error loading leaves: {e}")

    def apply_leave(self):
        try:
            emp_str = self.emp_combo.get()
            if not emp_str:
                messagebox.showerror("Error", "Please select an employee")
                return
            
            emp_id = emp_str.split(' - ')[0]
            leave_type = self.type_combo.get()
            start_date = self.start_entry.get().strip()
            end_date = self.end_entry.get().strip()
            
            if not leave_type or not start_date or not end_date:
                messagebox.showerror("Error", "Please fill all fields")
                return
            
            query = """
                INSERT INTO leaves (employee_id, leave_type, start_date, end_date, status)
                VALUES (?, ?, ?, ?, 'Pending')
            """
            execute_query(query, (emp_id, leave_type, start_date, end_date))
            
            messagebox.showinfo("Success", "Leave applied successfully")
            self.load_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply leave: {str(e)}")

    def update_status(self, status):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a leave request")
            return
        
        if messagebox.askyesno("Confirm", f"{status} this leave request?"):
            try:
                leave_id = self.tree.item(selected[0])['values'][0]
                execute_query("UPDATE leaves SET status=? WHERE id=?", (status, leave_id))
                self.load_data()
                messagebox.showinfo("Success", f"Leave {status}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {str(e)}")
