import os 
import sys
import dlib


from src.controllers.view_controller import AppController

# TODO: Finish Entry to application

# TODO: Test New Tkinter Frame Switching Mechanism, Add Switch User Button.


# -- Application Activation Function --
def activate(app) -> None:
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




    ## INFO: Using this with app controller to manage frames in later fix.
    app.geometry("800x600")
    app.title("Facial Attendance System")
    app.show_frame("ChooseUserPanel")
    app.protocol("WM_DELETE_WINDOW", app.destroy)
    
    ## Start GUI loop
    app.mainloop()

# -- END Application Activation Function --


# Terminates the application (will probably delete later as it serves limited use now).
def deactivate() -> None:
    sys.exit()


# Entry Point
def main() -> None:
    
    ## Ensure current working directory is in sys.path for module resolution.
    sys.path.append(os.getcwd())
    print("Current working directory: ", sys.path[0])
    
    ## Starts the application controller for frame switching and user interface management.
    app = AppController()
    activate(app)

if __name__ == '__main__':
    main()
