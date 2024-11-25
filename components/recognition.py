import os
import cv2 as cv
import face_recognition
import dlib
from PIL import Image, ImageDraw

#main code 
class FacialRecognition:
    def __init__(self, img_path: str = None):
        self.img_path = img_path
        self.img_face_encoding = self.get_face_encoding()
    
    def find_face(self):
        find_face_in = face_recognition.face_locations(self.img_path)
        return find_face_in
    
    def get_face_encoding(self):
        img = face_recognition.load_image_file(self.img_path)
        if img is None:
            print("Image not found")
            exit()
        img_encoding = face_recognition.face_encodings(img)[0]
        return img_encoding
    
    def show_faces(self):
        # ideally only one face when checking in.
       pil_image = Image.fromarray(self.img_path)
       d = ImageDraw.Draw(pil_image)
       d.rectangle(self.get_face_features)
       d.text((10, 10), "Is This you?", fill=(255, 255, 255))
       
    def get_face_features(self):
        face_features = face_recognition.face_landmarks(self.img_path)
        return face_features


def main():
    new_face = FacialRecognition()
    new_face.img_path = "path_to_image"

if __name__ == '__main__':
    main() 
