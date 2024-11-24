import os
import cv2
import dlib
from .facialSystem import facial_controller
from .ui import new_interface

#main code 
def activate():
    """_summary_
    starts the facial recognition system.
    """
    # adds the CUDA path to the system path and sets dlib to use CUDA
    os.add_dll_directory(os.environ['CUDA_PATH'])
    dlib.DLIB_USE_CUDA = True
    
    facial_controller.FacialController

    # loop to check everyone in until done.
    while True:
        
        # starts the interface
        check_in = new_interface.FacialAttendanceSystemApp()
        
        



    
    


def deactivate():
    exit()
    

def main():
    activate()

if __name__ == '__main__':
    main() 
