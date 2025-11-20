import tkinter as tk

# INFO: This panel allows the user to choose between Admin and User modes. Rather than doing it from the CLI.
## It will then call the controller to switch frames accordingly.

# -- Choose User Panel --
class ChooseUserPanel(tk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        print("Controller: ",self.controller.remote)
        self.built = False

    def build_ui(self) -> None:
        """Create widgets once when the panel is shown."""
        self.configure(background="lightblue")
        title = tk.Label(self, text="Choose User Type Panel",
                         bg="lightblue", font=("Arial", 16))
        title.pack(pady=20)
        tk.Button(self, text="Admin", command=self.admin_selected,
                  width=20, height=2, font=("Arial", 12)).pack(pady=10)
        tk.Button(self, text="User", command=self.user_selected,
                  width=20, height=2, font=("Arial", 12)).pack(pady=10)
        self.built = True

    def on_show(self) -> None:
        """Called by the controller when this frame is shown."""
        if not self.built:
            self.build_ui()
        # additional refresh logic could go here

    def admin_selected(self) -> bool:
        print("Admin selected")
        if self.controller:
            try:
                self.controller.show_frame("AdminPanel")
            except Exception as e:
                print("Error switching to AdminPanel:", e)
        return True

    def user_selected(self) -> bool:
        print("User selected")

        # Prompt for email and switch to FacialStudentPanel
        if self.controller:
            try:
                # Prompt for email in a modal dialog
                win = tk.Toplevel(self)
                win.title("Enter Email")
                win.geometry("350x130")
                win.resizable(False, False)
                tk.Label(win, text="Please enter your email:", font=("Arial", 11)).pack(pady=(10, 5), padx=10)

                email_var = tk.StringVar()
                entry = tk.Entry(win, textvariable=email_var, width=40, font=("Arial", 10))
                entry.pack(padx=10)
                entry.focus_set()
                
                switch_var = tk.BooleanVar(value=False) # var to swith view on successful email entry
                def submit_email():
                    email = email_var.get().strip()
                    if email:
                        print("Email entered:", email)
                        if email =="em@tamusa.edu":
                            print("Controller student type : ", type(self.controller.student))
                            self.controller.student = dict(
                                _id=123456,
                                name="Elon Musk",
                                email="em@tamusa.edu",
                                face_data=[]
                            )
                            self.controller.set_student(self.controller.student)
                            print("Test user logged in. : ", self.controller.student, type(self.controller.student))
                            switch_var.set(True)
                        else:
                            student = self.controller.get_single_student(email)
                            self.controller.set_student(self.controller.student)
                            print("Student fetched:", student["name"])
                            self.controller.student = student
                            
                            if not student:
                                print("No student found with that email.")
                                tk.Label(win, text="No student found with that email.", fg="red", font=("Arial", 10)).pack(pady=5)
                                return
                            switch_var.set(True)
                            
                    # If controller supports receiving the email, pass it along.
                    if self.controller and hasattr(self.controller, "set_user_email"):
                        try:
                            self.controller.set_user_email(email)
                        except Exception:
                            pass
                    win.destroy()

                btn_frame = tk.Frame(win)
                btn_frame.pack(pady=8)
                tk.Button(btn_frame, text="OK", width=10, command=submit_email).pack(side="left", padx=5)
                tk.Button(btn_frame, text="Cancel", width=10, command=win.destroy).pack(side="left", padx=5)

                # Make dialog modal
                win.transient(self.winfo_toplevel())
                win.grab_set()
                self.winfo_toplevel().wait_window(win)
                # target name should match the key used in AppController
                if switch_var.get():
                    self.controller.show_frame("FacialStudentPanel")
                
            except Exception as e:
                print("Error switching to user panel:", e)
        return True

    def close(self) -> None:
        """Clean up resources when the application is closed."""
        self.winfo_toplevel().destroy()

# -- END Choose User Panel --

def main() -> None:
    
    # root = tk.Tk()
    # root.title("Choose User Panel")
    # root.geometry("400x300")
    # # When used standalone, controller can be None
    # app = ChooseUserPanel(root)
    # app.on_show()
    # app.pack(fill="both", expand=True)
    
    # root.protocol("WM_DELETE_WINDOW", app.close)
    # root.mainloop()
    pass

if __name__ == '__main__':
    main()
