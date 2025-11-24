# Facial Student Panel UI using Tkinter
from ensurepip import bootstrap
import threading
import datetime
from datetime import datetime

# UI packages
import tkinter as tk
from tkinter import ttk
from tkinter import  messagebox


# Trying Styling
import ttkbootstrap as ttbk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox

# Image Handling
import cv2
from PIL import Image, ImageTk

# Local Imports
from src.controllers.facialController import FacialController

# from src.models.User import StudentUserSchema



# --- Facial Attendance Student View (Tkinter Frame) ---


class FacialStudentPanel(tk.Frame):
    """Tkinter Frame for Facial Attendance Student Panel UI.
    """

    def __init__(self, parent, controller) -> None:
        super().__init__(parent)
        self.parent = parent
        self.controller = controller
        
        # Configure grid sizing/constraints so camera expands
        # Title is row 0, combobox row 1, controls row 2, camera row 3
        self.grid_rowconfigure(0, weight=0, pad=10)
        self.grid_rowconfigure(1, weight=0, pad=10)
        self.grid_rowconfigure(2, weight=0, pad=10)
        self.grid_rowconfigure(3, weight=1, minsize=200)
        
        # Make left and center columns expand; right-side buttons stay their natural size
        self.grid_columnconfigure(0, weight=1, uniform="maincols")
        self.grid_columnconfigure(1, weight=1, uniform="maincols")
        self.grid_columnconfigure(2, weight=0, uniform="maincols")
        self.grid_columnconfigure(3, weight=0, uniform="maincols")


        # Title label
        self.title_label = ttbk.Label(
            self, text="Facial Attendance System", font=("Helvetica", 20, "bold"), bootstyle=DEFAULT)
        # Place in row 0, spanning from column 1 to the end (before the action bar)
        self.title_label.grid(row=0, column=1, columnspan= 2, sticky="ew", pady=10, padx=10)
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

        # Actions frame for class selection and buttons
        self.actions = ttbk.Frame(self, padding=10, bootstyle=(SECONDARY))
        self.actions.grid(row=0, rowspan=4, column=3, ipadx=5, sticky="ns")

        # Extract class names shows as "course_code : name"
        class_names = [
            f"{cls['course_code']} : {cls['name']}" for cls in classes_list]
        # Class selection combobox
        self.class_list = ttk.Combobox(self.actions)
        self.class_list['values'] = class_names
        self.class_list.set("Select Class")
        self.class_list.bind("<<ComboboxSelected>>", on_select)
        # self.class_list.grid(row=0, column=0,ipadx=5,pady=10, padx=2, sticky="ne")
        self.style = ttbk.Style()
        self.style.configure("primary.TButton", font=("Helvetica", 16, "bold"))
        # Record attendance button
        self.record_button = ttbk.Button(self.actions, text="Record Attendance", command=self.record_attendance, bootstyle=SUCCESS)
        # self.record_button.grid(row=1, column=0, ipadx=5, padx=2, pady=10)

        
        # Update Student Face Data Button (Not Implemented Yet)
        # self.update_face_button = ttbk.Button(self.actions, text="Update\nPortrait", command=self.update_face_data, style="primary.TButton", bootstyle=PRIMARY)
        # self.update_face_button.grid(row=2, column=0, pady=10, padx=2)


        self.role_call = ttbk.Notebook(self.actions, bootstyle=PRIMARY)
        self.checked_in_tab = ttbk.Frame(self.role_call)
        self.not_checked_in_tab = ttbk.Frame(self.role_call)
        self.role_call.add(self.checked_in_tab, text="Present")
        self.role_call.add(self.not_checked_in_tab, text="Absent")
        
        self.present = ttbk.Frame(self.checked_in_tab)
        self.absent = ttbk.Frame(self.not_checked_in_tab)

        present_people = ["No students present yet."]
        absent_people = ["No students absent yet."]

        self.present_list = tk.Listbox(self.present)
        self.present_list.pack(fill="both", expand=True, padx=5, pady=5)
        self.present_list.insert(tk.END, *[f"* {person}" for person in present_people])
        
        self.absent_list = tk.Listbox(self.absent)
        self.absent_list.pack(fill="both", expand=True, padx=5, pady=5)
        self.absent_list.insert(tk.END, *[f"* {person}" for person in absent_people])

        

        self.class_list.pack(pady=10, expand=False, fill="x")
        ttbk.Separator(self.actions, orient='horizontal', bootstyle=PRIMARY).pack(fill="x", pady=10)
        self.role_call.pack(pady=10, expand=True, fill="both")
        ttbk.Separator(self.actions, orient='horizontal', bootstyle=PRIMARY).pack(fill="x", pady=10)
        ttbk.Separator(self.actions, orient='horizontal', bootstyle=PRIMARY).pack(fill="x", pady=10)
        self.record_button.pack(pady=20, expand=True, fill="both")

        
        # LABELFRAME STUDENT INFO
        self.name_frame = ttbk.Labelframe(self, text="Logged In As:", bootstyle=INFO)
        # Place in the top left, spanning both content rows
        self.name_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        # --- Switch to GRID inside self.name_frame ---
        self.name_frame.grid_columnconfigure(0, weight=1) # Make the single column expand
        self.name_frame.grid_rowconfigure(0, weight=1) # Name label

        self.name_label = ttbk.Label(
            self.name_frame, text="student name", font=("Helvetica", 12), bootstyle=(SECONDARY, INVERSE))
        self.name_label.grid(row=0, column=0, sticky="ew", padx=2, pady=2)


        # Main Frame for Camera and Source Image Tabs
        self.notebook = ttbk.Notebook(self, bootstyle=PRIMARY)
        self.notebook.grid(row=2, column=0, columnspan=3, rowspan=2, sticky="nsew", padx=10, pady=10)
        

        self.camera_tab = ttbk.Frame(self.notebook, bootstyle=SECONDARY)
        self.source_tab = ttbk.Frame(self.notebook, bootstyle=SECONDARY)

        self.notebook.add(self.camera_tab, text="Camera Feed")
        self.notebook.add(self.source_tab, text="Source Image")
        self.camera_tab.rowconfigure(0, weight=1)
        self.camera_tab.columnconfigure(0, weight=1)
        self.source_tab.rowconfigure(0, weight=1)
        self.source_tab.columnconfigure(0, weight=1)
        # Camera feed frame (Label used to hold image/error)
        self.camera_frame = ttbk.Label(self.camera_tab, background='black') # Added background for visibility
        # Place in row 1, spanning from column 1 to the end (before the action bar)
        self.camera_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.source_tab.rowconfigure(0, weight=1)
        self.source_tab.columnconfigure(0, weight=1)
        self.source_tab.rowconfigure(1, weight=1)
        self.source_tab.columnconfigure(1, weight=1)
        self.source_tab.grid_rowconfigure(2, weight=1)

        ttbk.Label(self.source_tab, text="Please Add Path To Image", font=("Helvetica", 14), bootstyle=(SECONDARY,INVERSE)).grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        ttbk.Button(self.source_tab, text="Update Face From File", command=self.upload_from_file, bootstyle=SUCCESS).grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.update_entry_path = ttbk.Entry(self.source_tab, bootstyle=PRIMARY)
        self.update_entry_path.insert(0, "ex: .\\Database\\Tests\\<YourFaceHere>.jpg")
        self.update_entry_path.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        # Disable record button when source tab is selected
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

        # Camera
        self.cap = cv2.VideoCapture(0)


        # Handles no camera found error
        if self.cap is None or not self.cap.isOpened():
            self.camera_frame.grid_forget()
            from ttkbootstrap.icons import Icon
            error_image = ttbk.PhotoImage(data=Icon.error)
            error_label = ttbk.Label(
                self.camera_tab, image=error_image, text=" Error: Could not access the camera.", compound="left", bootstyle=DANGER)
            error_label.pack(expand=True, fill="both", pady=20)
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
            # Low performance suspected due to camera. Release and reinitialize camera
            # if self.cap is not None and self.cap.isOpened():
            #     self.cap.release()
        except Exception as e:
            print("Error in on_show:", e)
    
    def on_tab_change(self, event):
        
        if self.source_tab.winfo_ismapped():
            self.record_button.config(state="disabled")
            # Stop Camera Feed
            # self.cap.release()
            # self.running = False
        else:
            self.record_button.config(state="normal")
            # Restart Camera Feed
            # self.cap = cv2.VideoCapture(0)
            # self.running = True
        

    # -- Update Face Data --
    def update_face_data(self) -> None:
        """Update the face data for the student in the database."""
        student_name = self.student['name']
        print(student_name)
        if not student_name:
            Messagebox.show_error(
                "Error", "Please enter a student name to update face data.",parent=self.parent,alert=True)
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
        Messagebox.show_info(
            "Success", f"Face data for {student_name} has been updated.",parent=self.parent,alert=True)

    def upload_from_file(self) -> None:
        """Upload face data from a file to update the student's face data."""
        file_path = self.update_entry_path.get().strip()
        print("File path entered:", file_path)
        try:
            unknown_face = self.fc.process_image(file_path)
            print("Unknown Face Encoding from file: ", unknown_face, type(unknown_face))
            self.student['face_data'].append(unknown_face.tolist())
            self.save_confirmation_remote()
            # Here you would add code to update the student's face data in the database
            Messagebox.show_info(
                "Success", f"Face data for {self.student['name']} has been updated.",parent=self.parent,alert=True)
        except Exception as e:
            print("Error processing image from file:", e)
            return




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
                    message = (f"{student_name} successfully recorded for attendance on {formatted_time} for class {class_name}.")
            else:
                message = "No match found. Attendance not recorded."
        except Exception as e:
            print("Error: ", e)
            message = "An error occurred. Please try again."

        # Show confirmation message in a new window
        self.confirm_window = ttbk.Toplevel(self.parent)
        self.confirm_window.title("Attendance Confirmation")
        self.confirm_window.geometry("400x200")
        self.confirm_window.transient(self.parent)
        self.confirm_window.grab_set()
        self.confirmation_label = ttbk.Label(
            self.confirm_window, text=message, font=("Helvetica", 12), wraplength=350, justify="center"
        )
        
        self.confirmation_label.pack(pady=20)
        close_button = ttbk.Button(self.confirm_window, text="Close",
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


if __name__ == "__main__":
    main()
