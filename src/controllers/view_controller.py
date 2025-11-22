import tkinter as tk
import tkinter.ttk as ttk
from src import ui

# Testing Adding Variables to Frames and Passing Data Between Frames
from src.models.User import AdminUserModel , StudentUserSchema
from src.models.Classes import ClassesSchema
from typing import Any

from src.controllers.facialController import FacialController
from src.controllers.remoteDatabaseController import remoteController

# Controller that is the parent/root of the tkinter GUI. Methods to switch frames and fetch data from remote controller.

# TODO: New Frame Switching Mechanism with lazy-loading and on_show hooks. Needs Testing For Functionality.

# -- Application Controller for Frame Management --
class AppController(tk.Tk):
    def __init__(self, remoteClient: remoteController) -> None:
        super().__init__()
        # Initialize Local Scripts & Models
        self.remote: remoteController = remoteClient # Remote DB Controller Instance
        self.all_classes: list[ClassesSchema] = self.remote.get_all_classes() # Pre-fetch classes for initial use
        self.all_students: list[StudentUserSchema] = self.remote.get_all_students() # Pre-fetch students for initial use
        self.student: StudentUserSchema = StudentUserSchema()
        # self.admin = AdminUserModel

        # Setting up main window and container for frames
        self.title("Facial Attendance System")
        
        # Center the window on the screen
        self.swidth = int(self.winfo_screenwidth()/2 - 400)
        self.sheight = int(self.winfo_screenheight()/2 - 300)
        print("Screen Width:", self.swidth, "Screen Height:", self.sheight)
        self.geometry(f"800x600+{self.swidth}+{self.sheight}")
        # self.minsize(800, 600)
        # self.maxsize(800, 600)
        ## Menu to switch user types
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)
        
        switch_menu = tk.Menu(self.menubar, tearoff=0)
        switch_menu.add_command(label="Switch User Type", command=self.switch_user)
        self.menubar.add_cascade(label="View", menu=switch_menu)
        
        # Set ttk theme
        self.style = ttk.Style(self)
        print(self.style.theme_names())
        self.style.theme_use("aqua")
        
        # self.grid_rowconfigure(0, weight=1)
        # self.grid_columnconfigure(0, weight=1)

        # Container for all frames
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid(row=0, column=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        self.frames = {}

        for F, name in (
            (ui.choose_user_panel.ChooseUserPanel, "ChooseUserPanel"),
            (ui.admin_panel.AdminPanel, "AdminPanel"),
            (ui.facial_student_panel.FacialStudentPanel, "FacialStudentPanel"),
        ):
            frame = F(container, controller=self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # optionally show initial frame
        self.show_frame("ChooseUserPanel")
        
        
    def switch_user(self) -> None:
        """Switch back to the Choose User Panel."""
        self.show_frame("ChooseUserPanel")

    ## --- Student Related Methods --- ##
    def get_single_student(self, student_email: str) -> StudentUserSchema | None:
        """Fetch student data from remote controller (example function)."""
        print("Fetching student with email:", student_email)
        try:
            student = self.remote.get_student(student_email)
            self.student = student  # Store retrieved student
            print("Student Retrieved:", student)
            return student
        except Exception as e:
            print("Error retrieving student:", e)
            return None

    # Setting the current student in the controller
    def set_student(self, student: StudentUserSchema):
        """Set the current student (example function)."""
        self.student = student
        print("Current student set to:", self.student)

    # Loading student data into the application
    def load_student(self):
        """Load student data into the application (example function)."""
        try:
            if not self.student:
                print("No student set to load.")
                return None
            # Simulate loading student data
            return self.student
        except Exception as e:
            print("Error loading student data:", e)
            return None

    ## --- END Student Related Methods --- ##

    def show_frame(self, cont):
        frame = self.frames.get(cont)
        if not frame:
            print(f"Frame {cont} not found!")
            return
        frame.tkraise()

        # lazy-build / refresh hook
        if hasattr(frame, "on_show"):
            try:
                frame.on_show()
            except Exception as e:
                print(f"Error in on_show for {cont}: {e}")

        # example: automatically refresh classes when showing the AdminPanel
        if cont == "AdminPanel":
            print("Switched to AdminPanel.")

        if cont == "FacialStudentPanel":
            print("Switched to FacialStudentPanel.")

# -- END Application Controller for Frame Management --
