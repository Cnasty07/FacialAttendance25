import os
import dlib
import numpy as np
import pandas

import src.components.capture as cap
import src.components.comparison as comp
import src.components.recognition as rec

from typing import Optional , List


# FacialController Flow:
    # Load known faces from database
    # Capture new face (from camera or file)
    # Process new face
    # Match face
    

class FacialController:
    """_summary_
    This class is used to control the facial recognition system

    Args: 
        class_id (int): The class id to be used for the facial recognition system.

    Attributes:
        class_id (int): The class id to be used for the facial recognition system.
        known_faces (dict): The known faces of the class.
    """

    def __init__(self, class_id: Optional[int] = None) -> None:
        self.class_id = class_id
        # self.known_faces = self.load_known_faces()
        # pass

    # TODO : Check with real camera capture later and not test user.
    @staticmethod
    def load_known_faces(student) -> List[np.ndarray]:
        """_summary_
            Loads the known faces from the database.
        Returns:
            List[np.ndarray]: returns a list of known faces as numpy arrays.
        """

        known_faces = []

        # Inserting test known faces for Elon Musk Test User
        if student['name'] == "Elon Musk" and student["face_data"] == []:
            import sys
            sys.path.append(os.path.relpath("../../"))
            print("Current Directory: ", os.getcwd())
            print("Loaded Known Faces for Elon Musk: ", rec.FacialRecognition.get_face_encoding("database/tests/Musk3.jpg"), type(known_faces))
            known_faces.append(
                rec.FacialRecognition.get_face_encoding("./database/tests/Musk3.jpg"))
        else:# FIXME: Come back later to make sure it works
            for face in student['face_data']:
                known_faces.append(np.array(face))
        print ("Known Faces Loaded: ", known_faces)

        # Loading known faces from student face_data
        for face in student['face_data']:
            known_faces.append(np.array(face))
        return known_faces

    # -- not using this method yet --
        # starts the process of checking in a student
        # Steps For Entry
            # step 1: capture face
            # step 2: process image
            # step 3: match face
    def start_new_entry(self, capture_method: Optional[str] = None):
        """_summary_
            Starts a new entry for a student.
        Args:
            capture_method (Optional[str], optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        try:
            capture = self.capture_entry(capture_method)
            comparison_data = self.process_image(capture)
            match = self.match_processed_image(comparison_data)
            
        except Exception as e:
            print("Error: ", e)
            print("Could not start new entry. Please try again.")

        return "Check in complete."

    # Step 1
    @staticmethod
    def capture_entry(capture_method: Optional[str] = None) -> np.ndarray:
        """_summary_
            Captures the image from the camera or file.
        Args:
            capture_method (Optional[str], optional): _description_. Defaults to None.

        Returns:
            np.ndarray: _description_
        """
        try:
            capture = cap.Capture(capture_method)
        except Exception as e:
            print("Error: ", e)
            print("Could not capture image. Please try again.")
        load_face = rec.face_recognition.load_image_file(capture)
        return load_face

    # Step 2: process image. Gets the face location , encoding, and comparison using recognition module
    @staticmethod
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
        new_comparison_data = comp.FacialComparison.compare_faces(
            known_faces, capture)

        return new_comparison_data


def main():
    from utils.gpu_detection import is_gpu_available
    is_gpu_available()

    facialController = FacialController()
    known_faces = facialController.load_known_faces()
    print("Known faces loaded.")
    print(known_faces)


if __name__ == "__main__":
    main()
