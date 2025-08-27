import os 
import tkinter as tk
import src.controllers.databaseController as db
import pandas as pd

## TODO: Implement Admin Panel functionality
class AdminPanel():
    def __init__(self,root) -> None:
        self.root = root
        tk.Label(text="Admin Panel").pack()

    def run(self) -> None:
        self.root = tk.Tk()
        self.root.title("Admin Panel")
        self.root.geometry("800x600")
        self.root.configure(background="grey")
        tk.Label(text="Admin Panel").pack(pady=20)
        tk.Button(text="Manage Users", command=self.manage_users,width=50,height=5,font=("Arial", 14)).pack(pady=10)
        tk.Button(text="View Reports", command=self.view_reports,width=50,height=5,font=("Arial", 14)).pack(pady=10)

    def manage_users(self) -> None:
        users = db.StudentTable().read_all()
        user_list = tk.Listbox()
        for user in users:
            user_list.insert(tk.END, user)
        user_list.pack()

    def view_reports(self) -> None:
        pass
    
    def close(self):
        """Clean up resources when the application is closed."""
        self.root.destroy()


def main() -> None:
    admin_panel = AdminPanel(tk.Tk())
    admin_panel.run()


if __name__ == '__main__':
    main()