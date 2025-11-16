import os 
import sys
import dlib
import tkinter as tk

from src import ui

# getting ready to remove these as not needed here
# import cv2 
# import face_recognition

# TODO: Finish Entry to application


# -- Application Activation Function --
def activate(root: tk.Tk) -> None:
    """_summary_
    starts the facial recognition system.
    """
    # adds the CUDA path to the system path and sets dlib to use CUDA
    try:
        os.add_dll_directory(os.environ['CUDA_PATH'])
        dlib.DLIB_USE_CUDA = True
        print("Cuda detected. Using GPU acceleration.")
    except Exception as e:
        print("Cuda not detected. Defaulting to cpu.", e)




    # INFO: Using this with app controller to manage frames in later fix.
    # app.show_frame("ChooseUserPanel")
    # app.mainloop()


        
    # --- Starts the interface: CLI input required at the moment to choose admin or user ---
    user_type = input("Enter user type (admin/user): ").strip().lower()

    ## Changes window based on user type
    def change_window(user_type: str) -> None:    

        ### Option 1: Admin Panel
        if user_type == "admin":
            #### FIXME: Temporary fix until AppController is implemented
            root.title("Admin Panel")
            root.geometry("600x400")
            
            admin_panel = ui.admin_panel.AdminPanel(root)
            admin_panel.on_show() # Will build UI but later on the controller will handle this.
            admin_panel.pack(fill="both", expand=True) # This as well

            root.protocol("WM_DELETE_WINDOW", admin_panel.close)

        ### Option 2: User Facial Attendance Panel
        elif user_type == "user":
            ## TODO: Open Database Connection Here
            #### FIXME: Still on old root UI for testing purposes
            check_in = ui.new_interface.FacialAttendanceSystemApp(root)
            root.protocol("WM_DELETE_WINDOW", check_in.close)
        else:
            print("Invalid user type. Exiting.")
            return sys.exit(1)

    change_window(user_type)
    root.mainloop()

# -- END Application Activation Function --


# Terminates the application (will probably delete later as it serves limited use now).
def deactivate():
    sys.exit()


# Entry Point
def main() -> None:
    sys.path.append(os.getcwd())
    print("Current working directory: ", sys.path[0])
    root = tk.Tk()
    activate(root)

    # FIXME: Change to AppController Later
    # app = AppController()
    # activate(app)

if __name__ == '__main__':
    main()
