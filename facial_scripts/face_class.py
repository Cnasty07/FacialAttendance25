import os
import cv2 as cv
import face_recognition


#main code 
class FacialRecognition:
    def __init__(self):
        pass
    def get_face_encoding(self, image_path):
        img = cv.imread(image_path)
        if img is None:
            print("Image not found")
            exit()
        # convert image to grayscale
        rbg_image = cv.cvtColor(img,cv.COLOR_BGR2RGB)
        
        # eng encoding 
        img_encoding = face_recognition.face_encodings(rbg_image)[0]
        return img_encoding
    
    
def main():
    pass

if __name__ == '__main__':
    main() 
