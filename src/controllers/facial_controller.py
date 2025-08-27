import os
import dlib
import numpy as np
import pandas

import src.components.capture as cap
import src.components.comparison as comp
import src.components.recognition as rec
import src.controllers.databaseController as db

from typing import Optional


class FacialController:
    """_summary_
    This class is used to control the facial recognition system
    
    Args: 
        class_id (int): The class id to be used for the facial recognition system.
    
    Attributes:
        class_id (int): The class id to be used for the facial recognition system.
        known_faces (dict): The known faces of the class.
    """
    def __init__(self, class_id: Optional[int] = None):
    #     self.class_id = class_id
        # self.known_faces = self.load_known_faces()
        pass

    @staticmethod
    def load_known_faces() -> pandas.Series:
        student_table = db.StudentTable().read()
        known_faces = student_table.set_index('id')['face_encodings']
        for index, face_encoding in known_faces.items():
            known_faces.at[index] = np.array(face_encoding)
        print(known_faces[known_faces.index == 11])
        print("zero value: ", type(known_faces.values[0]))
        
        return known_faces

    # -- not using this method yet -- 
    # starts the process of checking in a student 
    def start_new_entry(self, capture_method: Optional[str] = None):
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

    @staticmethod
    # step 1: capture face
    def capture_entry(capture_method: Optional[str] = None) -> np.ndarray:
        try:
            capture = cap.Capture(capture_method)
        except Exception as e:
            print("Error: ", e)
            print("Could not capture image. Please try again.")
        load_face = rec.face_recognition.load_image_file(capture)
        return load_face
        
    @staticmethod
    # step 2: process image. Gets the face location , encoding, and comparison using recognition module
    def process_image(capture: Optional[str] = None) -> np.ndarray:
        """_summary_
            process the image to get the face encoding.
        Args:
            capture (str, optional): _description_. Defaults to None.

        Returns:
            _type_:  np.ndarray: returns processed image in numpy array
        """
        try:
            # get the face location and encoding
            new_face_encoding = rec.FacialRecognition().get_face_encoding(capture)
            # print("new face encoding: ",new_face_encoding)
            return new_face_encoding
        except Exception as e:
            print("Error: ", e)
            print("Could not process image. Please try again.")
        return None

    # runs a comparison from known faces to the captured face and returns
    @staticmethod
    def match_processed_image(capture: np.ndarray, known_faces: np.ndarray) -> bool:
        
        # compare the faces but params are backwards from input to output 
        new_comparison_data = comp.FacialComparison.compare_faces(known_faces,capture)
        
        return new_comparison_data



def main():
    os.add_dll_directory(os.environ['CUDA_PATH'])
    dlib.DLIB_USE_CUDA = True
    if dlib.DLIB_USE_CUDA:
        print("Using CUDA for dlib.")
    else:
        print("CUDA is not available for dlib.")


if __name__ == "__main__":
    main()
