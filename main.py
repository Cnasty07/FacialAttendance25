import os 
import sys

from utils import gpu_detection
from src.controllers.view_controller import AppController

# TODO: Finish Entry to application

# TODO: Test New Tkinter Frame Switching Mechanism, Add Switch User Button.


# -- Application Activation Function --
def activate(app) -> None:
    """_summary_
    starts the facial recognition system.
    """
    gpu_detection.is_gpu_available() # Check for GPU availability


    ## -- Setup Main Application Window --
    app.geometry("800x600")
    app.title("Facial Attendance System")
    app.show_frame("ChooseUserPanel")
    app.protocol("WM_DELETE_WINDOW", app.destroy)
    
    ## Start GUI loop
    app.mainloop()
    ## -- END Setup Main Application Window --
    
# -- END Application Activation Function --


# Terminates the application (will probably delete later as it serves limited use now).
def deactivate() -> None:
    sys.exit()


# Entry Point For Application
def main() -> None:
    
    sys.path.append(os.getcwd()) # Ensure current working directory is in sys.path for module resolution.
    print("Current working directory: ", sys.path[0])
    
    ## Starts the application controller for frame switching and user interface management.
    app = AppController()
    activate(app)

if __name__ == '__main__':
    main()
