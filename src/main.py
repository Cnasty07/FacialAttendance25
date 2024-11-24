import os
import cv2
import dlib
from .facialSystem import facial_controller

#main code 
def activate():
    """_summary_
    starts the facial recognition system.
    """
    # adds the CUDA path to the system path and sets dlib to use CUDA
    os.add_dll_directory(os.environ['CUDA_PATH'])
    dlib.DLIB_USE_CUDA = True
    
    # start the capture of face from the camera or stored image
    facial_controller.start_new_entry()
    
    


def deactivate():
    exit()
    

def main():
    activate()

if __name__ == '__main__':
    main() 
