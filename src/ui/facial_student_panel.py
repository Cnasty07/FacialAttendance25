# Facial Student Panel UI using Tkinter
import math
import threading
import datetime
from datetime import datetime

import tkinter as tk
from tkinter import ttk
from tkinter import Label, Button, messagebox

import pandas as pd
import cv2
from PIL import Image, ImageTk


# Local Imports
from src.controllers.databaseController import ClassTable, AttendanceTable, StudentTable , FaceTable
from src.controllers.facial_controller import FacialController


# TODO 1: Refactor this into a proper Tkinter Frame for better integration with AppController
# TODO 2: Change database calls to MongoDB later on.
# from src.controllers.remoteDatabaseController import StudentDatabaseController

# --- Facial Attendance Student View (Tkinter Frame) ---
class FacialStudentPanel(tk.Frame):
    """A Tkinter Frame that shows camera feed and attendance controls.

    This class is a drop-in Frame you can pack/grid into a parent window
    or another container. It preserves the original UI layout while
    using `self` as the frame instead of manipulating the parent window.
    """

    def __init__(self, parent, controller = None) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        self.db_path = "./database/school.db"
        self.file_path = ""
        
        # TODO 2: Database connection setup
        ## New database connection for remote MongoDB
        # self.remote_db_controller = StudentDatabaseController()
        # self.db = self.remote_db_controller.get_database()

        # Title label (inside this frame)
        self.title_label = Label(self, text="Facial Attendance System", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)

        # Initialize facial controller (may be stateful)
        try:
            self.fc = FacialController()
        except Exception:
            # Fallback to static usage if FacialController only exposes staticmethods
            self.fc = FacialController

        # Load classes for combobox
        try:
            classes_list = ClassTable(self.db_path).read()
        except Exception as e:
            print(f"An error occurred loading classes: {e}")
            classes_list = []

        def on_select(event):
            _ = self.class_list.get()

        # Extract class names
        class_names = [cls for cls in classes_list['name']] if hasattr(classes_list, 'get') else []

        # Class selection combobox
        self.class_list = ttk.Combobox(self)
        self.class_list['values'] = class_names
        self.class_list.set("Select Class")
        self.class_list.bind("<<ComboboxSelected>>", on_select)
        self.class_list.pack(pady=10)

        # Camera feed frame (Label used to hold image)
        self.camera_frame = Label(self, width=200, height=400)
        self.camera_frame.pack(pady=10, expand=False, fill="both")

        # Input field for student name
        self.input_label = Label(self, text="Enter Student Name:", font=("Helvetica", 14))
        self.input_label.pack(pady=5)
        self.input_entry = tk.Entry(self, font=("Helvetica", 14))
        self.input_entry.pack(pady=5)

        # Record attendance button
        self.record_button = Button(self, text="Record Attendance", font=("Helvetica", 14), command=self.record_attendance)
        self.record_button.pack(pady=10)

        # Search section
        self.search_label = Label(self, text="Search Attendance Records:", font=("Helvetica", 14))
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(self, font=("Helvetica", 14))
        self.search_entry.pack(pady=5)

        # Search buttons
        self.search_student_button = Button(self, text="Search Student", font=("Helvetica", 14), command=self.search_student)
        self.search_student_button.pack(pady=5)

        self.search_date_button = Button(self, text="Search Date", font=("Helvetica", 14), command=self.search_date)
        self.search_date_button.pack(pady=5)

        # Camera
        self.cap = cv2.VideoCapture(0)
        self.running = True
        # Start camera updates
        self.after(10, self.update_camera)

    ## -- Search by Student Name --
    def search_student(self) -> None:
        """Query attendance records by student name."""
        student_name = self.search_entry.get()
        if not student_name:
            messagebox.showerror("Error", "Please enter a student name to search.")
            return

        try:
            attendance_table = AttendanceTable("./database/school.db")
            query = f"""
                SELECT * FROM attendance
                WHERE student_id IN (
                    SELECT id FROM student WHERE name LIKE ?
                )
            """
            records = pd.read_sql_query(query, attendance_table.conn, params=(f"%{student_name}%",))
            self.display_results(records)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # -- Search by Date --
    def search_date(self) -> None:
        """Query attendance records by date."""
        date = self.search_entry.get()
        if not date:
            messagebox.showerror("Error", "Please enter a date to search.")
            return

        try:
            attendance_table = AttendanceTable("./database/school.db")
            query = "SELECT * FROM attendance WHERE date LIKE ?"
            records = pd.read_sql_query(query, attendance_table.conn, params=(f"%{date}%",))
            self.display_results(records)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    # -- Display Results in Popup --
    def display_results(self, records) -> None:
        """Display the queried records in a popup window."""
        if records.empty:
            messagebox.showinfo("No Results", "No records found for the given query.")
            return

        result_window = tk.Toplevel(self.parent)
        result_window.title("Search Results")
        result_window.geometry("600x400")

        tree = ttk.Treeview(result_window)
        tree["columns"] = list(records.columns)
        tree["show"] = "headings"

        for col in records.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")

        for _, row in records.iterrows():
            tree.insert("", "end", values=list(row))

        tree.pack(fill="both", expand=True)
        close_button = Button(result_window, text="Close", command=result_window.destroy)
        close_button.pack(pady=10)
        

        # Initialize camera and thread
        self.cap = cv2.VideoCapture(0)  # Open the default camera
        self.running = True
        self.update_camera()

    # -- Update Camera Feed --
    def update_camera(self) -> None:
        """Update the camera feed in the GUI with optional face detection."""
        if not self.running:
            return

        ret, frame = self.cap.read()
        if ret:
            # Convert BGR (OpenCV) to RGB (Pillow)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frame_image = ImageTk.PhotoImage(Image.fromarray(frame))
            self.camera_frame.configure(image=frame_image)
            self.camera_frame.image = frame_image

        # Schedule the next update
        self.parent.after(10, self.update_camera)

    # -- Confirm Attendance --
    def confirm_attendance(self, student_name, class_name, face_path) -> None:
        """Match face and confirm attendance."""
        
        try:
            # Process and match face loads image and gets encoding
            unknown_face = FacialController.process_image(face_path)
            # retrieves the known faces from the database, with id as index
            try:
                load_known_faces = FacialController.load_known_faces()
                # collects only the face encodings
                known_encodings = [face_encoding for face_encoding in load_known_faces]
                # Compare the unknown face to the known faces
                is_match = self.fc.match_processed_image(unknown_face, known_encodings)
    
                student_id = load_known_faces.index[is_match.index(True)]
                
            except ValueError:
                print("No match found.")
                student_id = None
            
            
            # Compare the unknown face to the known faces
            # is_match = FacialController.match_processed_image(unknown_face, known_encodings)

            # Generate current date and time
            current_time = datetime.now()
            formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")

            if is_match:
                student_table_class = StudentTable("./database/school.db")
                Student_table = student_table_class.read()
                try:
                    student_record = Student_table.loc[Student_table['id'] == student_id]
                except Exception as e:
                    print(f"Student not found:  {e}")
                    student_id = math.randomInt(20,100)
                    
                    
                if student_record:
                    student_id = student_record['id']
                    print(student_id)
                    AttendanceTable("./database/school.db").create(student_id, class_name, formatted_time)
                    message = (f"Successfully recorded student {student_name} " f"on {formatted_time} for class {class_name}.")
                else:
                    
                    new_student = student_table_class.create(student_id, student_name, [class_name], unknown_face)
                    
                    message = (f"New student {student_name} added and attendance recorded "
                               f"on {formatted_time} for class {class_name}.")
                
            else:
                message = "No match found. Attendance not recorded."
        except Exception as e:
            print("Error: ", e)
            message = "An error occurred. Please try again."

        ## Show confirmation message in a new window
        self.confirm_window = tk.Toplevel(self.parent)
        self.confirm_window.title("Attendance Confirmation")
        self.confirm_window.geometry("400x200")
        self.confirmation_label = Label(
            self.confirm_window, text=message, font=("Helvetica", 12), wraplength=350, justify="center"
        )
        self.confirmation_label.pack(pady=20)
        close_button = Button(self.confirm_window, text="Close", command=self.confirm_window.destroy)
        close_button.pack(pady=10)

    # -- Record Attendance -- 
    def record_attendance(self) -> None:
        """Capture image, detect face, and initiate attendance recording."""
        ret, frame = self.cap.read()
        if not ret:
            print("Failed to capture frame from camera.")
            return

        # Face detection
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

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
        student_name = self.input_entry.get() or "Unknown Student"
        class_name = self.class_list.get() or "Unknown Class"
        threading.Thread(target=self.confirm_attendance, args=(student_name, class_name, face_path)).start()


    def close(self) -> None:
        """Clean up resources when the application is closed."""
        self.running = False
        self.cap.release()
        self.parent.destroy()


if __name__ == "__main__":
    parent = tk.Tk()
    app = FacialStudentPanel(parent)
    parent.protocol("WM_DELETE_WINDOW", app.close)
    parent.mainloop()