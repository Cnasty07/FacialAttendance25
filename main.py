import os 
import sys
import cv2
import face_recognition
import dlib
import tkinter as tk

from src import ui


### TODO: Finish Entry to application


def activate(root):
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

    # Starts the interface
    user_type = input("Enter user type (admin/user): ").strip().lower()
    if user_type == "admin":
        admin_panel = ui.admin_panel.AdminPanel(root)
        root.protocol("WM_DELETE_WINDOW", admin_panel.close)
        root.mainloop()
    elif user_type == "user":
        check_in = ui.new_interface.FacialAttendanceSystemApp(root)
        root.protocol("WM_DELETE_WINDOW", check_in.close)
        root.mainloop()
    else:
        print("Invalid user type. Exiting.")
        return


def deactivate():
    exit()


def main():
    sys.path.append(os.getcwd())
    print("Current working directory: ", sys.path[0])
    activate(tk.Tk())

if __name__ == '__main__':
    main()
