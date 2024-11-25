import os
import face_recognition
import dlib
import numpy as np
import pandas as pd
import components.capture as cap
import components.comparison as comp
import components.recognition as rec

# import components for facial system
# from components.capture import Capture
# from components.comparison import FacialComparison
# from components.recognition import FacialRecognition

# TODO: Need to fix some boilerplate code


class FacialController:
    def __init__(self, known_faces_dir):
        self.known_faces_dir = known_faces_dir
        self.known_faces = self.load_known_faces()

    # starts the process of checking in a student
    def start_new_entry(self, capture_method: str = None):
        try :
            # step 1: capture face
            capture = self.capture_entry(capture_method)
            # step 2: process image
            comparison_data = self.process_image(capture)
            # step 3: match face
            match = self.match_processed_image(comparison_data)
        except Exception as e:
            print("Error: ", e)
            print("Could not start new entry. Please try again.")

        return "Check in complete."

    # step 1: capture face
    def capture_entry(self,capture_method: str = None) -> np.ndarray:
        try:
            capture = cap.Capture(capture_method)
        except Exception as e:
            print("Error: ", e)
            print("Could not capture image. Please try again.")
        return capture
        

    # step 2: process image. Gets the face location , encoding, and comparison 
    def process_image(self,capture: str = None):
        try:
            # get the face location and encoding
            new_face = rec.FacialRecognition(capture)
            # compare the face to known faces
            new_comparison_data = new_face.compare_faces
            return new_comparison_data
        except Exception as e:
            print("Error: ", e)
            print("Could not process image. Please try again.")
        return None

    # runs a comparison from known faces to the captured face and returns
    def match_processed_image(self, capture: np.ndarray) -> bool:
        # step 2: compare face to known faces returns {student_id , }
        new_comparison_data = comp.FacialComparison().compare_faces(capture)
        # step 3: return result
        print("Match found: ", new_comparison_data.student_id)
        
        return new_comparison_data.result

    


def main():
    os.add_dll_directory(os.environ['CUDA_PATH'])
    dlib.DLIB_USE_CUDA = True
    if dlib.DLIB_USE_CUDA:
        print("Using CUDA for dlib.")
    else:
        print("CUDA is not available for dlib.")
    



if __name__ == "__main__":
    main()
