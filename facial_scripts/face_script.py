import cv2
import face_recognition
import dlib
import numpy as np
from PIL import Image, ImageDraw
import os
os.add_dll_directory(os.environ['CUDA_PATH'])
dlib.DLIB_USE_CUDA = True
print(dlib.cuda)
#main code 


# not using, but can be used for future reference
def openCV_pkg():
    img = cv2.imread("girlTest.jpg")
    if img is None:
        print("Image not found")
        exit()
    # convert image to grayscale
    rbg_image = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # eng encoding 
    img_encoding = face_recognition.face_encodings(rbg_image)[0]
def show_faces(image_path):
    cv2.imshow('image', image_path)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# gets the directory of the pictures
def get_pictures_directory():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pictures_dir = os.path.join(current_dir, 'data', 'tests')
    if not os.path.exists(pictures_dir):
        print("Directory not found")
        exit()
    return pictures_dir


# using this function to get the face landmarks and face locations
def face_rec_pkg():
    image_face_rec = face_recognition.load_image_file("groupPic.jpg")
    face_locations = face_recognition.face_locations(image_face_rec,0,"cnn")
    face_landmarks = face_recognition.face_landmarks(image_face_rec,face_locations,"large")[0]
    
    pil_image = Image.fromarray(image_face_rec)
    d = ImageDraw.Draw(pil_image)
    print(face_locations)
    for face_location in face_locations:
        top, right, bottom, left = face_location
        d.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0))
        d.text((left, top), 'elon musk', fill=(255, 255, 255, 255))
    for face_feature in face_landmarks.keys():
        print(face_feature)
        d.line(face_landmarks[face_feature], width=5)
    #
    
    
    # drawing on the image
    # d.polygon(face_landmarks['left_eyebrow'], fill=(68, 54, 39, 128))
    # d.polygon(face_landmarks['right_eyebrow'], fill=(68, 54, 39, 128))
    # d.text((face_landmarks['nose_bridge'][1][0], face_landmarks['nose_bridge'][1][1]), 'random girl', fill=(255, 255, 255, 255))
    
    # d.rectangle(((face_landmarks['chin'][0][0], face_landmarks['chin'][17][1]), (face_landmarks['chin'][16][0], face_landmarks['chin'][8][1])), outline=(255, 0, 0))
    
    # show the image
    pil_image.show()
    return face_landmarks




def compare_faces(img_encoding, img_encoding2):
    # image comparison to see if the image is the same person in database
    result = face_recognition.compare_faces([img_encoding], img_encoding2)
    return result

def main():
    new_face = face_rec_pkg()
    print(new_face)
    
    # musk encoding
    # musk_encoding = face_recognition.face_encodings(face_recognition.load_image_file("Musk.webp"))[0]
    # musk_encoding2 = face_recognition.face_encodings(face_recognition.load_image_file("Musk3.jpg"))[0]
    # musk_encoding3 = face_recognition.face_encodings(face_recognition.load_image_file("MuskComp.jpg"))[0]
    
    # # face comparison
    # new_comparison = compare_faces([musk_encoding,musk_encoding3], musk_encoding2)
    # print(new_comparison)
    
    # # accuracy of prediction
    # face_distance = face_recognition.face_distance([face_recognition.face_encodings(face_recognition.load_image_file("Musk.webp"))[0]], face_recognition.face_encodings(face_recognition.load_image_file("MuskComp.jpg"))[0])
    # print(face_distance)
if __name__ == '__main__':
    main() 
