import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import Label, Button
import cv2
from PIL import Image, ImageTk
import threading
from datetime import datetime
# adding database and facial system to 
from controllers.databaseController import ClassTable
from controllers.facial_controller import FacialController


class FacialAttendanceSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facial Attendance System")
        self.root.geometry("800x600")
        self.root.configure(background="grey")

        # Title
        self.title_label = Label(root, text="Facial Attendance System", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)
        
        try:
            # Class List
            classes_list = ClassTable("./database/school.db").read()
            print(classes_list)
        except Exception as e:
            print(f"An error occurred: {e}")
        
        def on_select(event):
            selected_item = self.class_list.get()
        # Extract class names for the combobox
        class_names = [cls for cls in classes_list['name']]
        # Class List Dropdown
        self.class_list = ttk.Combobox(root)
        self.class_list['values'] = class_names
        self.class_list.set("Select Class")
        self.class_list.bind("<<ComboboxSelected>>",on_select)
        self.class_list.pack(pady=10)

        # Camera Feed Frame
        self.camera_frame = Label(root, width=200, height=400)
        self.camera_frame.pack(pady=10, expand=False, fill="both")
        
        # Input field
        self.input_label = Label(root, text="Enter Student Name:", font=("Helvetica", 14))
        self.input_label.pack(pady=5)
        self.input_entry = tk.Entry(root, font=("Helvetica", 14))
        self.input_entry.pack(pady=5)

        # Record Attendance Button
        self.record_button = Button(
            root,
            text="Record Attendance",
            font=("Helvetica", 14),
            command=self.record_attendance
        )
        self.record_button.pack(pady=10)

        # Initialize camera and thread
        self.cap = cv2.VideoCapture(0)  # Open the default camera
        self.running = True
        self.update_camera()

    def update_camera(self):
        """Update the camera feed in the GUI."""
        if not self.running:
            return

        

        ret, frame = self.cap.read()
        if ret:
            # Convert BGR (OpenCV) to RGB (Pillow)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame_image = ImageTk.PhotoImage(Image.fromarray(frame))

            # Update the frame
            self.camera_frame.configure(image=frame_image)
            self.camera_frame.image = frame_image
        
        # Get the current date and time
        now = datetime.now()
        # Format the date and time to include in the file path
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        # Save the captured image to the specified path with the timestamp
        file_path = f'./database/captures/captured_image_{timestamp}.jpg'
        # Save the captured image to the specified path
        cv2.imwrite(file_path, frame)
        unknown_face = FacialController.process_image(file_path)
        
        # Schedule the next update
        self.root.after(10, self.update_camera)
    
    def confirm_attendance(self, student_name, class_name,unknown_face):
        
        if FacialController.match_processed_image(unknown_face):
            """Method for attendance confirmation window."""
            self.confirm_window = tk.Toplevel(self.root)
            self.confirm_window.title("Attendance Confirmation")
            self.confirm_window.geometry("400x200")

            # Generate current date and time
            current_time = datetime.datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

            # Create confirmation message
            message = (f"Successfully recorded student {student_name} "
                    f"on {formatted_time} for class {class_name}.")

            self.confirmation_label = Label(
                self.confirm_window,
                text=message,
                font=("Helvetica", 12),
                wraplength=350,
                justify="center"
            )
            self.confirmation_label.pack(pady=20)
            

            # Close Button for the confirmation window
            close_button = Button(self.confirm_window, text="Close", command=self.confirm_window.destroy)
            close_button.pack(pady=10)
        else:
            print("No match found. Attendance not confirmed.")
            

    def record_attendance(self):
        """Method to simulate attendance recording and open the confirmation window."""
        # Simulate getting student name and class name (replace this with real data)
        student_name = "John Doe"
        class_name = "CSCI 3366"

        if self.input_entry.get() != "":
            student_name = self.input_entry.get()

        # Open the confirmation window
        threading.Thread(target=self.confirm_attendance, args=(student_name, class_name)).start()


    def close(self):
        """Clean up resources when the application is closed."""
        self.running = False
        self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FacialAttendanceSystemApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()