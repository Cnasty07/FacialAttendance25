import math
import pandas as pd
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import Label, Button, messagebox
import cv2
from PIL import Image, ImageTk
import threading
from datetime import datetime

import sys


from src.controllers.databaseController import ClassTable, AttendanceTable, StudentTable , FaceTable
from src.controllers.facial_controller import FacialController


class FacialAttendanceSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Facial Attendance System")
        self.root.geometry("800x600")
        self.root.configure(background="grey")
        self.file_path = ""

        # Title
        self.title_label = Label(root, text="Facial Attendance System", font=("Helvetica", 20, "bold"))
        self.title_label.pack(pady=10)
        
        try:
            # Class List
            classes_list = ClassTable(sys.path[0] + "/database/school.db").read()
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
        
        # Search Section
        self.search_label = Label(root, text="Search Attendance Records:", font=("Helvetica", 14))
        self.search_label.pack(pady=5)
        self.search_entry = tk.Entry(root, font=("Helvetica", 14))
        self.search_entry.pack(pady=5)

        # Buttons for searching
        self.search_student_button = Button(
            root,
            text="Search Student",
            font=("Helvetica", 14),
            command=self.search_student
        )
        self.search_student_button.pack(pady=5)

        self.search_date_button = Button(
            root,
            text="Search Date",
            font=("Helvetica", 14),
            command=self.search_date
        )
        self.search_date_button.pack(pady=5)

        # Initialize camera and thread
        self.cap = cv2.VideoCapture(0)  # Open the default camera
        self.running = True
        self.update_camera()

    def search_student(self):
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

    def search_date(self):
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

    def display_results(self, records):
        """Display the queried records in a popup window."""
        if records.empty:
            messagebox.showinfo("No Results", "No records found for the given query.")
            return

        result_window = tk.Toplevel(self.root)
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

    def update_camera(self):
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
        self.root.after(10, self.update_camera)

    def confirm_attendance(self, student_name, class_name, face_path):
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

        # Show confirmation message in a new window
        self.confirm_window = tk.Toplevel(self.root)
        self.confirm_window.title("Attendance Confirmation")
        self.confirm_window.geometry("400x200")
        self.confirmation_label = Label(
            self.confirm_window, text=message, font=("Helvetica", 12), wraplength=350, justify="center"
        )
        self.confirmation_label.pack(pady=20)
        close_button = Button(self.confirm_window, text="Close", command=self.confirm_window.destroy)
        close_button.pack(pady=10)


    def record_attendance(self):
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