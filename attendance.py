import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import execute_query

class AttendanceFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_data()
        self.load_employees()

    def setup_ui(self):
        tk.Label(self, text="📅 Attendance Management", font=('Segoe UI', 20, 'bold'),
                fg='#2c3e50').pack(pady=10)

        toolbar = tk.Frame(self, bg='white')
        toolbar.pack(fill=tk.X, pady=5, padx=10)

        tk.Label(toolbar, text="Employee:", bg='white').pack(side=tk.LEFT, padx=5)
        self.emp_combo = ttk.Combobox(toolbar, width=25)
        self.emp_combo.pack(side=tk.LEFT, padx=5)

        tk.Label(toolbar, text="Date (YYYY-MM-DD):", bg='white').pack(side=tk.LEFT, padx=5)
        self.date_entry = tk.Entry(toolbar, width=15)
        self.date_entry.pack(side=tk.LEFT, padx=5)
        self.date_entry.insert(0, "2026-08-09")

        tk.Button(toolbar, text="✅ Check In", bg='#27ae60', fg='white',
                 command=self.add_attendance).pack(side=tk.LEFT, padx=5)

        columns = ('ID', 'Employee', 'Date', 'Check In', 'Check Out', 'Status')
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
        tk.Button(btn_frame, text="❌ Delete", bg='#e74c3c', fg='white',
                 command=self.delete_attendance).pack(side=tk.LEFT, padx=5)

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
                SELECT a.id, e.name, a.date, a.check_in, a.check_out, a.status
                FROM attendance a
                JOIN employees e ON a.employee_id = e.id
                ORDER BY a.date DESC, a.id DESC
            """
            rows = execute_query(query, fetch=True)
            
            for row in rows:
                check_in = row[3] if row[3] else '-'
                check_out = row[4] if row[4] else '-'
                self.tree.insert('', tk.END, values=(row[0], row[1], row[2], check_in, check_out, row[5]))
                
        except Exception as e:
            print(f"Error loading attendance: {e}")

    def add_attendance(self):
        try:
            emp_str = self.emp_combo.get()
            if not emp_str:
                messagebox.showerror("Error", "Please select an employee")
                return
            
            emp_id = emp_str.split(' - ')[0]
            date = self.date_entry.get().strip()
            
            if not date:
                messagebox.showerror("Error", "Please enter date")
                return
            
            existing = execute_query(
                "SELECT id FROM attendance WHERE employee_id=? AND date=?",
                (emp_id, date),
                fetch=True
            )
            
            if existing:
                messagebox.showerror("Error", "Attendance already recorded for this date")
                return
            
            query = """
                INSERT INTO attendance (employee_id, date, check_in, status)
                VALUES (?, ?, time('now'), 'Present')
            """
            execute_query(query, (emp_id, date))
            
            messagebox.showinfo("Success", "Check-in recorded successfully")
            self.load_data()
            
        except Exception as e:
            print(f"Error adding attendance: {e}")
            messagebox.showerror("Error", f"Failed to add attendance: {str(e)}")

    def delete_attendance(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a record to delete")
            return
        
        if messagebox.askyesno("Confirm", "Delete this attendance record?"):
            try:
                record_id = self.tree.item(selected[0])['values'][0]
                execute_query("DELETE FROM attendance WHERE id=?", (record_id,))
                self.load_data()
                messagebox.showinfo("Success", "Record deleted")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete: {str(e)}")
