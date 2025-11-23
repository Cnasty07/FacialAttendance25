import os
from time import time

# Styling and UI
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Local Imports
from build.lib.src.models.User import StudentUserSchema

# TODO: Implement Admin Panel functionality
    # 1. Need to implement adding/removing students and classes
    
class AdminPanel(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.built = False

    def build_ui(self) -> None:
        """Create widgets once when the panel is shown."""
        self.rowconfigure(0, weight=1, uniform="mainrows", pad=20)
        self.rowconfigure(1, weight=1, uniform="mainrows", pad=20)
        self.rowconfigure(2, weight=1, uniform="mainrows", pad=20)
        self.rowconfigure(3, weight=1, uniform="mainrows", pad=20)
        self.rowconfigure(4, weight=1, uniform="mainrows", pad=20)
        self.columnconfigure(0, weight=1, uniform="maincols", pad=10)
        self.columnconfigure(1, weight=1, uniform="maincols", pad=20)
        self.columnconfigure(2, weight=1, uniform="maincols")
        
        title = ttk.Label(self, text="Admin Panel", font= ("Arial", 18, "bold", "underline"))
        title.grid(row=0, column=0, columnspan=3, ipady=10)

        
        ttk.Button(self, text="Manage Users", command=self.manage_users,
            ).grid(row=1, column=0, ipady=10, ipadx=10)
        ttk.Button(self, text="View Reports", command=self.view_reports,
            ).grid(row=1, column=1, ipady=10, ipadx=10)
        
        ttk.Button(self, text="Add New Student", command=self.add_new_student).grid(row=1, column=2, ipady=10, ipadx=10)
        


        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=2, column=0, columnspan=3, rowspan=2, sticky="nsew", padx=10, pady=10)

        # create tabs
        self.classes_tab = ttk.Frame(self.notebook)
        self.students_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.classes_tab, text="Classes")
        self.notebook.add(self.students_tab, text="Students")

        self.classes_tab.rowconfigure(0, weight=1)
        self.classes_tab.columnconfigure(0, weight=1)
        self.students_tab.rowconfigure(0, weight=1)
        self.students_tab.columnconfigure(0, weight=1)

        self.classes_listbox = tk.Listbox(self.classes_tab)
        self.classes_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.classes_listbox.insert(tk.END, *[f"{clss['course_code']} : {clss['name']}" for clss in self.controller.all_classes])
        
        self.students_listbox = tk.Listbox(self.students_tab)
        self.students_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.students_listbox.insert(tk.END, *[f"{student['name']} : {student['email']}" for student in self.controller.all_students])
        
        self.built = True

    def on_show(self) -> None:
        """Called by the controller when this frame is shown."""
        if not self.built:
            self.build_ui()
        # refresh data if needed each time the frame is shown
        # self.refresh()


    def add_new_student(self) -> None:
        # Implement adding a new student (open new window or modal dialog)
        win = ttk.Toplevel(self.controller)
        win.transient(self.controller)
        win.grab_set()
        x = self.winfo_rootx() + self.winfo_width() // 2
        y = self.winfo_rooty() + self.winfo_height() // 2
        win.title("Add New Student")
        win.geometry(f"300x200-{x}+{y}")
        ttk.Label(win, text="Student Name:").pack(pady=10)
        name_entry = ttk.Entry(win, bootstyle=PRIMARY)
        name_entry.pack(pady=5)
        ttk.Label(win, text="Student Email:").pack(pady=10)
        email_entry = ttk.Entry(win, bootstyle=PRIMARY)
        email_entry.pack(pady=5)
        
        
        def submit() -> None:
            name = name_entry.get()
            email = email_entry.get()
            if name and email:
                new_student = StudentUserSchema(name=name, email=email, face_data=[])
                id = new_student.save()
                print(f"Added new student with ID: {id}")
                win.destroy()
        ttk.Button(win, text="Submit", command=submit).pack(pady=20)
    
    def manage_users(self) -> None:
        users = self.controller.all_students
        win = ttk.Toplevel(self)
        win.title("Manage Users")
        win.geometry("300x300")
        user_list = tk.Listbox(win)
        for user in users:
            user_list.insert(tk.END, user['name'])
        user_list.pack(fill="both", expand=True, padx=10, pady=10)

        user_list.bind("<<ListboxSelect>>", lambda event: print("Selected user:", user_list.get(user_list.curselection())))

    def view_reports(self) -> None:
        # Implement report viewing (open new window or populate this frame)
        pass

    # Refresh on certain commands
    def refresh(self) -> None:
        """Refresh the data displayed in the panel."""
        # Implement data refresh logic if needed
        pass

    def close(self) -> None:
        """Clean up resources when the application is closed."""
        self.winfo_toplevel().destroy()


def main() -> None:
    pass

if __name__ == '__main__':
    main()
