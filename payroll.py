import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import execute_query

class PayrollFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_employees()
        self.load_data()

    def setup_ui(self):
        tk.Label(self, text="💰 Payroll Management", font=('Segoe UI', 20, 'bold'),
                fg='#2c3e50').pack(pady=10)

        form = tk.LabelFrame(self, text="Generate Payroll", font=('Segoe UI', 12, 'bold'))
        form.pack(fill=tk.X, padx=10, pady=5)

        row1 = tk.Frame(form)
        row1.pack(fill=tk.X, pady=5)
        tk.Label(row1, text="Employee:").pack(side=tk.LEFT, padx=5)
        self.emp_combo = ttk.Combobox(row1, width=25)
        self.emp_combo.pack(side=tk.LEFT, padx=5)
        tk.Label(row1, text="Month (YYYY-MM-01):").pack(side=tk.LEFT, padx=5)
        self.month_entry = tk.Entry(row1, width=15)
        self.month_entry.pack(side=tk.LEFT, padx=5)
        self.month_entry.insert(0, "2026-08-01")

        row2 = tk.Frame(form)
        row2.pack(fill=tk.X, pady=5)
        tk.Label(row2, text="Basic Salary:").pack(side=tk.LEFT, padx=5)
        self.basic_entry = tk.Entry(row2, width=15)
        self.basic_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(row2, text="Allowances:").pack(side=tk.LEFT, padx=5)
        self.allow_entry = tk.Entry(row2, width=15)
        self.allow_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(row2, text="Deductions:").pack(side=tk.LEFT, padx=5)
        self.ded_entry = tk.Entry(row2, width=15)
        self.ded_entry.pack(side=tk.LEFT, padx=5)

        btn_frame = tk.Frame(form)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="Calculate & Save", bg='#27ae60', fg='white',
                 command=self.add_payroll).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", bg='#95a5a6', fg='white',
                 command=self.clear_fields).pack(side=tk.LEFT, padx=5)

        columns = ('ID', 'Employee', 'Month', 'Basic', 'Allowances', 'Deductions', 'Net Pay')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)

        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=10)

        bottom_frame = tk.Frame(self)
        bottom_frame.pack(pady=5)
        tk.Button(bottom_frame, text="🔄 Refresh", bg='#3498db', fg='white',
                 command=self.load_data).pack(side=tk.LEFT, padx=5)
        tk.Button(bottom_frame, text="❌ Delete", bg='#e74c3c', fg='white',
                 command=self.delete_payroll).pack(side=tk.LEFT, padx=5)

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
                SELECT p.id, e.name, p.month_year, p.basic_salary, 
                       p.allowances, p.deductions, p.net_pay
                FROM payroll p
                JOIN employees e ON p.employee_id = e.id
                ORDER BY p.id DESC
            """
            rows = execute_query(query, fetch=True)
            for row in rows:
                self.tree.insert('', tk.END, values=row)
        except Exception as e:
            print(f"Error loading payroll: {e}")

    def add_payroll(self):
        try:
            emp_str = self.emp_combo.get()
            if not emp_str:
                messagebox.showerror("Error", "Please select an employee")
                return
            emp_id = emp_str.split(' - ')[0]
            month = self.month_entry.get().strip()
            basic = self.basic_entry.get().strip()
            allow = self.allow_entry.get().strip()
            ded = self.ded_entry.get().strip()
            if not all([month, basic, allow, ded]):
                messagebox.showerror("Error", "Please fill all fields")
                return
            basic = float(basic)
            allow = float(allow)
            ded = float(ded)
            net = basic + allow - ded
            query = """
                INSERT INTO payroll (employee_id, month_year, basic_salary, 
                                    allowances, deductions, net_pay, payment_date)
                VALUES (?, ?, ?, ?, ?, ?, date('now'))
            """
            execute_query(query, (emp_id, month, basic, allow, ded, net))
            messagebox.showinfo("Success", f"Payroll generated!\nNet Pay: ")
            self.clear_fields()
            self.load_data()
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for salary fields")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate payroll: {str(e)}")

    def clear_fields(self):
        self.basic_entry.delete(0, tk.END)
        self.allow_entry.delete(0, tk.END)
        self.ded_entry.delete(0, tk.END)

    def delete_payroll(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        if messagebox.askyesno("Confirm", "Delete this payroll record?"):
            try:
                record_id = self.tree.item(selected[0])['values'][0]
                execute_query("DELETE FROM payroll WHERE id=?", (record_id,))
                self.load_data()
                messagebox.showinfo("Success", "Record deleted")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")
