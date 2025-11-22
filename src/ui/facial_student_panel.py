# Facial Student Panel UI using Tkinter
import threading
import datetime
from datetime import datetime

# UI packages
import tkinter as tk
from tkinter import ttk
from tkinter import Label, Button, messagebox

# import pandas as pd
import cv2
from PIL import Image, ImageTk

# Local Imports
# from src.controllers.databaseController import AttendanceTable, StudentTable
from src.controllers.facialController import FacialController
from src.models.User import StudentUserSchema

# from src.controllers import mongooseClient
# TODO: Refactor and Change DB to mongo
# 1: Refactor this into a proper Tkinter Frame for better integration with AppController
# 2: Change database calls to MongoDB later on. (classes already done here)
# 1. Load face_data from MongoDB instead of local SQLite
# 2. Load attendance data from MongoDB instead of local SQLite

# --- Facial Attendance Student View (Tkinter Frame) ---


class FacialStudentPanel(tk.Frame):
    """Tkinter Frame for Facial Attendance Student Panel UI.
    """

    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        # New database connection for remote MongoDB
        # self.db = self.controller.remote
        
        # Configure grid sizing/constraints so camera expands
        # Title is row 0, combobox row 1, controls row 2, camera row 3
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0, pad=10)
        self.grid_rowconfigure(2, weight=0, pad=10)
        self.grid_rowconfigure(3, weight=1, minsize=200)
        
        # Make left and center columns expand; right-side buttons stay their natural size
        self.grid_columnconfigure(0, weight=1, uniform="maincols")
        self.grid_columnconfigure(1, weight=1, uniform="maincols")
        self.grid_columnconfigure(2, weight=0, uniform="maincols")
        self.grid_columnconfigure(3, weight=0)
        
        # Ensure widgets that should fill their cells use sticky
        # Example: let camera fill whole row and expand
        # self.camera_frame.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        
        # # Make labels/buttons stretch horizontally if desired (use sticky="ew")
        # self.class_list.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5)
        # self.input_label.grid(row=2, column=0, sticky="e", padx=5)
        # self.name_label.grid(row=2, column=1, sticky="w", padx=5)
        # self.record_button.grid(row=2, column=2, sticky="ew", padx=5)
        # self.update_face_button.grid(row=2, column=3, sticky="ew", padx=5)
        
        # Title label (inside this frame)
        self.title_label = ttk.Label(
            self, text="Facial Attendance System", font=("Helvetica", 20, "bold"))
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        # self.sep = ttk.Separator(self, orient='horizontal')
        # self.sep.grid(row=1, column=0, columnspan=2, sticky="ew", pady=5)

        # self.configure(bg="lightblue")
        
        # Initialize facial controller (may be stateful)
        try:
            self.fc = FacialController()
        except Exception:
            # Fallback to static usage if FacialController only exposes staticmethods
            self.fc = FacialController

        # Selected class data
        def on_select(event):
            _ = self.class_list.get()
            print(f"Selected class: {_}")
            # searching for data for class
            for classes in self.controller.all_classes:
                if classes['name'] == _:
                    print(f"Found class data: {classes}")
                    break

        try:
            classes_list = []
            for classes in self.controller.all_classes:
                classes_list.append(classes)
        except Exception as e:
            print(f"An error occurred loading classes: {e}")
            classes_list = []

        # Extract class names shows as "course_code : name"
        class_names = [
            f"{cls['course_code']} : {cls['name']}" for cls in classes_list]
        # Class selection combobox
        self.class_list = ttk.Combobox(self)
        self.class_list['values'] = class_names
        self.class_list.set("Select Class")
        self.class_list.bind("<<ComboboxSelected>>", on_select)
        self.class_list.grid(row=1, column=0,ipadx=5, sticky="w")

        # # Camera feed frame (Label used to hold image)
        # self.camera_frame = Label(self, width=self.parent.winfo_width()//2, height=(self.parent.winfo_height()//4))
        # self.camera_frame.pack(pady=10, expand=False, fill="both")


        # Input field for student name
        self.input_label = ttk.Label(
            self, text="Current Student Name:", font=("Helvetica", 14))
        self.input_label.grid(row=2, column=0, ipadx=5, sticky="w")

        self.name_label = ttk.Label(
            self, text="student name", font=("Helvetica", 14))
        self.name_label.grid(row=2, column=0, ipadx=5, sticky="e")
        
        # Record attendance button
        self.record_button = ttk.Button(self, text="Record Attendance", command=self.record_attendance)
        self.record_button.grid(row=1, column=1, ipadx=5, sticky="e")
        # Update Student Face Data Button
        self.update_face_button = ttk.Button(self, text="Update Face Data", command=self.update_face_data)
        self.update_face_button.grid(row=1, column=2, ipadx=5, sticky="w")
        
        
        # Camera feed frame (Label used to hold image)
        self.camera_frame = ttk.Label(self)
        self.camera_frame.grid(row=3, column=0,columnspan=3, ipadx=5, sticky="ew")
        # self.camera_frame.pack()
        # Camera
        self.cap = cv2.VideoCapture(0)

        # Handles no camera found error
        if self.cap is None or not self.cap.isOpened():
            self.camera_frame.grid_forget()
            error_label = ttk.Label(
                self, text="Error: Could not access the camera.", foreground="red", font=("Helvetica", 14))
            error_label.grid(row=3, column=0, columnspan=3, ipadx=5)
            self.running = False
        else:
            self.running = True
            # Start camera updates
            self.after(10, self.update_camera)

    def on_show(self) -> None:
        """_summary_
            Hook called when this frame is shown.
        """
        try:
            self.student = self.controller.load_student()
            print("FacialStudentPanel on_show loaded student: ", self.student)
            self.name_label.config(text=f"{self.student['name']}")
        except Exception as e:
            print("Error in on_show:", e)

        if self.student['name'] == "Elon Musk":
            self.confirm_button = tk.Button(self, text="Confirm Attendance", font=(
                "Helvetica", 14), command=self.test_confirm_attendance)
            self.confirm_button.grid(row=4, column=2,pady=10)

    # -- Test Confirm Attendance --
    def test_confirm_attendance(self):
        self.confirm_attendance(
            student_name=self.student['name'], class_name=self.class_list.get(), face_path="./database/tests/MuskComp.jpg")
        print("Test confirm attendance executed.")

    # -- Update Face Data --
    def update_face_data(self) -> None:
        """Update the face data for the student in the database."""
        student_name = self.student['name']
        print(student_name)
        if not student_name:
            messagebox.showerror(
                "Error", "Please enter a student name to update face data.")
            return

        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame from camera.")
            return

        # Face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            print("No face detected. Please try again.")
            return

        # Process the first detected face
        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]
            break  # Only process the first face

        # Save the face ROI
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        face_path = f'./database/tests/updated_face_{timestamp}.jpg'
        cv2.imwrite(face_path, face_roi)
        print(f"Face captured and saved to {face_path}")

        # Here you would add code to update the student's face data in the database
        messagebox.showinfo(
            "Success", f"Face data for {student_name} has been updated.")

    # -- Update Camera Feed --
    def update_camera(self) -> None:
        """Update the camera feed in the GUI with optional face detection."""
        if not self.running or self.cap is None:
            return

        ret, frame = self.cap.read()
        if ret:
            # Convert BGR (OpenCV) to RGB (Pillow)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (800, 500))
            frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
            self.camera_frame.configure(image=frame_image)
            self.camera_frame.image = frame_image

        # Schedule the next update
        self.parent.after(10, self.update_camera)

    # -- Confirm Attendance --
    def confirm_attendance(self, student_name, class_name, face_path) -> None:
        """_summary_
            Confirm attendance after processing and matching face.
            Args:
                student_name (str): _description_
                class_name (str): _description_
                face_path (list): path to face image to be processed
                Returns:
                None
        """
        message = ""
        is_match: bool = False
        # Process and Match Face
        try:
            unknown_face = self.fc.process_image(face_path)
            print("Unknown Face Encoding: ", unknown_face, type(unknown_face))
            # Loads known faces from the student face_data
            try:
                load_known_faces = self.fc.load_known_faces(
                    student=self.student)
                if self.student['email'] == "em@tamusa.edu" and self.student["face_data"] == []:
                    for face in load_known_faces:
                        print("Adding initial face data for test user.")
                        self.student['face_data'].append(face.tolist())
                # filters out only the encodings
                known_encodings = [face_encoding for face_encoding in load_known_faces]
                # Compare the unknown face to the known faces
                is_match = self.fc.match_processed_image(unknown_face, known_encodings)

                student_id = self.student['_id']
            except ValueError:
                print("No match found.")
                student_id = None

            # Generate current date and time
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

            # If match found, record attendance in MongoDB
            if is_match:
                try:
                    self.student['face_data'].append(unknown_face.tolist())
                    # self.controller.set_student(self.student)
                    
                    confirm_student = self.save_confirmation_remote()
                    print("Attendance Confirmed: ", confirm_student)

                    print("Face data updated for student:",
                          self.student['name'], type(self.student['face_data']))
                
                except Exception as e:
                    print(f"Student not found:  {e}")

                # Printing message for confirmation on student attendance
                if self.controller.remote.Student.find_one(student_id):
                    print("Attendance recorded for existing student.")
                    message = (f"{student_name} successfully recorded for attendance " +
                               f"on {formatted_time} for class {class_name}.")
                # if self.controller.remote.Student.find_one({"email": self.student['email']}):
                #     print("Attendance recorded for existing student.")
                #     message = (f"{student_name} successfully recorded for attendance " +
                #                f"on {formatted_time} for class {class_name}.")
                else:
                    # Delete when done. Will not be used once DB is set up properly.
                    new_student = self.student
                    print("New student created:", new_student)
                    message = (f"New student {student_name} added and attendance recorded " +
                               f"on {formatted_time} for class {class_name}.")
            else:
                message = "No match found. Attendance not recorded."
        except Exception as e:
            print("Error: ", e)
            message = "An error occurred. Please try again."

        # Show confirmation message in a new window
        self.confirm_window = tk.Toplevel(self.parent)
        self.confirm_window.title("Attendance Confirmation")
        self.confirm_window.geometry("400x200")
        self.confirmation_label = Label(
            self.confirm_window, text=message, font=("Helvetica", 12), wraplength=350, justify="center"
        )
        self.confirmation_label.pack(pady=20)
        close_button = Button(self.confirm_window, text="Close",
                            command=self.confirm_window.destroy)
        close_button.pack(pady=10)

        
    # -- Confirm Attendance Update --
    def save_confirmation_remote(self):
        """Confirm attendance for a student (example function)."""
        print("Confirming attendance for student:", self.student['name'])

        print("Student saved with ID:", self.student['_id'])
        try:
            print(len(self.student["face_data"]))
            self.controller.remote.Student.update_one(
                {"_id": self.student['_id']}, {"$set": {"face_data": self.student["face_data"]}})
            print("Attendance Confirmation Name:", self.student["name"])
            return True
        except Exception as e:
            print("Error confirming attendance:", e)
            return False


    # -- Record Attendance --
    def record_attendance(self) -> None:
        """Capture image, detect face, and initiate attendance recording."""
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame from camera.")
            return

        # Face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(
            gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            print("No face detected. Please try again.")
            return

        # Process the first detected face
        for (x, y, w, h) in faces:
            face_roi = frame[y:y + h, x:x + w]
            break  # Only process the first face

        # Save the face ROI
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        face_path = f'./database/tests/face_{timestamp}.jpg'
        cv2.imwrite(face_path, face_roi)
        print(f"Face captured and saved to {face_path}")

        # Get student name and class name from input fields
        try:
            print("Recording attendance for student:", self.student['name'])
        except Exception as e:
            print("Error getting student name:", e)
        student_name = self.student['name'] or "Unknown Student"
        class_name = self.class_list.get() or "Unknown Class"
        threading.Thread(target=self.confirm_attendance, args=(
            student_name, class_name, face_path)).start()

    # -- Close Panel --
    def close(self) -> None:
        """Clean up resources when the application is closed."""
        self.running = False
        self.cap.release()
        self.parent.destroy()

# -- END Facial Attendance Student View (Tkinter Frame) --


# -- Standalone Test Runner --
def main() -> None:
    """Run the Facial Student Panel as a standalone application for testing."""
    # parent = tk.Tk()
    # app = FacialStudentPanel(parent)
    # parent.protocol("WM_DELETE_WINDOW", app.close)
    # parent.mainloop()


if __name__ == "__main__":
    main()
