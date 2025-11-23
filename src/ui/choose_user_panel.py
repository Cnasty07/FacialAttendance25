import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# INFO: This panel allows the user to choose between Admin and User modes. Rather than doing it from the CLI.
## It will then call the controller to switch frames accordingly.

# -- Choose User Panel --
class ChooseUserPanel(ttk.Frame):
    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.controller = controller
        print("Controller: ",self.controller.remote)
        print(type(self.controller))
        print("Tester : ",self.winfo_width(), self.winfo_height())

        # Grid Configuration
        self.grid_rowconfigure(0, weight=1, uniform="mainrows", pad=10)
        self.grid_rowconfigure(1, weight=1, uniform="mainrows", pad=10)
        self.grid_columnconfigure(0, weight=1, uniform="maincols", pad=10)
        self.grid_columnconfigure(1, weight=1, uniform="maincols", pad=10)
        self.built = False

    def build_ui(self) -> None:
        """Create widgets once when the panel is shown."""
    
        # --- Title ---
        title = ttk.Label(self, text="Who Are You?", font=("Arial", 28, "bold"), bootstyle="inverse-light")
        # Increase the font size for emphasis
        title.grid(row=0, columnspan=2, pady=30) # Add vertical padding

        # --- Style Configuration (using a custom outline style for better visual) ---
        self.style = ttk.Style()
        # Configure the standard TButton styles for larger font
        self.style.configure("TButton", font=("Helvetica", 18, "bold")) 
        
        # Optional: Configure a style that looks more like a filled panel (less border)
        self.style.configure("Admin.TButton", background="#213a5a", foreground="white", focuscolor=self.style.lookup("primary.TButton", "focuscolor"))

        self.style.configure("Student.TButton", background="#00a373", foreground="white", focuscolor=self.style.lookup("success.TButton", "focuscolor"))
        
        # --- Buttons (Full Panel) ---
        self.admin_button = ttk.Button(self, text="Admin", command=self.admin_selected, bootstyle=PRIMARY) # Using standard bootstyle
        
        # The sticky="nsew" combined with grid_columnconfigure/grid_rowconfigure (weight=1) 
        # makes the button fill the entire cell in row 1, column 0.
        self.admin_button.grid(row=1, column=0, sticky="nsew") 

        self.user_button = ttk.Button(self, text="Student", command=self.user_selected, bootstyle=SUCCESS) # Using standard bootstyle
        
        self.user_button.grid(row=1, column=1, sticky="nsew")
    
        # --- Add Hover Effect ---
        self.setup_hover_effects() # Call the new method
    
        self.built = True
    def setup_hover_effects(self) -> None:
        """Binds mouse events to buttons to create a hover effect."""
        
        # Admin Button Hover
        self.admin_button.bind("<Enter>", lambda event: self.on_hover_enter(self.admin_button, "primary-outline"))
        self.admin_button.bind("<Leave>", lambda event: self.on_hover_leave(self.admin_button, "primary"))
        
        # Student Button Hover
        self.user_button.bind("<Enter>", lambda event: self.on_hover_enter(self.user_button, "success-outline"))
        self.user_button.bind("<Leave>", lambda event: self.on_hover_leave(self.user_button, "success"))
    
    def on_hover_enter(self, widget: ttk.Button, bootstyle: str) -> None:
        """Changes the widget's bootstyle to an outline style on mouse entry."""
        widget.configure(bootstyle=bootstyle)
        widget.config(cursor="hand2") # Change cursor to a hand pointer
        
    def on_hover_leave(self, widget: ttk.Button, bootstyle: str) -> None:
        """Changes the widget's bootstyle back to the solid style on mouse exit."""
        widget.configure(bootstyle=bootstyle)
        widget.config(cursor="") # Reset cursor

    def on_show(self) -> None:
        """Called by the controller when this frame is shown."""
        if not self.built:
            self.build_ui()
        # additional refresh logic could go here

    # Admin Selected Handler.
    def admin_selected(self) -> bool:
        print("Admin selected")
        if self.controller:
            try:
                self.controller.show_frame("AdminPanel")
            except Exception as e:
                print("Error switching to AdminPanel:", e)
        return True

    # User Selected Handler.
    def user_selected(self) -> bool:
        print("User selected")

        # Prompt for email and switch to FacialStudentPanel
        if self.controller:
            try:
                # Prompt for email in a modal dialog
                x = self.winfo_rootx() + self.winfo_width() // 2
                y = self.winfo_rooty() + self.winfo_height() // 2
                win = ttk.Toplevel(self.controller)
                win.title("Enter Email")
                win.geometry(f"350x160-{x}+{y}")
                win.resizable(False, False)
                ttk.Label(win, text="Please enter your email:", font=("Arial", 11)).pack(pady=(10, 5), padx=10)

                email_var = ttk.StringVar()
                entry = ttk.Entry(win, textvariable=email_var, width=40, font=("Arial", 10), bootstyle=PRIMARY)
                entry.pack(padx=10)
                entry.focus_set()
                
                switch_var = ttk.BooleanVar(value=False) # var to swith view on successful email entry
                def submit_email():
                    email = email_var.get().strip()
                    if email:
                        print("Email entered:", email)
                        # Test user shortcut
                        if email =="em@tamusa.edu":
                            from src.models.User import StudentUserSchema
                            id = None
                            if self.controller.remote.get_student(email) is None:
                                # Create test user if not exists
                                test_user = StudentUserSchema(
                                    name="Elon Musk",
                                    email="em@tamusa.edu",
                                    face_data=[],
                                )
                                id = test_user.save()
                            else:
                                student = self.controller.get_single_student(email)
                                self.controller.set_student(student)
                                print("Test user logged in. : ", self.controller.student, type(self.controller.student))
                                switch_var.set(True)
                        # Normal User Flow
                        else:
                            student = self.controller.get_single_student(email)
                            # self.controller.set_student(self.controller.student) # Unsure if i need to set it again here
                            if not student:
                                print("No student found with that email.")
                                ttk.Label(win, text="No student found with that email.", bootstyle=DANGER,font=("Arial", 10)).pack(pady=5)
                                return
                            print("Student fetched:", student["name"])
                            self.controller.student = student
                            self.controller.set_student(student)
                            switch_var.set(True)
                            
                    # If controller supports receiving the email, pass it along.
                    if self.controller and hasattr(self.controller, "set_user_email"):
                        try:
                            self.controller.set_user_email(email)
                        except Exception:
                            pass
                    win.destroy()

                btn_frame = ttk.Frame(win, bootstyle=DEFAULT)
                btn_frame.pack(pady=8)
                ttk.Button(btn_frame, text="OK", width=10, command=submit_email, bootstyle=SUCCESS).pack(side="left", padx=5)
                ttk.Button(btn_frame, text="Cancel", width=10, command=win.destroy, bootstyle=DANGER).pack(side="left", padx=5)

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

    # Clean up resources on close
    def close(self) -> None:
        """Clean up resources when the application is closed."""
        self.winfo_toplevel().destroy()





# -- END Choose User Panel --

def main() -> None:
    pass

if __name__ == '__main__':
    main()
