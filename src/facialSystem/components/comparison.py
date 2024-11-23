import os
import face_recognition
import dlib
import numpy as np

#main code 
class FacialComparison:
    def __init__(self):
        # TODO: make query for comparison between faces
        try:
            # {student_id: img_encoding_array}
            self.known_faces = {}
        except Exception as e:
            print(f"Error: {e}\n Defaulting to empty list.")
            self.known_faces = {}
    
    def compare_faces(self,new_img: np.ndarray = None) -> dict:
        """_summary_
        Checks database for a match of the new image. If found returns the student_id and the result of the comparison.
        If not found returns None.

        Args:
            new_img (np.ndarray, optional): _description_. Defaults to None.

        Returns:
            dict: _description_
        """
        # image comparison to see if the image is the same person in database
        for student_id,student_img_encoding in self.known_faces.keys():    
            result = face_recognition.compare_faces([student_img_encoding], new_img)
            if result:
                found_student = {"student_id": student_id, "result": result}
                self.comparison_accuracy(student_img_encoding,new_img)
                return found_student
                
        return None
    
    def comparison_accuracy(self,student_facial_imgs = None,new_img: np.ndarray = None):
        # accuracy of prediction
        face_distance = face_recognition.face_distance([student_facial_imgs], new_img)
        return face_distance
    
    
def main():
    pass

if __name__ == '__main__':
    main() 
