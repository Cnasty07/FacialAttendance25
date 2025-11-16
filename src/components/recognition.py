import os
import cv2 as cv
import face_recognition
import dlib
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

    @staticmethod
    def get_face_encoding(img_path: str) -> np.ndarray:
        try:
            img = FacialRecognition().load_image_file(img_path)
        except Exception as e:
            print(f"Error loading image: {e}")
            exit()
        img_encoding = face_recognition.face_encodings(img)[0]
        return img_encoding
    
    @staticmethod
    def show_faces(self) -> None:
        # ideally only one face when checking in.
       pil_image = Image.fromarray(self.img_path)
       d = ImageDraw.Draw(pil_image)
       d.rectangle(self.get_face_features)
       d.text((10, 10), "Is This you?", fill=(255, 255, 255))

    def get_face_features(self) -> dict:
        face_features = face_recognition.face_landmarks(self.img_path)
        return face_features

# -- END Facial Recognition Class --


# Testing Purposes
def main() -> None:
    new_face = FacialRecognition()
    new_face.img_path = "path_to_image"

if __name__ == '__main__':
    main() 
