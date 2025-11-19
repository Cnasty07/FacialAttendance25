import tkinter as tk
from src import ui

# Testing Adding Variables to Frames and Passing Data Between Frames
from src.models.User import StudentUserModel, AdminUserModel
from src.controllers.facialController import FacialController
from src.controllers.remoteDatabaseController import remoteController

# Controller that is the parent/root of the tkinter GUI. Methods to switch frames and fetch data from remote controller.

# TODO: New Frame Switching Mechanism with lazy-loading and on_show hooks. Needs Testing For Functionality.

# -- Application Controller for Frame Management --
class AppController(tk.Tk):
    def __init__(self, facialController=None, studentModel=None, adminModel=None) -> None:
        super().__init__()
        self.remote = remoteController() # Remote DB Controller Instance
        self.all_classes = self.remote.get_all_classes() # Pre-fetch classes for initial use


        # Setting up main window and container for frames
        self.title("Facial Attendance System")
        self.geometry("800x600")

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
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

    def get_classes(self):
        """Fetch classes from remote controller and return them (prints for debugging)."""
        try:
            classes_list = self.remote.get_all_classes()
            print("Classes Retrieved:", classes_list)
            return classes_list
        except Exception as e:
            print("Error retrieving classes:", e)
            return []

    ## --- Student Related Methods --- ##
    def get_single_student(self, student_email: str):
        """Fetch student data from remote controller (example function)."""
        print("Fetching student with email:", student_email)
        try:
            student = self.remote.get_student(student_email)
            print("Student Retrieved:", student)
            return student
        except Exception as e:
            print("Error retrieving student:", e)
            return None

    # Getting all Students from Student Collection
    def get_all_students(self):
        """Fetch all students from remote controller (example function)."""
        try:
            students = self.remote.get_all_students()
            print("Students Retrieved:", students)
            return students
        except Exception as e:
            print("Error retrieving students:", e)
            return []
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
            print("Refreshed: ", self.all_classes)
            print("Switched to AdminPanel.")

        if cont == "FacialStudentPanel":
            # all_classes = self.get_classes()
            # print("Refreshed: ", all_classes)
            print("Switched to FacialStudentPanel.")

# -- END Application Controller for Frame Management --
