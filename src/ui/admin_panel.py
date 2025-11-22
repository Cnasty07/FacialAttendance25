import os
from time import time
import tkinter as tk

from build.lib.src.models.User import StudentUserSchema

# TODO: Implement Admin Panel functionality
    # 1. Need to get and show all classes
    # 2. Need to get and show all students
    # 3. Need to implement adding/removing students and classes

class AdminPanel(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        self.built = False

    def build_ui(self) -> None:
        """Create widgets once when the panel is shown."""
        self.configure(background="grey")
        
        title = tk.Label(self, text="Admin Panel",
                         bg="grey", font=("Arial", 18))
        title.pack(pady=20)
        tk.Button(self, text="Manage Users", command=self.manage_users,
                  width=50, height=2, font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="View Reports", command=self.view_reports,
                  width=50, height=2, font=("Arial", 14)).pack(pady=10)
        
        tk.Button(self,background="green", text="Add New Student", command=self.add_new_student, width=50, height=2, font=("Arial", 14)).pack(pady=10)
        
        self.built = True



        # Display List of Classes in raw format
        classes_list = tk.Text(self, height=100, width=100,
                bg="grey", font=("Arial", 12), fg="white")
        for clss in self.controller.all_classes:
            classes_list.insert(tk.END, f"_id: {clss['_id']} : [{clss['course_code']} : {clss['name']}, Start time: {clss['start_time'].time()} : End time {clss['end_time'].time()}]\n")
        classes_list.pack(fill="both", pady=20, expand=True)


    def on_show(self) -> None:
        """Called by the controller when this frame is shown."""
        if not self.built:
            self.build_ui()
        # refresh data if needed each time the frame is shown
        # self.refresh()


    def add_new_student(self) -> None:
        # Implement adding a new student (open new window or modal dialog)
        win = tk.Toplevel(self)
        win.title("Add New Student")
        win.geometry("300x200")
        tk.Label(win, text="Student Name:").pack(pady=10)
        name_entry = tk.Entry(win)
        name_entry.pack(pady=5)
        tk.Label(win, text="Student Email:").pack(pady=10)
        email_entry = tk.Entry(win)
        email_entry.pack(pady=5)
        
        
        def submit() -> None:
            name = name_entry.get()
            email = email_entry.get()
            if name and email:
                new_student = StudentUserSchema(name=name, email=email, face_data=[])
                id = new_student.save()
                print(f"Added new student with ID: {id}")
                win.destroy()
        tk.Button(win, text="Submit", command=submit).pack(pady=20)
    
    def manage_users(self) -> None:
        users = self.controller.all_students
        win = tk.Toplevel(self)
        win.title("Manage Users")
        win.geometry("300x300")
        user_list = tk.Listbox(win)
        for user in users:
            user_list.insert(tk.END, user['name'])
        user_list.pack(fill="both", expand=True, padx=10, pady=10)

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
    root = tk.Tk()
    root.title("Admin Panel")
    root.geometry("600x400")
    
    app = AdminPanel(root)
    app.on_show()
    app.pack(fill="both", expand=True)
    
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


if __name__ == '__main__':
    main()
