import os
import numpy as np

import face_recognition

# -- Facial Comparison Class --
# INFO: This class is used to compare faces to known faces in the database.
class FacialComparison:

    @staticmethod
    def compare_faces(known_faces_encodings: np.ndarray, new_img_encodings: np.ndarray | None = None) -> list[bool]:
        """_summary_
        Checks database for a match of the new image. If found returns the student_id and the result of the comparison.
        If not found returns None.
        Args:
            new_img (np.ndarray, optional): _description_. Defaults to None.
        Returns:
            dict: array of bools to see who it is in the database
        """
        # image comparison to see if the image is the same person in database
        # params : known_faces_encodings, new_img_encodings in that order
        comparison = face_recognition.compare_faces(
            known_faces_encodings, new_img_encodings)

        return comparison

    @staticmethod
    def comparison_accuracy(student_facial_imgs=None, new_img: np.ndarray | None= None) -> np.ndarray:
        """_summary_
            Calculates the accuracy of the facial recognition comparison.
        Args:
            student_facial_imgs (_type_, optional): _description_. Defaults to None.
            new_img (np.ndarray, optional): _description_. Defaults to None.

        Returns:
            np.linalg.norm: _description_
        """
        # accuracy of prediction
        face_distance = face_recognition.face_distance(
            [student_facial_imgs], new_img)
        return face_distance

# -- END Facial Comparison Class --


# Testing Purposes
def main() -> None:
    from utils.gpu_detection import is_gpu_available
    is_gpu_available()
    # new_comparison = FacialComparison()
    # new_comparison.compare_faces()


if __name__ == '__main__':
    main()
