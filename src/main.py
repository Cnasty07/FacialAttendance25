import os
import cv2
import dlib

#main code 
def activate():
    """_summary_
    starts the facial recognition system.
    """
    # adds the CUDA path to the system path and sets dlib to use CUDA
    os.add_dll_directory(os.environ['CUDA_PATH'])
    dlib.DLIB_USE_CUDA = True
    
    # start the capture of face from the camera or stored image
    
    # step 1: capture face
    
    # step 2: compare face
    # step 3: return result
    # step 4: if match, return name and check in
    # step 5: if no match, return no match and alert to try again
    


def deactivate():
    exit()
    

def main():
    activate()

if __name__ == '__main__':
    main() 
