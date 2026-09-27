import tkinter as tk
from tkinter import ttk, messagebox
from db_utils import execute_query

class TrainingFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        self.load_data()

    def setup_ui(self):
        tk.Label(self, text="📚 Training Management", font=('Segoe UI', 20, 'bold'),
                fg='#2c3e50').pack(pady=10)

        form = tk.LabelFrame(self, text="Add New Training", font=('Segoe UI', 10, 'bold'))
        form.pack(fill=tk.X, padx=10, pady=5)

        row1 = tk.Frame(form)
        row1.pack(fill=tk.X, pady=5)
        tk.Label(row1, text="Title:").pack(side=tk.LEFT, padx=5)
        self.title_entry = tk.Entry(row1, width=25)
        self.title_entry.pack(side=tk.LEFT, padx=5)
        tk.Label(row1, text="Trainer:").pack(side=tk.LEFT, padx=5)
        self.trainer_entry = tk.Entry(row1, width=20)
        self.trainer_entry.pack(side=tk.LEFT, padx=5)

        row2 = tk.Frame(form)
        row2.pack(fill=tk.X, pady=5)
        tk.Label(row2, text="Description:").pack(side=tk.LEFT, padx=5)
        self.desc_entry = tk.Entry(row2, width=40)
        self.desc_entry.pack(side=tk.LEFT, padx=5)

        row3 = tk.Frame(form)
        row3.pack(fill=tk.X, pady=5)
        tk.Label(row3, text="Start Date:").pack(side=tk.LEFT, padx=5)
        self.start_entry = tk.Entry(row3, width=15)
        self.start_entry.pack(side=tk.LEFT, padx=5)
        self.start_entry.insert(0, "2026-08-15")
        tk.Label(row3, text="End Date:").pack(side=tk.LEFT, padx=5)
        self.end_entry = tk.Entry(row3, width=15)
        self.end_entry.pack(side=tk.LEFT, padx=5)
        self.end_entry.insert(0, "2026-08-20")
        tk.Button(row3, text="Add Training", bg='#27ae60', fg='white',
                 command=self.add_training).pack(side=tk.LEFT, padx=5)

        columns = ('ID', 'Title', 'Trainer', 'Start', 'End', 'Status')
        self.tree = ttk.Treeview(self, columns=columns, show='headings', height=12)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120)
        scrollbar = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar.pack(side=tk.RIGHT, fill='y', pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)
        tk.Button(btn_frame, text="🔄 Refresh", bg='#3498db', fg='white',
                 command=self.load_data).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="✅ Complete", bg='#2ecc71', fg='white',
                 command=self.mark_complete).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="❌ Cancel", bg='#e74c3c', fg='white',
                 command=self.cancel_training).pack(side=tk.LEFT, padx=5)

    def load_data(self):
        try:
            for item in self.tree.get_children():
                self.tree.delete(item)
            rows = execute_query("SELECT id, title, trainer, start_date, end_date, status FROM training", fetch=True)
            for row in rows:
                self.tree.insert('', tk.END, values=row)
        except Exception as e:
            print(f"Error loading training: {e}")

    def add_training(self):
        title = self.title_entry.get().strip()
        trainer = self.trainer_entry.get().strip()
        desc = self.desc_entry.get().strip()
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required")
            return
        try:
            query = "INSERT INTO training (title, description, trainer, start_date, end_date) VALUES (?, ?, ?, ?, ?)"
            execute_query(query, (title, desc, trainer, start, end))
            messagebox.showinfo("Success", "Training added!")
            self.title_entry.delete(0, tk.END)
            self.trainer_entry.delete(0, tk.END)
            self.desc_entry.delete(0, tk.END)
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add training: {str(e)}")

    def mark_complete(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a training to complete")
            return
        if messagebox.askyesno("Confirm", "Mark this training as completed?"):
            try:
                training_id = self.tree.item(selected[0])['values'][0]
                execute_query("UPDATE training SET status='Completed' WHERE id=?", (training_id,))
                self.load_data()
                messagebox.showinfo("Success", "Training marked as completed")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update: {str(e)}")

    def cancel_training(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a training to cancel")
            return
        if messagebox.askyesno("Confirm", "Cancel this training?"):
            try:
                training_id = self.tree.item(selected[0])['values'][0]
                execute_query("UPDATE training SET status='Cancelled' WHERE id=?", (training_id,))
                self.load_data()
                messagebox.showinfo("Success", "Training cancelled")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to cancel: {str(e)}")
