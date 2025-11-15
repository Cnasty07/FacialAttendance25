import os
import tkinter as tk
import src.controllers.databaseController as db
import pandas as pd

# TODO: Implement Admin Panel functionality


class AdminPanel(tk.Frame):
    def __init__(self, parent, controller=None) -> None:
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
        self.built = True

    def on_show(self) -> None:
        """Called by the controller when this frame is shown."""
        if not self.built:
            self.build_ui()
        # refresh data if needed each time the frame is shown
        # self.refresh()

    def manage_users(self) -> None:
        # Replace with db.StudentTable().read_all()
        users = ["Chris", "Ruben", "Alice", "Bob"]
        win = tk.Toplevel(self)
        win.title("Manage Users")
        win.geometry("300x300")
        user_list = tk.Listbox(win)
        for user in users:
            user_list.insert(tk.END, user)
        user_list.pack(fill="both", expand=True, padx=10, pady=10)

    def view_reports(self) -> None:
        # Implement report viewing (open new window or populate this frame)
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
