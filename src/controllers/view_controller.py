import tkinter as tk
from src import ui

# TODO: AppController to manage frames aka the different views of the application

# FIXME: Worked in the main.py file before, moving here for better organization and need to change activate from root to app: AppController later
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
            # (ui.new_interface.FacialAttendanceSystemApp, "FacialAttendanceSystemApp"),
        ):
            frame = F(container)
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

def main():
    pass

if __name__ == '__main__':
    main()