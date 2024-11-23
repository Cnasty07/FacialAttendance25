import os
import cv2
import face_recognition
#main code 
img = cv2.imread('/Tesla-Ceo-Elon-Musk-2014..webp')


# convert image to grayscale
rbg_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# eng encoding 
img_encoding = face_recognition.face_encodings(rbg_image)[0]


# 1 encode image

# image comparison to see if the image is the same person in database
# result = face_recognition.compare_faces([img_encoding], img_encoding)

cv2.imshow('image', img)
cv2.waitKey(0)

def main():
    pass

if __name__ == '__main__':
    main() 
