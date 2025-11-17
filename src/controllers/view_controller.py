import tkinter as tk
from src import ui



# TODO: New Frame Switching Mechanism with lazy-loading and on_show hooks. Needs Testing For Functionality.

# -- Application Controller for Frame Management --
class AppController(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Facial Attendance System")
        
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
            # pass controller so panels can call controller.show_frame(...)
            frame = F(container, controller=self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, cont):
        frame = self.frames[cont]
        if not frame:
            print(f"Frame {cont} not found!")
            return
        frame.tkraise()
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

# -- END Application Controller for Frame Management --
