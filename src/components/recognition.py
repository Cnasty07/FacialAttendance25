import os

# Staging for facial recognition component
# import cv2
import face_recognition
from PIL import Image, ImageDraw
import numpy as np

# -- Facial Recognition Class --
    # INFO: This class handles facial recognition tasks using the face_recognition library.
class FacialRecognition:
    def __init__(self, img_path: str | None = None):
        self.img_path = img_path
    #     # self.img_face_encoding = self.get_face_encoding()
    
    @staticmethod
    def find_face(self) -> list:
        """_summary_
            This function finds the face in the image
        Returns:
            _type_: list
        """
        find_face_in = face_recognition.face_locations(self.img_path)
        return find_face_in
    
    @staticmethod
    def load_image_file(img_path) -> np.ndarray:
        """_summary_
            This function loads the image file
        Returns:
            _type_: np.ndarray
        """
        img = face_recognition.load_image_file(img_path)
        return img

    # INFO: IN USE
    @staticmethod
    def get_face_encoding(img_path: str) -> np.ndarray:
        """_summary_
            This function gets the face encoding from the image
        Returns:
            _type_: np.ndarray (128-dimension face encoding)
        """

        try:
            img = FacialRecognition.load_image_file(img_path)
        except Exception as e:
            print(f"Error loading image: {e}")
            exit()
        
        img_encoding = face_recognition.face_encodings(img)[0]
        return img_encoding

    # 
    @staticmethod
    def show_faces(self) -> None:
        """_summary_
            This function shows the faces in the image
            Returns:
                _type_: None
        """
        
        # ideally only one face when checking in.
        pil_image = Image.fromarray(self.img_path)
        d = ImageDraw.Draw(pil_image)
        d.rectangle(self.get_face_features)
        d.text((10, 10), "Is This you?", fill=(255, 255, 255))

    def get_face_features(self) -> list[dict]:
        face_features = face_recognition.face_landmarks(self.img_path)
        return face_features

# -- END Facial Recognition Class --


# Testing Purposes
def main() -> None:
    new_face = FacialRecognition()
    new_face.img_path = "./database/tests/ruben1.jpg"
    face_data = new_face.get_face_encoding(new_face.img_path)
    print(face_data, type(face_data), face_data.shape)

    # Steps:
        # After getting face encoding, we need to convert it to a list for MongoDB storage.
        # 1. Create a new StudentUserModel instance with the face data.
        # 2. Test the conversion to MongoDB format.
        # 3. Insert the new student into the remote database.


    # # 1. Creating New Model Instance
    # from src.models.User import StudentUserModel
    # new_student = StudentUserModel(
    #     name="Ruben Reyes",
    #     email="rreyes@tamusa.edu",
    #     face_data=[face_data]
    # )


    # # 2. Testing DB Conversion
    # print("Student Face Data:", new_student.face_data, type(new_student.face_data))
    # print("Student Face Data Type:", type(new_student.face_data[0]))

    # # 3. Convert to MongoDB format
    # new_student_conversion = new_student.model_dump_for_mongo(keep_id=True)
    # print(new_student_conversion)

    # # Inserts into Remote DB
    # from src.controllers.remoteDatabaseController import remoteController
    # db_controller = remoteController()
    # print(db_controller.Student.insert_one(new_student_conversion))


if __name__ == '__main__':
    main()
