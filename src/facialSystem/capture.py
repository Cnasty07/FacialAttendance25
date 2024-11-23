import os
import cv2
import face_recognition
from datetime import datetime

class Capture:
    """ Summary:
    A class to capture video and images using OpenCV.
    """
    
    def __init__(self,capture_method: str):
        if capture_method == 'video':
            self.start_video_capture()
        elif capture_method == 'image':
            self.start_image_capture()
        # used for testing
        elif capture_method == 'stored':
             self.start_return_image()
        
    def start_video_capture(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open video capture.")
            return
        
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break
            
            cv2.imshow('Video Capture', frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            
             # Get the current date and time
        now = datetime.now()
        # Format the date and time to include in the file path
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        # Save the captured image to the specified path with the timestamp
        file_path = f'./data/db/captures/captured_image_{timestamp}.jpg'
        # Save the captured image to the specified path
        cv2.imwrite(file_path, frame)
        
        cap.release()
        cv2.destroyAllWindows()
        
        # not sure if this method works on videos yet
        return face_recognition.load_image_file(frame)
        
    def start_image_capture(self):
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            print("Error: Could not open video capture.")
            return
        
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            cap.release()
            return
        
        cv2.imshow('Image Capture', frame)
        
        # Get the current date and time
        now = datetime.now()
        # Format the date and time to include in the file path
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        # Save the captured image to the specified path with the timestamp
        file_path = f'./data/db/captures/captured_image_{timestamp}.jpg'
        # Save the captured image to the specified path
        cv2.imwrite(file_path, frame)
        
        
        cv2.waitKey(0)
        cap.release()
        cv2.destroyAllWindows()
        
        return face_recognition.load_image_file(file_path)

def start_return_image(self):
    return face_recognition.load_image_file('../../data/db/tests/Musk3.jpg')

def main():
    capture = Capture('video')
    # method one to capture video
    capture.start_video_capture()
    # method two to capture image
    capture.start_image_capture()

if __name__ == '__main__':
    main() 
