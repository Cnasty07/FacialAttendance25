import os
import face_recognition
import dlib

# import the other scripts to start the process
from capture import Capture
from . import comparison
from . import recognition

# TODO: Need to fix some boilerplate code

class FacialController:
    def __init__(self, known_faces_dir):
        self.known_faces_dir = known_faces_dir
        self.known_faces = self.load_known_faces()
        os.add_dll_directory(os.environ['CUDA_PATH'])
        dlib.DLIB_USE_CUDA = True

    def start_new_entry(self,capture_method: str = None):
        # step 1: capture face
        try:
            capture = Capture(capture_method)
        except Exception as e:
            print("Error: ", e)
            print("Could not capture image. Please try again.")
        # step 2: compare face to known faces returns {student_id , }
        new_comparison_data = comparison.FacialComparison().compare_faces(capture)
        # step 3: return result
        print("Match found: ", new_comparison_data.student_id)
        # step 4: if match, return name and check in
        try:
            print("Checking in: ", new_comparison_data.student_id)
            self.check_in(new_comparison_data)
            # perform the insert operation into the database
        except Exception as e:
            print("Error: ", e)
            print("Could not check in. Please try again.")
            
        return "Check in complete."

        

def main():
  pass
if __name__ == "__main__":
    main()